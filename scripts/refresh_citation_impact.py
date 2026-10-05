#!/usr/bin/env python3
"""Refresh the TSC's public, conservatively verified CoSAI citation report.

Verified citations live in sources.json and require supporting evidence.
Public GitHub code search and Crossref expose additional unreviewed candidates;
those candidates never change the verified headline counts automatically.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import os
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = REPO_ROOT / "TSC Deliverables" / "citation-impact"
GITHUB_API = "https://api.github.com"
CROSSREF_API = "https://api.crossref.org/works"
OWNER_DOMAINS = {"coalitionforsecureai.org", "oasis-open.org"}
OWNER_REPOSITORIES = {"cosai-oasis", "project-codeguard"}
KNOWN_MEMBER_OWNERS = {"google", "google-deepmind", "microsoft", "ibm", "cisco", "cisco-open", "ciscodevnet", "redhatproductsecurity"}
EASTERN_TIME = ZoneInfo("America/New_York")
CROSSREF_SEARCHES = ("Coalition for Secure AI", "CoSAI agentic security", "CoSAI Model Context Protocol")
UNVERIFIED_STATUS = "Unverified / uncertain — not counted as verified"
AUTOMATED_REPORT_URL = "https://github.com/cosai-oasis/cosai-tsc/tree/automation/citation-impact-report/TSC%20Deliverables/citation-impact"

WORKS = {
    "Model Context Protocol (MCP) Security": (
        '"CoSAI" "Model Context Protocol" extension:md -org:cosai-oasis',
        ("model context protocol", "mcp security", "mcp-security"),
    ),
    "Principles for Secure-by-Design Agentic Systems": (
        '"CoSAI" "Secure-by-Design" "Agentic" extension:md -org:cosai-oasis',
        ("secure-by-design", "secure by design", "agentic principles"),
    ),
    "AI Incident Response Framework": (
        '"CoSAI" "AI Incident Response Framework" extension:md -org:cosai-oasis',
        ("incident response",),
    ),
    "CoSAI Risk Map": (
        '"CoSAI Risk Map" extension:md -org:cosai-oasis',
        ("risk map", "risk-map"),
    ),
    "Signing ML Artifacts": (
        '"CoSAI" "Signing ML Artifacts" extension:md -org:cosai-oasis',
        ("signing ml artifacts", "model signing", "ml artifact"),
    ),
    "Agentic Identity and Access Management": (
        '"CoSAI" "Agentic Identity" extension:md -org:cosai-oasis',
        ("agentic identity", "agentic iam"),
    ),
    "AI Shared Responsibility Framework": (
        '"CoSAI" "Shared Responsibility Framework" extension:md -org:cosai-oasis',
        ("shared responsibility",),
    ),
    "Preparing Defenders of AI Systems": (
        '"CoSAI" "Preparing Defenders of AI Systems" extension:md -org:cosai-oasis',
        ("preparing defenders of ai systems",),
    ),
    "The Future of Agentic Security: From Chatbots to Autonomous Swarms": (
        '"CoSAI" "Future of Agentic Security" extension:md -org:cosai-oasis',
        ("future of agentic security", "chatbots to autonomous swarms"),
    ),
    "Establish Risks and Controls for the AI Supply Chain": (
        '"CoSAI" "Risks and Controls for the AI Supply Chain" extension:md -org:cosai-oasis',
        ("risks and controls for the ai supply chain",),
    ),
    "Project CodeGuard": (
        '"CoSAI" "Project CodeGuard" extension:md -org:cosai-oasis -org:project-codeguard',
        ("project codeguard",),
    ),
}


class FatalArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # Exit 2 is reserved for a valid but incomplete discovery snapshot.
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = FatalArgumentParser(description=__doc__)
    parser.add_argument("--discover", action="store_true", help="Look for new public GitHub and Crossref citations.")
    parser.add_argument("--skip-crossref", action="store_true", help="Skip Crossref, useful where api.crossref.org is unavailable.")
    parser.add_argument("--max-results-per-query", type=int, default=10, help="Maximum results fetched from each discovery query.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--resume-from", type=Path, help="Restore candidate/checkpoint JSON only from this data directory.")
    parser.add_argument("--discovery-budget-seconds", type=float, default=180, help="Global discovery time budget, including pacing and retries.")
    parser.add_argument("--as-of", type=date.fromisoformat, default=datetime.now(EASTERN_TIME).date(), help="Report date in YYYY-MM-DD format.")
    parser.add_argument("--fail-on-discovery-error", action="store_true", help="Exit 2 after saving an incomplete discovery snapshot; fatal errors use exit 1.")
    return parser.parse_args(argv)


def canonical_url(raw_url: str) -> str:
    """Normalize URL fragments, trailing slashes and GitHub branch/commit refs."""
    parsed = urlparse(raw_url.strip())
    host = parsed.netloc.lower().removeprefix("www.")
    parts = [piece for piece in parsed.path.split("/") if piece]
    if host == "github.com" and len(parts) >= 5 and parts[2] in {"blob", "tree"}:
        parts = parts[:2] + parts[4:]
    return f"{parsed.scheme.lower()}://{host}/{'/'.join(parts)}".rstrip("/")


def is_owner_controlled(url: str, repository: str = "") -> bool:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    owner = repository.split("/", maxsplit=1)[0].lower()
    return host in OWNER_DOMAINS or owner in OWNER_REPOSITORIES


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def github_token() -> str | None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    try:
        process = subprocess.run(["gh", "auth", "token"], check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return process.stdout.strip() or None


def timestamp(value: float | None = None) -> str:
    return datetime.fromtimestamp(time.time() if value is None else value, timezone.utc).isoformat().replace("+00:00", "Z")


def timestamp_seconds(value: str | None) -> float:
    if value is None:
        return 0
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Discovery timestamps must include a timezone")
    return parsed.timestamp()


class DiscoveryDeferred(TimeoutError):
    """A provider must wait beyond this invocation's remaining budget."""


class DiscoveryContext:
    def __init__(self, state: dict[str, Any], budget_seconds: float, checkpoint: Any = None):
        self.state = state
        self.deadline = time.monotonic() + budget_seconds
        self.checkpoint = checkpoint or (lambda: None)

    def remaining(self) -> float:
        return self.deadline - time.monotonic()

    def provider(self, name: str) -> dict[str, Any]:
        return self.state.setdefault("providers", {}).setdefault(name, {"next_retry_at": None, "last_request_at": None})

    def before_request(self, name: str) -> float:
        state = self.provider(name)
        ready = timestamp_seconds(state.get("next_retry_at"))
        if name == "github" and state.get("last_request_at"):
            ready = max(ready, timestamp_seconds(state["last_request_at"]) + 7)
        delay = max(0, ready - time.time())
        if self.remaining() <= delay:
            raise DiscoveryDeferred(f"{name} cannot run within the remaining discovery budget; next permitted request: {timestamp(ready) if ready else 'next invocation'}")
        if delay:
            print(f"{name}: waiting {delay:.1f}s before requesting (next permitted: {timestamp(ready)}).", file=sys.stderr, flush=True)
            time.sleep(delay)
        remaining = self.remaining()
        if remaining <= 0:
            raise DiscoveryDeferred("Global discovery budget exhausted; remaining queries will resume next time")
        state["last_request_at"] = timestamp()
        state["next_retry_at"] = None
        self.checkpoint()
        return min(30, remaining)

    def defer_until(self, name: str, ready: float) -> None:
        state = self.provider(name)
        state["next_retry_at"] = timestamp(max(ready, timestamp_seconds(state.get("next_retry_at"))))
        self.checkpoint()


def request_json(url: str, *, headers: dict[str, str] | None = None, context: DiscoveryContext | None = None, provider: str | None = None) -> dict[str, Any]:
    provider = provider or ("github" if urlparse(url).netloc == "api.github.com" else "crossref")
    context = context or DiscoveryContext({}, 180)
    request = Request(url, headers={"User-Agent": "cosai-tsc-citation-impact/1.0", **(headers or {})})
    for attempt in range(5):
        timeout = context.before_request(provider)
        try:
            with urlopen(request, timeout=timeout) as response:
                payload = json.load(response)
                response_headers = getattr(response, "headers", {}) or {}
                reset_at = response_headers.get("X-RateLimit-Reset")
                if response_headers.get("X-RateLimit-Remaining") == "0" and isinstance(reset_at, str) and reset_at.isdigit():
                    context.defer_until(provider, int(reset_at) + 1)
                return payload
        except HTTPError as error:
            exhausted_search_limit = error.code in {403, 429} and error.headers is not None and error.headers.get("X-RateLimit-Remaining") == "0"
            retry_after = error.headers.get("Retry-After") if error.headers is not None else None
            reset_at = error.headers.get("X-RateLimit-Reset") if error.headers is not None else None
            if error.code not in {429, 500, 502, 503, 504} and not exhausted_search_limit and not (error.code == 403 and retry_after):
                raise
            now = time.time()
            usable_reset = exhausted_search_limit and reset_at and reset_at.isdigit()
            ready = now + (60 if error.code in {403, 429} and not retry_after and not usable_reset else 2 ** attempt)
            if exhausted_search_limit:
                if reset_at and reset_at.isdigit():
                    ready = max(ready, int(reset_at) + 1)
            if retry_after:
                if retry_after.isdigit():
                    ready = max(ready, now + int(retry_after))
                else:
                    try:
                        ready = max(ready, parsedate_to_datetime(retry_after).timestamp())
                    except (TypeError, ValueError, OverflowError) as invalid_header:
                        context.defer_until(provider, now + 60)
                        raise DiscoveryDeferred(f"HTTP {error.code} from {urlparse(url).netloc}: unusable Retry-After; query deferred") from invalid_header
            context.defer_until(provider, ready)
            print(f"HTTP {error.code} from {urlparse(url).netloc}: next permitted retry at {timestamp(ready)} ({math.ceil(ready - now)}s); attempt {attempt + 1}/5.", file=sys.stderr, flush=True)
            if attempt == 4:
                raise DiscoveryDeferred(f"{provider} exhausted five attempts; query and retry time saved for the next invocation") from error
    raise RuntimeError(f"Request retry loop terminated unexpectedly for {url}")


def source_snippet(item: dict[str, Any]) -> str:
    matches = item.get("text_matches", [])
    fragments = [match.get("fragment", "") for match in matches if match.get("fragment")]
    snippet = " ".join(fragments)
    return " ".join(snippet.split())[:320]


def github_candidates(payload: dict[str, Any], work: str) -> list[dict[str, Any]]:
    if not isinstance(payload.get("items"), list):
        raise ValueError("GitHub discovery response has no items array")
    discovered: dict[str, dict[str, Any]] = {}
    for item in payload["items"]:
        repository = item.get("repository", {})
        full_name = repository.get("full_name", "")
        url = item.get("html_url", "")
        if not url or repository.get("private") is not False or repository.get("fork") or is_owner_controlled(url, full_name):
            continue
        key = canonical_url(url)
        discovered[key] = {
            "publisher": full_name,
            "title": item.get("path") or item.get("name") or full_name,
            "url": url,
            "matched_works": [work],
            "discovery_provider": "GitHub public code search",
            "evidence": source_snippet(item),
            "status": UNVERIFIED_STATUS,
            "publisher_relationship": "Known member-affiliated" if full_name.split("/", 1)[0].lower() in KNOWN_MEMBER_OWNERS else "Not established",
        }
    return list(discovered.values())


def crossref_text(item: dict[str, Any]) -> str:
    references = " ".join(reference.get("unstructured", "") for reference in item.get("reference", []))
    titles = " ".join(item.get("title", []))
    abstract = re.sub(r"<[^>]+>", " ", html.unescape(item.get("abstract", "")))
    return " ".join((titles, abstract, references)).strip()


def matched_works(text: str) -> list[str]:
    lowered = text.lower()
    return [work for work, (_, terms) in WORKS.items() if any(term in lowered for term in terms)]


def crossref_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    items = payload.get("message", {}).get("items")
    if not isinstance(items, list):
        raise ValueError("Crossref discovery response has no items array")
    found: dict[str, dict[str, Any]] = {}
    for item in items:
        text = crossref_text(item)
        if not re.search(r"\bcoalition for secure ai\b|\bcosai\b", text, flags=re.IGNORECASE):
            continue
        title = " ".join(item.get("title", []))
        url = item.get("URL") or (f"https://doi.org/{item['DOI']}" if item.get("DOI") else "")
        publisher = item.get("publisher", "Unknown publisher")
        if not url or is_owner_controlled(url) or re.search(r"\boasis\b|coalition for secure ai", publisher, re.IGNORECASE):
            continue
        key = canonical_url(url)
        found[key] = {
            "publisher": publisher,
            "title": title,
            "url": url,
            "matched_works": matched_works(text),
            "discovery_provider": "Crossref scholarly metadata",
            "evidence": " ".join(text.split())[:320],
            "status": UNVERIFIED_STATUS,
            "publisher_relationship": "Not established",
        }
    return list(found.values())


def merge_candidates(existing: list[dict[str, Any]], discovered: list[dict[str, Any]], verified: list[dict[str, Any]], as_of: date, excluded: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    verified_urls = {canonical_url(item["source_url"]) for item in verified}
    excluded_urls = {canonical_url(item["source_url"]) for item in excluded or []}
    disallowed_urls = verified_urls | excluded_urls
    combined = {
        canonical_url(item["url"]): item
        for item in existing
        if canonical_url(item["url"]) not in disallowed_urls
    }
    for candidate in discovered:
        key = canonical_url(candidate["url"])
        if key in disallowed_urls:
            continue
        if key in combined:
            current = combined[key]
            current["last_seen"] = as_of.isoformat()
            current["matched_works"] = sorted(set(current.get("matched_works", [])) | set(candidate.get("matched_works", [])))
            if not current.get("evidence"):
                current["evidence"] = candidate.get("evidence", "")
            continue
        combined[key] = {**candidate, "first_seen": as_of.isoformat(), "last_seen": as_of.isoformat()}
    return sorted(combined.values(), key=lambda item: (item.get("first_seen", ""), item.get("publisher", ""), item.get("title", "")))


def discovery_queries(max_results: int) -> list[dict[str, str]]:
    return [
        {"id": f"github:{work}", "provider": "github", "label": work,
         "url": f"{GITHUB_API}/search/code?{urlencode({'q': query + ' is:public', 'per_page': max_results})}"}
        for work, (query, _) in WORKS.items()
    ] + [
        {"id": f"crossref:{query}", "provider": "crossref", "label": query,
         "url": f"{CROSSREF_API}?{urlencode({'query.bibliographic': query, 'rows': max_results})}"}
        for query in CROSSREF_SEARCHES
    ]


def query_plan(queries: list[dict[str, str]]) -> str:
    return hashlib.sha256(json.dumps(queries, sort_keys=True).encode()).hexdigest()


def stored_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("candidates", []), list):
        raise ValueError("Candidate data must be an object with a candidates array")
    candidates = payload.get("candidates", [])
    for item in candidates:
        if not isinstance(item, dict) or not all(isinstance(item.get(key), str) for key in ("url", "title", "publisher")):
            raise ValueError("Stored candidates require url, title and publisher strings")
        if not item["url"].startswith("https://") or not isinstance(item.get("matched_works", []), list) or not all(isinstance(work, str) for work in item.get("matched_works", [])):
            raise ValueError("Stored candidates require HTTPS URLs and string matched_works")
    return candidates


def merge_stored_candidates(payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Restoring saved data is not a new observation; keep its original dates."""
    combined: dict[str, dict[str, Any]] = {}
    for payload in payloads:
        for item in stored_candidates(payload):
            key = canonical_url(item["url"])
            if key not in combined:
                combined[key] = {**item, "status": UNVERIFIED_STATUS}
                continue
            current = combined[key]
            current["matched_works"] = sorted(set(current.get("matched_works", [])) | set(item.get("matched_works", [])))
            for field, choose in (("first_seen", min), ("last_seen", max)):
                dates = [record[field] for record in (current, item) if record.get(field)]
                if dates:
                    current[field] = choose(dates)
            if not current.get("evidence"):
                current["evidence"] = item.get("evidence", "")
    return list(combined.values())


def validate_state(state: dict[str, Any]) -> None:
    if not isinstance(state, dict) or state.get("schema_version") != 1:
        raise ValueError("Unsupported discovery-state.json schema")
    if not isinstance(state.get("query_plan"), str) or not isinstance(state.get("completed_queries"), list) or not all(isinstance(key, str) for key in state["completed_queries"]):
        raise ValueError("Invalid discovery query checkpoint")
    for field in ("updated_at", "round_started_at", "round_completed_at", "last_attempted", "last_completed"):
        timestamp_seconds(state.get(field))
    if not isinstance(state.get("providers", {}), dict) or not isinstance(state.get("query_warnings", {}), dict):
        raise ValueError("Invalid discovery provider checkpoint")
    if not all(isinstance(key, str) and isinstance(value, str) for key, value in state.get("query_warnings", {}).items()):
        raise ValueError("Discovery warnings must be strings")
    for provider in state.get("providers", {}).values():
        if not isinstance(provider, dict):
            raise ValueError("Invalid provider checkpoint")
        timestamp_seconds(provider.get("next_retry_at"))
        timestamp_seconds(provider.get("last_request_at"))
    stored_candidates(state)


def load_discovery_data(output_dir: Path, resume_from: Path | None, queries: list[dict[str, str]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payloads: list[dict[str, Any]] = []
    states: list[dict[str, Any]] = []
    for directory in dict.fromkeys([output_dir, *([resume_from.resolve()] if resume_from else [])]):
        payloads.append(load_json(directory / "discovered-candidates.json", {"candidates": []}))
        state_path = directory / "discovery-state.json"
        if state_path.exists():
            state = load_json(state_path, {})
            validate_state(state)
            states.append(state)
            payloads.append(state)
    fingerprint = query_plan(queries)
    matching = [state for state in states if state["query_plan"] == fingerprint]
    state = max(matching, key=lambda item: (timestamp_seconds(item.get("last_attempted")), len(set(item["completed_queries"])), timestamp_seconds(item.get("updated_at"))), default=None)
    if state is None:
        # Old last_refreshed/discovery_enabled metadata does not prove discovery completed.
        state = {"schema_version": 1, "query_plan": fingerprint, "round_started_at": None,
                 "round_completed_at": None, "completed_queries": [], "last_attempted": None,
                 "last_completed": None, "providers": {}, "query_warnings": {}, "candidates": []}
    query_ids = {query["id"] for query in queries}
    if not set(state["completed_queries"]) <= query_ids:
        raise ValueError("Checkpoint contains query IDs outside its query plan")
    # A changed query plan does not waive a provider's persisted rate limit.
    for previous in states:
        for name, provider in previous.get("providers", {}).items():
            current = state.setdefault("providers", {}).setdefault(name, {})
            for field in ("next_retry_at", "last_request_at"):
                values = [record.get(field) for record in (current, provider) if record.get(field)]
                if values:
                    current[field] = max(values, key=timestamp_seconds)
    # Completion metadata is accepted only from the new schema and matching query plan.
    for payload in payloads:
        coverage = payload.get("query_coverage", {})
        valid_metadata = (isinstance(coverage, dict) and coverage.get("total") == len(queries)
                          and isinstance(coverage.get("completed"), int) and 0 <= coverage["completed"] <= len(queries)
                          and payload.get("discovery_status") in {"complete", "partial", "not_run"}
                          and (payload.get("discovery_status") != "complete" or coverage["completed"] == len(queries)))
        if not matching and valid_metadata and payload.get("schema_version") == 1 and payload.get("query_plan") == fingerprint:
            for field in ("last_attempted", "last_completed"):
                value = payload.get(field)
                if value and timestamp_seconds(value) > timestamp_seconds(state.get(field)):
                    state[field] = value
    return state, merge_stored_candidates(payloads)


def atomic_write(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def run_discovery(queries: list[dict[str, str]], state: dict[str, Any], context: DiscoveryContext,
                  verified: list[dict[str, Any]], excluded: list[dict[str, Any]], as_of: date,
                  skip_crossref: bool, notices: list[str]) -> None:
    token = github_token()
    headers = {"Accept": "application/vnd.github.text-match+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"} if token else None
    blocked: set[str] = set()
    for index, query in enumerate(queries, start=1):
        key, provider, label = query["id"], query["provider"], query["label"]
        if key in state["completed_queries"] or provider in blocked:
            continue
        if provider == "github" and not token:
            notices.append("GitHub code search was skipped because GITHUB_TOKEN/GH_TOKEN was unavailable.")
            blocked.add(provider)
            continue
        if provider == "crossref" and skip_crossref:
            notices.append("Crossref was explicitly skipped; its pending queries remain incomplete.")
            blocked.add(provider)
            continue
        if context.remaining() <= 0:
            notices.append("Global discovery budget exhausted; remaining queries will resume next time.")
            break
        print(f"{provider} discovery {index}/{len(queries)}: {label}", file=sys.stderr, flush=True)
        try:
            payload = request_json(query["url"], headers=headers if provider == "github" else None, context=context, provider=provider)
        except (HTTPError, URLError, TimeoutError) as error:
            warning = f"{provider} discovery for {label} incomplete: {error}"
            state["query_warnings"][key] = warning
            print(f"WARNING: {warning}", file=sys.stderr, flush=True)
            if isinstance(error, TimeoutError) or (isinstance(error, HTTPError) and error.code in {401, 403, 429}):
                blocked.add(provider)
            context.checkpoint()
            continue
        discovered = github_candidates(payload, label) if provider == "github" else crossref_candidates(payload)
        state["candidates"] = merge_candidates(state["candidates"], discovered, verified, as_of, excluded)
        print(f"{provider} discovery retained {len(discovered)} external matches for {label}.", file=sys.stderr, flush=True)
        if payload.get("incomplete_results", False):
            state["query_warnings"][key] = f"{provider} returned incomplete_results for {label}; partial matches saved and this query will resume."
        else:
            state["completed_queries"].append(key)
            state["query_warnings"].pop(key, None)
        context.checkpoint()


def markdown_link(label: str, url: str) -> str:
    label = html.escape(" ".join(label.split()), quote=False).replace("[", "(").replace("]", ")").replace("|", "&#124;")
    destination = quote(url, safe=":/?#[]@!$&'*+,;=%-._~")
    return f"[{label}]({destination})"


def discovery_review_entries(verified: list[dict[str, Any]], candidates: list[dict[str, Any]], excluded: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the complete discovery trail after candidates are reviewed or excluded."""
    entries = [
        {
            "publisher": item.get("publisher", item["id"]),
            "title": item.get("citing_publication", item["id"]),
            "url": item["source_url"],
            "matched_works": item.get("cosai_works", []),
            "status": "Verified — included in totals",
        }
        for item in verified]
    entries.extend({**item, "status": UNVERIFIED_STATUS} for item in candidates)
    for item in excluded:
        parts = [part for part in urlparse(item["source_url"]).path.split("/") if part]
        publisher = "/".join(parts[:2]) if len(parts) >= 2 else urlparse(item["source_url"]).netloc
        title = "/".join(parts[4:]) if len(parts) > 4 else publisher
        entries.append({
            "publisher": publisher,
            "title": title,
            "url": item["source_url"],
            "matched_works": item.get("matched_works", []),
            "status": f"Excluded — {item['reason']}",
        })
    return sorted(entries, key=lambda item: (item["publisher"].casefold(), item["title"].casefold()))


def render_report(verified: list[dict[str, Any]], candidates: list[dict[str, Any]], warnings: list[str], as_of: date, discovery_enabled: bool, excluded: list[dict[str, Any]] | None = None, discovery_metadata: dict[str, Any] | None = None) -> str:
    citing = [item for item in verified if item.get("cosai_works")]
    mentions = [item for item in verified if not item.get("cosai_works")]
    edges = sum(len(item.get("cosai_works", [])) for item in citing)
    formal = sum(item.get("category") == "Formal reference" for item in citing)
    substantive = sum(item.get("category") == "Substantive work citation" for item in citing)
    distribution = Counter(work for item in citing for work in item["cosai_works"])
    directly_inspected = sum(item.get("verification") == "Directly inspected" for item in verified)
    by_id = {item["id"]: item for item in verified}
    review_entries = discovery_review_entries(verified, candidates, excluded or [])
    discovered_verified = sum(item["status"].startswith("Verified") for item in review_entries)
    preferred_sources = ("C96", "C60", "C61", "C82", "C97", "C53", "C92", "C95", "C31", "C01", "C02", "C04", "C05", "C08", "C09", "C10", "C30", "C32", "C33")
    source_priority = {identifier: position for position, identifier in enumerate(preferred_sources)}
    metadata = discovery_metadata or {}
    coverage = metadata.get("query_coverage", {})
    status = metadata.get("discovery_status", "partial" if discovery_enabled else "not_run")

    lines = [
        "# CoSAI Citation and External Impact",
        "",
        "> [!NOTE]",
        f"> **Last updated: {as_of.strftime('%B %-d, %Y')}**",
        "> Snapshot generation date, not evidence that every discovery query completed.",
        f"> **Discovery status: {status}.** Current round: **{coverage.get('completed', 0)} of {coverage.get('total', 'unrecorded')} configured queries completed**.",
        f"> Last attempted: **{metadata.get('last_attempted') or 'not recorded'}**. Last fully completed query round: **{metadata.get('last_completed') or 'not recorded'}**.",
        "> Automated discovery does not re-verify existing sources in the verified registry.",
        ">",
        "> Scheduled refresh: every Monday at **12:00 p.m. Eastern Time** (`America/New_York`).",
        "",
        f"**Automatically published report:** [Latest discovery snapshot]({AUTOMATED_REPORT_URL}). The `main` branch may contain an older snapshot.",
        "",
        "**Scope:** Publicly discoverable references to Coalition for Secure AI publications and frameworks.",
        "",
        "## Summary",
        "",
        "| Measure | Count | What it means |",
        "| --- | --- | --- |",
        f"| Publications citing CoSAI work | **{len(citing)}** | External publications reference at least one of {len(distribution)} CoSAI papers, frameworks or technical works. |",
        f"| Total citations | **{edges}** | Those {len(citing)} publications create {edges} citation relationships because some reference multiple CoSAI works. |",
        f"| Type of use | **{formal} formal; {substantive} substantive** | Of the same {len(citing)} publications, {formal} cite CoSAI formally and {substantive} discuss or apply its work. |",
        f"| Organization-only mentions | **{len(mentions)} additional; {len(verified)} total** | Another {len(mentions)} publications mention CoSAI without citing a specific work, bringing the overall total to {len(verified)}. |",
        f"| Unverified / uncertain findings | **{len(candidates)}** | Automatically published discoveries; not included in verified publication or citation totals. |",
        "",
        "Here, **external** means published outside CoSAI/OASIS-controlled channels; it does not imply that every publisher is unaffiliated with CoSAI.",
        "",
        "## Most-cited CoSAI publications and frameworks",
        "",
        "| CoSAI publication or framework | Distinct citing publications | Selected external citations |",
        "| --- | ---: | --- |",
    ]
    for work, count in sorted(distribution.items(), key=lambda pair: (-pair[1], pair[0])):
        work_sources = sorted(
            (item for item in citing if work in item["cosai_works"]),
            key=lambda item: (source_priority.get(item["id"], len(preferred_sources)), item.get("publisher", item["id"]).casefold()),
        )
        examples = "; ".join(markdown_link(item.get("publisher", item["id"]), item["source_url"]) for item in work_sources[:3])
        lines.append(f"| {work} | {count} | {examples} |")
    lines += [
        "",
        "## Examples of real-world use",
        "",
    ]
    if "C96" in by_id:
        lines.append(f"- **Government guidance:** The U.S. National Security Agency {markdown_link('formally cites CoSAI MCP Security', by_id['C96']['source_url'])}; this is not a government endorsement.")
    if "C60" in by_id and "C61" in by_id:
        specification = markdown_link("security specification", by_id["C60"]["source_url"])
        testing = markdown_link("audit tests", by_id["C61"]["source_url"])
        lines.append(f"- **Security standards:** The App Defense Alliance applies CoSAI’s MCP threat model in an AI-tool {specification} and corresponding {testing}.")
    if "C97" in by_id or "C31" in by_id:
        examples = []
        if "C97" in by_id:
            examples.append(markdown_link("OWASP GenAI Security Project", by_id["C97"]["source_url"]))
        if "C31" in by_id:
            examples.append(markdown_link("OWASP AI Security Verification Standard", by_id["C31"]["source_url"]))
        lines.append(f"- **Practitioner standards:** {' and '.join(examples)} reference CoSAI security guidance.")
    if "C82" in by_id:
        lines.append(f"- **Supply-chain security:** {markdown_link('OpenSSF reports model-signing adoption by IBM and Cohere', by_id['C82']['source_url'])} in connection with CoSAI work.")
    if "C53" in by_id or "C92" in by_id:
        examples = []
        if "C53" in by_id:
            examples.append(markdown_link("Red Hat Product Security", by_id["C53"]["source_url"]))
        if "C92" in by_id:
            examples.append(markdown_link("Cisco DevNet", by_id["C92"]["source_url"]))
        lines.append(f"- **Secure-development tooling:** {' and '.join(examples)} incorporate or reference Project CodeGuard.")
    if "C95" in by_id:
        lines.append(f"- **Shared responsibility:** {markdown_link('An external practitioner analysis', by_id['C95']['source_url'])} applies CoSAI’s framework to provider and customer accountability.")

    lines += [
        "",
        "## Complete CoSAI paper-to-source register",
        "",
        f"Every verified publication-to-work relationship is listed below: **{edges} distinct citations across {len(distribution)} CoSAI papers, frameworks and other technical works**. Sources citing multiple CoSAI works correctly appear once under each work.",
        "",
        "| CoSAI paper or framework | External citing publication | Publisher | Citation type | Verification | Publisher relationship |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for work, _ in sorted(distribution.items(), key=lambda pair: (-pair[1], pair[0])):
        work_sources = sorted((item for item in citing if work in item["cosai_works"]), key=lambda item: (item.get("publisher", item["id"]).casefold(), item.get("citing_publication", work).casefold()))
        for item in work_sources:
            publication = markdown_link(item.get("citing_publication", work), item["source_url"])
            relationship = item.get("publisher_relationship", "Not established")
            publisher = item.get("publisher", item["id"])
            lines.append(f"| {work} | {publication} | {publisher} | {item['category']} | {item['verification']} | {relationship} |")

    lines += [
        "",
        "## Methodology",
        "",
        "1. Identify CoSAI’s published papers, frameworks, workstream outputs and canonical GitHub artifacts.",
        "2. Search public research, policy, standards, enterprise documentation and open-source references for the coalition name and publication titles.",
        "3. Verify the source directly or from a precise indexed excerpt, then classify the reference as a formal citation, substantive framework use or organization-only mention.",
        "4. Exclude CoSAI/OASIS self-citations, owner-controlled announcements, copied papers, translated duplicates, repeated publisher material, generated-chat exports and NIST COSAiS false positives; count each publication-to-work relationship only once.",
        "",
        f"Of the **{len(verified)} verified sources**, **{directly_inspected} were inspected directly** and **{len(verified) - directly_inspected} were confirmed from precise search-index excerpts**. Known member- and contributor-affiliated publishers, along with source-date discrepancies, are identified in [`sources.json`](sources.json).",
        f"Reviewed false positives, mirrors and duplicate publisher listings are excluded permanently; **{len(excluded or [])} reviewed exclusions** are recorded in [`excluded-sources.json`](excluded-sources.json).",
        "",
        "## Discovery and review status",
        "",
        f"The discovery log contains **{len(review_entries)} references**: **{discovered_verified} verified and counted**, **{len(candidates)} unverified / uncertain**, and **{len(excluded or [])} excluded as false positives, copied materials or duplicates**.",
        "",
        "<details>",
        f"<summary>View all {len(review_entries)} references</summary>",
        "",
        "| External reference | CoSAI works identified | Verification status |",
        "| --- | --- | --- |",
    ]
    for item in review_entries:
        works = "; ".join(item.get("matched_works", [])) or "CoSAI organizational mention"
        lines.append(f"| {markdown_link(item['publisher'] + ': ' + item['title'], item['url'])} | {works} | {item['status']} |")

    lines += [
        "",
        "</details>",
        "",
        "## Unverified / uncertain discoveries",
        "",
    ]
    metadata = discovery_metadata or {}
    coverage = metadata.get("query_coverage", {})
    status = metadata.get("discovery_status", "partial" if discovery_enabled else "not_run")
    lines += [
        f"**Discovery status: {status}.** Last attempted: **{metadata.get('last_attempted') or 'not recorded'}**. Last fully completed query round: **{metadata.get('last_completed') or 'not recorded'}**.",
        "",
    ]
    if coverage:
        lines.append(f"Current round: **{coverage['completed']} of {coverage['total']} configured queries completed**. Completed queries are checkpointed and partial rounds resume on the next run.")
        lines.append("")
    lines.append("Completion means the configured, result-capped GitHub and Crossref queries finished; it does not mean exhaustive coverage of the web or all scholarly citations.")
    lines.append("")
    lines.append(f"There are **{len(candidates)} candidate references**, including retained findings from earlier attempts. These are automatically published as **unverified / uncertain** and are **not included** in verified totals. Only evidence-supported entries in [`sources.json`](sources.json) contribute to verified counts.")
    if candidates:
        lines += ["", "<details>", f"<summary>View {min(len(candidates), 15)} candidate references</summary>", ""]
        for candidate in candidates[:15]:
            works = "; ".join(candidate.get("matched_works", [])) or "CoSAI organization mention"
            lines.append(f"- {markdown_link(candidate['publisher'], candidate['url'])}: {works}.")
        if len(candidates) > 15:
            lines.append(f"- See [`discovered-candidates.json`](discovered-candidates.json) for all {len(candidates)} candidates.")
        lines += ["", "</details>"]
    if warnings:
        lines += ["", "**Discovery warnings:**"]
        lines.extend(f"- {warning}" for warning in warnings)
    lines += [
        "",
        "## Refresh and verification",
        "",
        "- GitHub Actions refreshes this report every Monday at 12:00 p.m. Eastern Time, including daylight-saving changes, and can also be started manually.",
        "- The workflow automatically publishes complete and partial snapshots on `automation/citation-impact-report`; uncertain findings do not require review before publication and never increase verified counts automatically.",
        "- Evidence-supported citations belong in [`sources.json`](sources.json), with their `discovery_provider` preserved. Entries without sufficient support remain visibly unverified / uncertain.",
        "- To reject copied or duplicative material, record its source, matched works and reason in [`excluded-sources.json`](excluded-sources.json). Future refreshes will not rediscover it as pending.",
        "- GitHub code search discovers public code/documentation references; Crossref adds matching scholarly metadata. General-web discovery can be added later through an approved search provider.",
        "",
        "**Interpretation:** These figures are verified public-web minimums, not a comprehensive academic citation count, Google Scholar metric or social-media reach measure.",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.max_results_per_query < 1 or args.max_results_per_query > 100:
        raise ValueError("--max-results-per-query must be between 1 and 100")
    if not math.isfinite(args.discovery_budget_seconds) or args.discovery_budget_seconds <= 0:
        raise ValueError("--discovery-budget-seconds must be a positive finite number")
    output_dir = args.output_dir.resolve()
    verified_path = output_dir / "sources.json"
    excluded_path = output_dir / "excluded-sources.json"
    candidates_path = output_dir / "discovered-candidates.json"
    report_path = output_dir / "README.md"
    verified = load_json(verified_path, [])
    if not verified:
        raise ValueError(f"No verified sources found at {verified_path}")
    source_ids = [item["id"] for item in verified]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Verified source IDs must be unique")
    if not all(item.get("source_url", "").startswith("https://") for item in verified):
        raise ValueError("Every verified source must have an HTTPS source URL")
    excluded = load_json(excluded_path, [])
    if not all(item.get("source_url", "").startswith("https://") for item in excluded):
        raise ValueError("Every reviewed exclusion must have an HTTPS source URL")
    verified_urls = {canonical_url(item["source_url"]) for item in verified}
    excluded_urls = {canonical_url(item["source_url"]) for item in excluded}
    if len(excluded_urls) != len(excluded):
        raise ValueError("Reviewed exclusions must have unique source URLs")
    if verified_urls & excluded_urls:
        raise ValueError("A source cannot be both verified and excluded")

    queries = discovery_queries(args.max_results_per_query)
    state, existing = load_discovery_data(output_dir, args.resume_from, queries)
    state["candidates"] = merge_candidates(existing, [], verified, args.as_of, excluded)
    notices: list[str] = []
    if args.discover:
        if len(set(state["completed_queries"])) == len(queries):
            state["completed_queries"] = []
            state["query_warnings"] = {}
            state["round_started_at"] = None
            state["round_completed_at"] = None
        state["round_started_at"] = state.get("round_started_at") or timestamp()
        state["last_attempted"] = timestamp()

    candidates_payload: dict[str, Any] = {}

    def checkpoint() -> None:
        nonlocal candidates_payload
        completed = len(set(state["completed_queries"]))
        status = ("complete" if completed == len(queries) else "partial") if args.discover else "not_run"
        if status == "complete" and not state.get("round_completed_at"):
            state["round_completed_at"] = timestamp()
            state["last_completed"] = state["round_completed_at"]
        state["updated_at"] = timestamp()
        warnings = list(dict.fromkeys([*notices, *state.get("query_warnings", {}).values()]))
        candidates_payload = {
            "schema_version": 1,
            "query_plan": state["query_plan"],
            "last_refreshed": args.as_of.isoformat(),
            "last_attempted": state.get("last_attempted"),
            "last_completed": state.get("last_completed"),
            "description": "Automatically published unverified / uncertain CoSAI references; not included in verified totals.",
            "discovery_enabled": args.discover,
            "discovery_status": status,
            "discovery_warnings": warnings,
            "query_coverage": {"completed": completed, "total": len(queries), "round_started_at": state.get("round_started_at"),
                               "per_provider": {provider: {"completed": sum(query["id"] in state["completed_queries"] for query in queries if query["provider"] == provider),
                                                          "total": sum(query["provider"] == provider for query in queries)} for provider in ("github", "crossref")}},
            "candidates": state["candidates"],
        }
        report = render_report(verified, state["candidates"], warnings, args.as_of, args.discover, excluded, candidates_payload)
        # The checkpoint contains candidates as well as query progress, so a later
        # interrupted write cannot make resumed progress lose already found data.
        atomic_write(output_dir / "discovery-state.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n")
        atomic_write(candidates_path, json.dumps(candidates_payload, indent=2, ensure_ascii=False) + "\n")
        atomic_write(report_path, report)

    checkpoint()
    if args.discover:
        context = DiscoveryContext(state, args.discovery_budget_seconds, checkpoint)
        run_discovery(queries, state, context, verified, excluded, args.as_of, args.skip_crossref, notices)
    checkpoint()
    print(f"Verified sources: {len(verified)}")
    print(f"Verified work-level citations: {sum(len(item.get('cosai_works', [])) for item in verified)}")
    print(f"Unverified / uncertain discovery candidates: {len(state['candidates'])}")
    print(f"Discovery status: {candidates_payload['discovery_status']} ({candidates_payload['query_coverage']['completed']}/{len(queries)} queries complete)")
    for warning in candidates_payload["discovery_warnings"]:
        print(f"WARNING: {warning}", file=sys.stderr)
    return 2 if args.fail_on_discovery_error and candidates_payload["discovery_status"] == "partial" else 0


if __name__ == "__main__":
    raise SystemExit(main())
