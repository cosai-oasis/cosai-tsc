#!/usr/bin/env python3
"""Refresh the TSC's public, conservatively verified CoSAI citation report.

Verified citations live in sources.json and are promoted by human reviewers.
Public GitHub code search and Crossref expose additional unreviewed candidates;
those candidates never change the verified headline counts automatically.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discover", action="store_true", help="Look for new public GitHub and Crossref citations.")
    parser.add_argument("--skip-crossref", action="store_true", help="Skip Crossref, useful where api.crossref.org is unavailable.")
    parser.add_argument("--max-results-per-query", type=int, default=10, help="Maximum results fetched from each discovery query.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--as-of", type=date.fromisoformat, default=datetime.now(EASTERN_TIME).date(), help="Report date in YYYY-MM-DD format.")
    parser.add_argument("--fail-on-discovery-error", action="store_true", help="Exit nonzero when a discovery provider cannot be reached.")
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


def request_json(url: str, *, headers: dict[str, str] | None = None) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": "cosai-tsc-citation-impact/1.0", **(headers or {})})
    for attempt in range(5):
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            exhausted_search_limit = error.code == 403 and error.headers is not None and error.headers.get("X-RateLimit-Remaining") == "0"
            if (error.code not in {429, 500, 502, 503, 504} and not exhausted_search_limit) or attempt == 4:
                raise
            retry_after = error.headers.get("Retry-After") if error.headers is not None else None
            reset_at = error.headers.get("X-RateLimit-Reset") if error.headers is not None else None
            if exhausted_search_limit and reset_at and reset_at.isdigit():
                delay = min(max(int(reset_at) - int(time.time()) + 1, 1), 60)
            elif retry_after and retry_after.isdigit():
                delay = min(int(retry_after), 60)
            else:
                delay = 2 ** attempt
            time.sleep(delay)
    raise RuntimeError(f"Request retry loop terminated unexpectedly for {url}")


def source_snippet(item: dict[str, Any]) -> str:
    matches = item.get("text_matches", [])
    fragments = [match.get("fragment", "") for match in matches if match.get("fragment")]
    snippet = " ".join(fragments)
    return " ".join(snippet.split())[:320]


def discover_github(max_results: int) -> tuple[list[dict[str, Any]], list[str]]:
    token = github_token()
    if not token:
        return [], ["GitHub code search was skipped because GITHUB_TOKEN/GH_TOKEN was unavailable."]

    headers = {
        "Accept": "application/vnd.github.text-match+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    discovered: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []
    for work, (query, _) in WORKS.items():
        endpoint = f"{GITHUB_API}/search/code?{urlencode({'q': query, 'per_page': max_results})}"
        try:
            payload = request_json(endpoint, headers=headers)
        except (HTTPError, URLError, TimeoutError) as error:
            warnings.append(f"GitHub discovery for {work} failed: {error}")
            continue

        for item in payload.get("items", []):
            repository = item.get("repository", {})
            full_name = repository.get("full_name", "")
            url = item.get("html_url", "")
            if not url or repository.get("fork") or is_owner_controlled(url, full_name):
                continue
            key = canonical_url(url)
            candidate = discovered.setdefault(key, {
                "publisher": full_name,
                "title": item.get("path") or item.get("name") or full_name,
                "url": url,
                "matched_works": [],
                "discovery_provider": "GitHub public code search",
                "evidence": source_snippet(item),
                "status": "Needs human review",
                "publisher_relationship": "Known member-affiliated" if full_name.split("/", 1)[0].lower() in KNOWN_MEMBER_OWNERS else "Not established",
            })
            if work not in candidate["matched_works"]:
                candidate["matched_works"].append(work)
            if not candidate["evidence"]:
                candidate["evidence"] = source_snippet(item)
    return list(discovered.values()), warnings


def crossref_text(item: dict[str, Any]) -> str:
    references = " ".join(reference.get("unstructured", "") for reference in item.get("reference", []))
    titles = " ".join(item.get("title", []))
    abstract = re.sub(r"<[^>]+>", " ", html.unescape(item.get("abstract", "")))
    return " ".join((titles, abstract, references)).strip()


def matched_works(text: str) -> list[str]:
    lowered = text.lower()
    return [work for work, (_, terms) in WORKS.items() if any(term in lowered for term in terms)]


def discover_crossref(max_results: int) -> tuple[list[dict[str, Any]], list[str]]:
    searches = ("Coalition for Secure AI", "CoSAI agentic security", "CoSAI Model Context Protocol")
    found: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []
    for query in searches:
        endpoint = f"{CROSSREF_API}?{urlencode({'query.bibliographic': query, 'rows': max_results})}"
        try:
            payload = request_json(endpoint)
        except (HTTPError, URLError, TimeoutError) as error:
            warnings.append(f"Crossref discovery for {query} failed: {error}")
            continue

        for item in payload.get("message", {}).get("items", []):
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
                "status": "Needs human review",
                "publisher_relationship": "Not established",
            }
    return list(found.values()), warnings


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


def markdown_link(label: str, url: str) -> str:
    return f"[{label.replace('[', '(').replace(']', ')').replace('|', '&#124;')}]({url.replace(' ', '%20')})"


def discovery_review_entries(verified: list[dict[str, Any]], candidates: list[dict[str, Any]], excluded: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the complete discovery trail after candidates are reviewed or excluded."""
    entries = [
        {
            "publisher": item["publisher"],
            "title": item["citing_publication"],
            "url": item["source_url"],
            "matched_works": item.get("cosai_works", []),
            "status": "Verified — included in totals",
        }
        for item in verified
        if item.get("discovery_provider")
    ]
    entries.extend({**item, "status": "Pending human review — not counted"} for item in candidates)
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


def render_report(verified: list[dict[str, Any]], candidates: list[dict[str, Any]], warnings: list[str], as_of: date, discovery_enabled: bool, excluded: list[dict[str, Any]] | None = None) -> str:
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

    lines = [
        "# CoSAI Citation and External Impact",
        "",
        "> [!NOTE]",
        f"> **Last updated: {as_of.strftime('%B %-d, %Y')}**",
        ">",
        "> Scheduled refresh: every Monday at **12:00 p.m. Eastern Time** (`America/New_York`).",
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
        f"The discovery log contains **{len(review_entries)} references**: **{discovered_verified} verified and counted**, **{len(candidates)} awaiting review**, and **{len(excluded or [])} excluded as false positives, copied materials or duplicates**. The remaining **{len(verified) - discovered_verified} verified sources** were found through direct research and are included in the complete source register above.",
        "",
        "<details>",
        f"<summary>View all {len(review_entries)} reviewed references</summary>",
        "",
        "| External reference | CoSAI works identified | Review status |",
        "| --- | --- | --- |",
    ]
    for item in review_entries:
        works = "; ".join(item.get("matched_works", [])) or "CoSAI organizational mention"
        lines.append(f"| {markdown_link(item['publisher'] + ': ' + item['title'], item['url'])} | {works} | {item['status']} |")

    lines += [
        "",
        "</details>",
        "",
        "## New references awaiting review",
        "",
    ]
    if discovery_enabled:
        lines.append(f"The scheduled refresh identified **{len(candidates)} candidate references**. These are **not included** in the verified counts until a reviewer confirms and promotes them to [`sources.json`](sources.json).")
    elif candidates:
        lines.append(f"There are **{len(candidates)} previously discovered candidate references** awaiting review. Run the scheduled workflow or use `--discover` to search again.")
    else:
        lines.append("All currently discovered references have been reviewed. Newly discovered sources will appear here after a scheduled or manual refresh.")
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
        "## Refresh and review",
        "",
        "- GitHub Actions refreshes this report every Monday at 12:00 p.m. Eastern Time, including daylight-saving changes, and can also be started manually.",
        "- The workflow opens or updates a pull request; new candidates never increase verified counts automatically.",
        "- To verify a candidate, inspect its source, add it to [`sources.json`](sources.json), and preserve its `discovery_provider` field. The next refresh recalculates all totals and keeps its discovery-review history.",
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

    existing_payload = load_json(candidates_path, {"candidates": []})
    existing = existing_payload.get("candidates", [])
    discovered: list[dict[str, Any]] = []
    warnings: list[str] = []
    if args.discover:
        github_results, github_warnings = discover_github(args.max_results_per_query)
        discovered.extend(github_results)
        warnings.extend(github_warnings)
        if not args.skip_crossref:
            crossref_results, crossref_warnings = discover_crossref(args.max_results_per_query)
            discovered.extend(crossref_results)
            warnings.extend(crossref_warnings)
    candidates = merge_candidates(existing, discovered, verified, args.as_of, excluded)
    candidates_payload = {
        "last_refreshed": args.as_of.isoformat(),
        "description": "Unreviewed external CoSAI references; not included in verified citation totals.",
        "discovery_enabled": args.discover,
        "discovery_warnings": warnings,
        "candidates": candidates,
    }
    candidates_path.write_text(json.dumps(candidates_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path.write_text(render_report(verified, candidates, warnings, args.as_of, args.discover, excluded), encoding="utf-8")
    print(f"Verified sources: {len(verified)}")
    print(f"Verified work-level citations: {sum(len(item.get('cosai_works', [])) for item in verified)}")
    print(f"Unreviewed discovery candidates: {len(candidates)}")
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    return 1 if warnings and args.fail_on_discovery_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
