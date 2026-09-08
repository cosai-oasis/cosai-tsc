#!/usr/bin/env python3
"""
Process a TSC meeting transcript and update GitHub Issues to match.

Reads the Gemini-generated transcript for one meeting from
tsc-meeting-minutes/<YYYY-MM-DD>.md, asks Claude to extract what actually
happened (action items, resolutions, deferrals, decisions), then reconciles
that against the open Issues labeled `action-item` and `proposed` in
cosai-oasis/cosai-tsc:

  * resolved in the meeting   → closing comment with transcript evidence, close
  * discussed, not resolved   → comment summarizing what was said
  * deferred                  → comment noting the deferral and target meeting
  * not mentioned             → left untouched

New action items in the transcript that match no open Issue are filed as new
`action-item` Issues. Recently-closed Issues are passed to the model as
history so it does not re-propose work the committee already settled.

`--skip` drops specific Issues or proposed new items from the plan, so a
co-chair decision ("leave #48 open", "don't file that one") can be applied
without hand-editing the plan.

Nothing is written to GitHub until the full plan is printed and the user types
'yes' at the confirmation prompt. `--dry-run` prints the plan and stops.

All GitHub reads and writes go through the `gh` CLI, so the script inherits
whatever `gh auth` credentials are already configured. Individual gh failures
are logged and skipped rather than aborting the run.

Usage:
    python scripts/process_transcript.py 2026-09-01
    python scripts/process_transcript.py 2026-09-01 --dry-run

    # Leave #48 untouched, and drop proposed new items 4 and 5
    python scripts/process_transcript.py 2026-09-01 --skip 48 --skip new:4,new:5

    # Comment on #48 but never close it
    python scripts/process_transcript.py 2026-09-01 --skip close:48
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta

from anthropic import Anthropic
from dotenv import load_dotenv

# ── Configuration ────────────────────────────────────────────────────────────

REPO = "cosai-oasis/cosai-tsc"

# Transcripts live here, one file per meeting, named <YYYY-MM-DD>.md.
TRANSCRIPT_DIR = "tsc-meeting-minutes"

# Labels whose open Issues are reconciled against the transcript.
TRACKED_LABELS = ("action-item", "proposed")

# Label applied to Issues created for newly surfaced action items.
NEW_ITEM_LABEL = "action-item"

# Recently-closed Issues are shown to the model as history, so it does not
# re-propose an action item the committee already closed or explicitly
# rejected. Only closures this recent are worth the prompt space.
CLOSED_HISTORY_DAYS = 60
CLOSED_HISTORY_LIMIT = 40

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4000

# Transcripts are Gemini summaries (tens of KB), not raw transcripts, so they
# fit whole. Cap anyway so a pathologically long file cannot blow the window.
MAX_TRANSCRIPT_CHARS = 120_000


# ── Repo root ────────────────────────────────────────────────────────────────

def repo_root() -> str:
    """Return the repository root, so the script works from any directory."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fall back to the parent of scripts/.
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Transcript ───────────────────────────────────────────────────────────────

def read_transcript(root: str, iso: str) -> str:
    """Read the transcript for `iso`, exiting if it is missing or empty."""
    path = os.path.join(root, TRANSCRIPT_DIR, f"{iso}.md")
    rel = os.path.relpath(path, root)
    if not os.path.exists(path):
        print(f"❌ No transcript found at {rel}")
        print("   Run scripts/fetch_meeting_minutes.py first, or check the date.")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read().strip()

    if not text:
        print(f"❌ Transcript {rel} is empty — nothing to process.")
        sys.exit(1)

    if len(text) > MAX_TRANSCRIPT_CHARS:
        print(f"⚠️  Transcript is {len(text):,} chars — truncating to "
              f"{MAX_TRANSCRIPT_CHARS:,} for the model.")
        text = text[:MAX_TRANSCRIPT_CHARS]

    print(f"📄 Read transcript: {rel} ({len(text):,} chars)")
    return text


# ── GitHub Issues ────────────────────────────────────────────────────────────

def fetch_issues(label: str) -> list:
    """
    Fetch open Issues carrying `label` via the gh CLI.
    Returns a list of issue dicts, or [] if gh fails (with a warning).
    """
    cmd = [
        "gh", "issue", "list",
        "--repo", REPO,
        "--label", label,
        "--state", "open",
        "--limit", "100",
        "--json", "number,title,body,assignees,labels,createdAt,url",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issues = json.loads(out.stdout or "[]")
        print(f"  🔖 label '{label}': {len(issues)} open issue(s)")
        return issues
    except FileNotFoundError:
        print("⚠️  gh CLI not found — cannot read or update Issues. "
              "Install GitHub CLI (https://cli.github.com) and re-run.")
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(f"⚠️  gh issue list failed for label '{label}': "
              f"{exc.stderr.strip() or exc}")
    except json.JSONDecodeError as exc:
        print(f"⚠️  Could not parse gh output for label '{label}': {exc}")
    return []


def collect_open_issues() -> dict:
    """
    Fetch open Issues for every tracked label, de-duplicated by number.
    An Issue carrying both labels is fetched twice; keep one copy.
    """
    by_number = {}
    for label in TRACKED_LABELS:
        for issue in fetch_issues(label):
            by_number[issue["number"]] = issue
    return by_number


def fetch_closed_issues(meeting_date: date) -> list:
    """
    Fetch Issues closed within CLOSED_HISTORY_DAYS before the meeting, across
    the tracked labels. Passed to the model as history only — these are never
    modified. Returns [] if gh fails; history is a nicety, not a requirement.
    """
    cutoff = meeting_date - timedelta(days=CLOSED_HISTORY_DAYS)
    by_number = {}
    for label in TRACKED_LABELS:
        cmd = [
            "gh", "issue", "list",
            "--repo", REPO,
            "--label", label,
            "--state", "closed",
            "--limit", str(CLOSED_HISTORY_LIMIT),
            "--json", "number,title,closedAt,stateReason",
        ]
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, check=True)
            rows = json.loads(out.stdout or "[]")
        except (subprocess.CalledProcessError, json.JSONDecodeError,
                FileNotFoundError) as exc:
            print(f"⚠️  Could not fetch closed history for '{label}': {exc}")
            continue

        for row in rows:
            closed_at = (row.get("closedAt") or "")[:10]
            if not closed_at:
                continue
            try:
                closed_date = datetime.strptime(closed_at, "%Y-%m-%d").date()
            except ValueError:
                continue
            if closed_date < cutoff:
                continue
            row["closedDate"] = closed_at
            by_number[row["number"]] = row

    history = sorted(by_number.values(), key=lambda r: r["closedDate"],
                     reverse=True)
    print(f"  🗄  {len(history)} Issue(s) closed in the last "
          f"{CLOSED_HISTORY_DAYS} days (history only)")
    return history


def issue_labels(issue: dict) -> list:
    """Label names on an issue dict, as returned by gh --json labels."""
    return [lab.get("name", "") for lab in issue.get("labels") or []]


def truncate(text: str, limit: int) -> str:
    """Collapse whitespace and clip `text` to `limit` chars for prompt use."""
    flat = re.sub(r"\s+", " ", (text or "").strip())
    return flat[:limit] + ("…" if len(flat) > limit else "")


# ── Prompt ───────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are a meticulous technical program manager for the OASIS CoSAI Technical \
Steering Committee (TSC). You read meeting transcripts and reconcile them \
against the committee's GitHub Issue tracker.

Your judgments must be grounded strictly in the transcript. Never infer that \
an item was resolved, discussed, or deferred because it seems likely — say so \
only when the transcript supports it. When the transcript is silent about an \
Issue, classify it as "not_mentioned". Being conservative is correct: a missed \
update is cheap, a wrongly closed Issue is not.

Return ONLY a single JSON object, with no markdown fences and no commentary.
"""


def build_user_prompt(iso: str, transcript: str, issues: dict,
                     closed: list) -> str:
    """Build the extraction/reconciliation prompt."""
    if issues:
        issue_lines = []
        for number in sorted(issues):
            issue = issues[number]
            labels = ", ".join(issue_labels(issue)) or "none"
            assignees = ", ".join(
                a.get("login", "") for a in issue.get("assignees") or []
            ) or "unassigned"
            issue_lines.append(
                f"- Issue #{number}: {issue.get('title', '(no title)')}\n"
                f"  labels: {labels}\n"
                f"  assignees: {assignees}\n"
                f"  body: {truncate(issue.get('body'), 600)}"
            )
        issue_block = "\n".join(issue_lines)
    else:
        issue_block = "(No open Issues carrying the tracked labels.)"

    if closed:
        closed_block = "\n".join(
            f"- Issue #{row['number']} (closed {row['closedDate']}"
            + (f", {row['stateReason'].lower()}" if row.get("stateReason") else "")
            + f"): {row.get('title', '(no title)')}"
            for row in closed
        )
    else:
        closed_block = "(No recently closed Issues.)"

    return f"""\
# Task

Below is the transcript of the CoSAI TSC meeting held on {iso}, followed by \
every currently open GitHub Issue labeled `action-item` or `proposed`.

Do two things:

1. Classify each open Issue against the transcript.
2. Identify action items agreed in the meeting that no open Issue covers.

# Transcript ({iso})

{transcript}

# Open Issues

{issue_block}

# Recently closed Issues (history — do NOT propose these again)

These were already settled by the committee. Do not resurrect them as new
action items, and do not include them in "issue_updates" — they are closed.

{closed_block}

# Output format

Return one JSON object with exactly these keys:

{{
  "meeting_date": "{iso}",
  "decisions": [
    "One sentence per decision the committee actually made in this meeting."
  ],
  "issue_updates": [
    {{
      "number": 42,
      "status": "resolved" | "discussed" | "deferred" | "not_mentioned",
      "comment": "The comment to post on the Issue. Summarize what the \
transcript says about it, in 1-4 sentences. Omit or leave empty for \
not_mentioned.",
      "evidence": "A short direct quote or close paraphrase from the \
transcript supporting this classification. Required for resolved, deferred, \
and discussed.",
      "deferred_to": "For deferred items only: the meeting or timeframe it \
was deferred to, exactly as the transcript describes it. Empty otherwise."
    }}
  ],
  "new_action_items": [
    {{
      "title": "Short imperative title, under 80 characters.",
      "owner": "Name as it appears in the transcript, or empty if unstated.",
      "due_date": "YYYY-MM-DD if the transcript gives a concrete date; \
otherwise the timeframe as stated (e.g. 'in 4-6 weeks'), or empty.",
      "body": "1-4 sentences of context from the transcript, including who \
committed to it and any stated deadline."
    }}
  ]
}}

Rules:

- Include an entry in "issue_updates" for EVERY open Issue listed above, \
including ones you classify as "not_mentioned".
- "resolved" means the transcript shows the work is done, the question is \
settled, or the item was explicitly closed or rejected. A decision to NOT \
pursue something resolves the Issue.
- "deferred" means the transcript explicitly postpones it.
- "discussed" means it came up substantively but remains open.
- Do NOT propose a new action item that duplicates an open Issue above — those \
belong in "issue_updates" instead.
- Only list an action item under "new_action_items" if someone in the \
transcript committed to doing something specific.
- Do NOT propose a new action item whose only content is "open a GitHub issue \
to track X". Filing the tracking Issue IS this script's job, so such an item \
would duplicate itself. Instead, propose the underlying substantive work, or \
omit it if there is none.
- Do NOT propose anything matching a recently closed Issue above.
"""


# ── Model call ───────────────────────────────────────────────────────────────

def strip_fences(text: str) -> str:
    """Remove a ```json ... ``` wrapper if the model added one anyway."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def analyze(client: Anthropic, iso: str, transcript: str, issues: dict,
            closed: list) -> dict:
    """Send the transcript to Claude and return the parsed analysis."""
    user_prompt = build_user_prompt(iso, transcript, issues, closed)
    print(f"🤖 Sending transcript to {MODEL} (~{len(user_prompt):,} chars)...")

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except Exception as exc:
        print(f"❌ Claude request failed: {exc}")
        sys.exit(1)

    raw = "".join(
        block.text for block in response.content
        if getattr(block, "type", None) == "text"
    ).strip()

    if not raw:
        print("❌ Claude returned no text content — nothing to do.")
        sys.exit(1)

    if response.stop_reason == "max_tokens":
        print(f"❌ Response hit the {MAX_TOKENS}-token limit, so the JSON is "
              "truncated and cannot be trusted. Aborting without changes.")
        sys.exit(1)

    try:
        analysis = json.loads(strip_fences(raw))
    except json.JSONDecodeError as exc:
        print(f"❌ Could not parse Claude's response as JSON: {exc}")
        print("--- response ---")
        print(raw[:2000])
        sys.exit(1)

    if not isinstance(analysis, dict):
        print("❌ Claude returned JSON that is not an object. Aborting.")
        sys.exit(1)

    return analysis


# ── Plan ─────────────────────────────────────────────────────────────────────

# An action item whose whole content is "file an Issue to track X" would be
# satisfied by this script's own act of filing it, so creating it produces a
# self-referential ticket. The prompt asks the model to avoid these, but a
# transcript that states one explicitly will often surface it anyway, so
# filter deterministically as well.
SELF_REFERENTIAL_RE = re.compile(
    r"\b(open|create|file|raise|add)\b[^.]{0,40}?"
    r"\b(github\s+)?(issue|ticket)\b",
    re.IGNORECASE,
)


def is_self_referential(title: str) -> bool:
    """True if `title` merely asks for an Issue to be filed."""
    return bool(SELF_REFERENTIAL_RE.search(title or ""))


def parse_skips(raw_skips: list) -> dict:
    """
    Parse --skip values into a spec.

    Accepted forms, comma- or repeat-separated:
      48          → skip Issue #48 entirely (no comment, no close)
      close:48    → comment on #48 but never close it
      new:3       → drop the 3rd proposed new action item (1-based, as printed)

    Exits on an unparseable token rather than silently ignoring it — a typo'd
    skip that quietly does nothing is how an unwanted close slips through.
    """
    spec = {"issues": set(), "closes": set(), "new": set()}
    for raw in raw_skips:
        for token in str(raw).split(","):
            token = token.strip().lower()
            if not token:
                continue
            if token.startswith("new:"):
                target, kind = token[4:], "new"
            elif token.startswith("close:"):
                target, kind = token[6:], "closes"
            elif token.startswith("#"):
                target, kind = token[1:], "issues"
            else:
                target, kind = token, "issues"
            try:
                value = int(target)
            except ValueError:
                print(f"❌ Could not parse --skip value '{token}'. Use forms "
                      "like '48', 'close:48', or 'new:3'.")
                sys.exit(1)
            if value < 1:
                print(f"❌ --skip value '{token}' must be positive.")
                sys.exit(1)
            spec[kind].add(value)
    return spec


def build_plan(iso: str, analysis: dict, issues: dict,
               skips: dict = None) -> dict:
    """
    Turn the model's analysis into a concrete, validated action plan.

    Drops entries referring to Issues that are not open (the model may
    hallucinate a number), and entries missing the fields their status needs.
    """
    skips = skips or {"issues": set(), "closes": set(), "new": set()}
    plan = {"close": [], "comment": [], "create": [], "skipped": []}

    updates = analysis.get("issue_updates")
    if not isinstance(updates, list):
        updates = []

    seen = set()
    for update in updates:
        if not isinstance(update, dict):
            continue
        try:
            number = int(update.get("number"))
        except (TypeError, ValueError):
            plan["skipped"].append(f"update with unusable number: {update!r}")
            continue

        if number not in issues:
            plan["skipped"].append(
                f"#{number}: not in the open Issue set — ignored"
            )
            continue
        if number in seen:
            plan["skipped"].append(f"#{number}: duplicate update — ignored")
            continue
        seen.add(number)

        if number in skips["issues"]:
            plan["skipped"].append(f"#{number}: excluded by --skip")
            continue

        status = (update.get("status") or "").strip().lower()
        comment = (update.get("comment") or "").strip()
        evidence = (update.get("evidence") or "").strip()
        deferred_to = (update.get("deferred_to") or "").strip()
        title = issues[number].get("title", "(no title)")

        if status == "not_mentioned":
            continue

        if status not in ("resolved", "discussed", "deferred"):
            plan["skipped"].append(f"#{number}: unknown status '{status}'")
            continue

        if not comment:
            plan["skipped"].append(
                f"#{number}: status '{status}' with no comment text"
            )
            continue

        if status == "resolved" and number in skips["closes"]:
            # --skip close:N — record what was said, but leave it open.
            plan["skipped"].append(
                f"#{number}: --skip close — commenting instead of closing"
            )
            status = "discussed"

        if status == "resolved" and not evidence:
            # Never close an Issue without transcript evidence to cite.
            plan["skipped"].append(
                f"#{number}: marked resolved but gave no evidence — "
                "not closing"
            )
            continue

        body = format_comment(iso, status, comment, evidence, deferred_to)
        entry = {
            "number": number,
            "title": title,
            "status": status,
            "body": body,
            "deferred_to": deferred_to,
        }
        if status == "resolved":
            plan["close"].append(entry)
        else:
            plan["comment"].append(entry)

    new_items = analysis.get("new_action_items")
    if not isinstance(new_items, list):
        new_items = []

    for index, item in enumerate(new_items, start=1):
        if not isinstance(item, dict):
            continue
        title = (item.get("title") or "").strip()
        if not title:
            plan["skipped"].append("new action item with no title — ignored")
            continue
        if index in skips["new"]:
            plan["skipped"].append(
                f"new:{index} '{truncate(title, 60)}': excluded by --skip"
            )
            continue
        if is_self_referential(title):
            plan["skipped"].append(
                f"new:{index} '{truncate(title, 60)}': asks only for an Issue "
                "to be filed — filing it here would be self-referential"
            )
            continue
        plan["create"].append({
            "title": title,
            "owner": (item.get("owner") or "").strip(),
            "due_date": (item.get("due_date") or "").strip(),
            "body": (item.get("body") or "").strip(),
        })

    return plan


def format_comment(iso: str, status: str, comment: str, evidence: str,
                   deferred_to: str) -> str:
    """Build the Issue comment body for one update."""
    headers = {
        "resolved": f"**Resolved at the {iso} TSC meeting.**",
        "discussed": f"**Discussed at the {iso} TSC meeting.**",
        "deferred": f"**Deferred at the {iso} TSC meeting.**",
    }
    parts = [headers[status], "", comment]

    if status == "deferred" and deferred_to:
        parts += ["", f"Deferred to: {deferred_to}"]

    if evidence:
        parts += ["", "From the meeting transcript:", "", f"> {evidence}"]

    parts += [
        "",
        f"_Source: `{TRANSCRIPT_DIR}/{iso}.md` — "
        "posted by `scripts/process_transcript.py`._",
    ]
    return "\n".join(parts)


def format_new_issue_body(iso: str, item: dict) -> str:
    """Build the Issue body for a newly surfaced action item."""
    parts = [f"Action item from the {iso} CoSAI TSC meeting.", ""]
    if item["owner"]:
        parts.append(f"**Owner:** {item['owner']}")
    if item["due_date"]:
        parts.append(f"**Due:** {item['due_date']}")
    if item["owner"] or item["due_date"]:
        parts.append("")
    if item["body"]:
        parts += [item["body"], ""]
    parts.append(
        f"_Source: `{TRANSCRIPT_DIR}/{iso}.md` — "
        "created by `scripts/process_transcript.py`._"
    )
    return "\n".join(parts)


# ── Confirmation ─────────────────────────────────────────────────────────────

def print_plan(iso: str, analysis: dict, plan: dict, issue_count: int) -> None:
    """Print the full planned change set for the user to review."""
    print()
    print("=" * 72)
    print(f"PLANNED CHANGES — {REPO} — meeting {iso}")
    print("=" * 72)

    decisions = [d for d in (analysis.get("decisions") or [])
                 if isinstance(d, str) and d.strip()]
    if decisions:
        print(f"\n📌 Decisions recorded in the transcript ({len(decisions)}):")
        for decision in decisions:
            print(f"   • {decision.strip()}")

    print(f"\n🔒 CLOSE with a comment ({len(plan['close'])}):")
    if not plan["close"]:
        print("   (none)")
    for entry in plan["close"]:
        print(f"\n   #{entry['number']} — {entry['title']}")
        print(indent(entry["body"]))

    print(f"\n💬 COMMENT only, left open ({len(plan['comment'])}):")
    if not plan["comment"]:
        print("   (none)")
    for entry in plan["comment"]:
        suffix = f" → {entry['deferred_to']}" if entry["deferred_to"] else ""
        print(f"\n   #{entry['number']} [{entry['status']}{suffix}] "
              f"— {entry['title']}")
        print(indent(entry["body"]))

    print(f"\n🆕 CREATE new '{NEW_ITEM_LABEL}' Issues ({len(plan['create'])}):")
    if not plan["create"]:
        print("   (none)")
    for index, item in enumerate(plan["create"], start=1):
        print(f"\n   [new:{index}] {item['title']}")
        if item["owner"]:
            print(f"      owner: {item['owner']}")
        if item["due_date"]:
            print(f"      due:   {item['due_date']}")
        print(indent(format_new_issue_body(iso, item)))

    if plan["skipped"]:
        print(f"\n⚠️  Skipped ({len(plan['skipped'])}):")
        for note in plan["skipped"]:
            print(f"   • {note}")

    untouched = (issue_count - len(plan["close"]) - len(plan["comment"]))
    print("\n" + "-" * 72)
    print(f"Summary: {len(plan['close'])} to close, "
          f"{len(plan['comment'])} to comment on, "
          f"{len(plan['create'])} to create, "
          f"{untouched} open Issue(s) left unchanged.")
    print("To exclude anything above, re-run with --skip: '--skip 48' drops an "
          "Issue,\n'--skip close:48' comments without closing, '--skip new:3' "
          "drops a proposed item.")
    print("-" * 72)


def indent(text: str, prefix: str = "      | ") -> str:
    """Indent a multi-line block for readable plan output."""
    return "\n".join(prefix + line for line in text.splitlines())


def confirm() -> bool:
    """
    Ask for explicit confirmation. Only the literal word 'yes' proceeds.
    This step is mandatory — there is no flag that bypasses it.
    """
    print("\nThese changes will be written to GitHub and cannot be fully "
          "undone (comments can be deleted, but the edits are public).")
    try:
        answer = input("Type 'yes' to proceed, anything else to abort: ")
    except (EOFError, KeyboardInterrupt):
        print("\n🚫 No confirmation received — aborting without changes.")
        return False
    if answer.strip().lower() == "yes":
        return True
    print("🚫 Aborted — no changes made.")
    return False


# ── Execution ────────────────────────────────────────────────────────────────

def run_gh(cmd: list, what: str) -> tuple:
    """
    Run a gh command. Returns (ok, stdout). Logs and swallows failures so one
    bad Issue does not abort the rest of the run.
    """
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, out.stdout.strip()
    except FileNotFoundError:
        print(f"   ❌ {what}: gh CLI not found")
    except subprocess.CalledProcessError as exc:
        print(f"   ❌ {what}: {exc.stderr.strip() or exc}")
    return False, ""


def apply_plan(iso: str, plan: dict) -> dict:
    """Execute the plan against GitHub, tallying successes and failures."""
    tally = {
        "closed": [], "commented": [], "created": [],
        "failed": [],
    }

    for entry in plan["comment"]:
        number, what = entry["number"], f"comment on #{entry['number']}"
        print(f"💬 Commenting on #{number} ({entry['status']})...")
        ok, _ = run_gh(
            ["gh", "issue", "comment", str(number),
             "--repo", REPO, "--body", entry["body"]],
            what,
        )
        (tally["commented"] if ok else tally["failed"]).append(
            number if ok else what
        )

    for entry in plan["close"]:
        number = entry["number"]
        print(f"🔒 Closing #{number}...")
        ok, _ = run_gh(
            ["gh", "issue", "comment", str(number),
             "--repo", REPO, "--body", entry["body"]],
            f"comment on #{number}",
        )
        if not ok:
            # Don't close an Issue whose rationale comment failed to post —
            # a bare close leaves no record of why.
            print(f"   ⏭  Skipping close of #{number}: comment failed, so "
                  "the closing rationale would be lost.")
            tally["failed"].append(f"close #{number} (comment failed)")
            continue
        ok, _ = run_gh(
            ["gh", "issue", "close", str(number),
             "--repo", REPO,
             "--reason", "completed"],
            f"close #{number}",
        )
        if ok:
            tally["closed"].append(number)
        else:
            tally["failed"].append(f"close #{number}")

    for item in plan["create"]:
        print(f"🆕 Creating Issue: {item['title']}...")
        ok, out = run_gh(
            ["gh", "issue", "create",
             "--repo", REPO,
             "--title", item["title"],
             "--body", format_new_issue_body(iso, item),
             "--label", NEW_ITEM_LABEL],
            f"create '{item['title']}'",
        )
        if ok:
            tally["created"].append(out.splitlines()[-1] if out else item["title"])
        else:
            tally["failed"].append(f"create '{item['title']}'")

    return tally


def print_results(tally: dict) -> None:
    """Print what actually happened."""
    print()
    print("=" * 72)
    print("RESULTS")
    print("=" * 72)

    print(f"\n🔒 Closed ({len(tally['closed'])}): "
          + (", ".join(f"#{n}" for n in tally["closed"]) or "none"))
    print(f"💬 Commented ({len(tally['commented'])}): "
          + (", ".join(f"#{n}" for n in tally["commented"]) or "none"))
    print(f"🆕 Created ({len(tally['created'])}):"
          + ("" if tally["created"] else " none"))
    for ref in tally["created"]:
        print(f"   • {ref}")

    if tally["failed"]:
        print(f"\n❌ Failed ({len(tally['failed'])}):")
        for what in tally["failed"]:
            print(f"   • {what}")
        print("\n   These were logged and skipped. Re-run to retry, or fix "
              "them by hand.")
    else:
        print("\n✅ All planned changes applied.")


# ── CLI ──────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update GitHub Issues from a TSC meeting transcript."
    )
    parser.add_argument(
        "meeting_date",
        help="Meeting date in YYYY-MM-DD format (e.g. 2026-09-01)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the plan and exit without touching GitHub.",
    )
    parser.add_argument(
        "--skip",
        action="append",
        default=[],
        metavar="SPEC",
        help="Exclude items from the plan. Repeatable and comma-separated. "
             "'48' skips Issue #48 entirely; 'close:48' comments on it but "
             "does not close it; 'new:3' drops the 3rd proposed new action "
             "item as numbered in the plan output.",
    )
    args = parser.parse_args()
    try:
        datetime.strptime(args.meeting_date, "%Y-%m-%d")
    except ValueError:
        parser.error(
            f"Invalid date '{args.meeting_date}'. Use YYYY-MM-DD format "
            "(e.g. 2026-09-01)."
        )
    return args


def main() -> None:
    args = parse_args()
    iso = args.meeting_date
    root = repo_root()
    skips = parse_skips(args.skip)
    if any(skips.values()):
        parts = []
        if skips["issues"]:
            parts.append("issues " + ", ".join(f"#{n}" for n in sorted(skips["issues"])))
        if skips["closes"]:
            parts.append("no-close " + ", ".join(f"#{n}" for n in sorted(skips["closes"])))
        if skips["new"]:
            parts.append("new items " + ", ".join(str(n) for n in sorted(skips["new"])))
        print(f"⏭  Skipping: {'; '.join(parts)}")

    # Credentials
    load_dotenv(os.path.join(root, ".env"))
    api_key = os.environ.get("LITELLM_API_KEY")
    base_url = os.environ.get("LITELLM_BASE_URL")
    missing = [n for n, v in (("LITELLM_API_KEY", api_key),
                              ("LITELLM_BASE_URL", base_url)) if not v]
    if missing:
        print(f"❌ Missing in .env: {', '.join(missing)}")
        sys.exit(1)

    transcript = read_transcript(root, iso)

    print(f"📚 Fetching open Issues from {REPO}...")
    issues = collect_open_issues()
    print(f"  📋 {len(issues)} distinct open Issue(s) to reconcile")
    meeting_day = datetime.strptime(iso, "%Y-%m-%d").date()
    closed = fetch_closed_issues(meeting_day)

    client = Anthropic(api_key=api_key, base_url=base_url)
    analysis = analyze(client, iso, transcript, issues, closed)

    plan = build_plan(iso, analysis, issues, skips)
    print_plan(iso, analysis, plan, len(issues))

    if not (plan["close"] or plan["comment"] or plan["create"]):
        print("\n✅ Nothing to change — no Issue updates and no new action "
              "items. Done.")
        return

    if args.dry_run:
        print("\n🧪 --dry-run: stopping here. No changes made.")
        return

    if not confirm():
        sys.exit(1)

    print()
    tally = apply_plan(iso, plan)
    print_results(tally)


if __name__ == "__main__":
    main()
