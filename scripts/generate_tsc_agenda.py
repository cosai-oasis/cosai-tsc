#!/usr/bin/env python3
"""
generate_tsc_agenda.py

Drafts a CoSAI TSC meeting agenda for a given meeting date by assembling
context from the repository and sending it to Claude.

Context assembled:
  1. Recent meeting minutes from each subdirectory of meeting_minutes/
     (how many per subdirectory is controlled by MEETINGS_TO_READ below).
  2. Open GitHub Issues labeled `proposed`    — member-suggested topics.
  3. Open GitHub Issues labeled `action-item` — carry-over tasks needing status.
  4. TSC Deliverables/roadmap.md
  5. skills/cosai-tsc-meeting-agenda.md — used as the system prompt.

Non-TSC minutes (PGB, WS1-WS4, ADLC, ...) are passed with instructions to
extract only TSC-relevant items rather than summarize the whole meeting.

The draft is written to:
    TSC Meeting Planner and Tracker/meetings/<YYYY-MM-DD>.md

If that file already exists the script exits cleanly without calling the API.

Usage:
    python scripts/generate_tsc_agenda.py 2026-08-25
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date

from dotenv import load_dotenv
from anthropic import Anthropic


# ── Configuration ────────────────────────────────────────────────────────────

# How many of the most recent meeting files to read from each subdirectory of
# meeting_minutes/. Keys are subdirectory names (lowercase); "default" applies
# to any subdirectory not listed here.
MEETINGS_TO_READ = {
    "tsc": 2,
    "default": 1,
}

REPO = "cosai-oasis/cosai-tsc"

MINUTES_DIR = "meeting_minutes"
ROADMAP_PATH = os.path.join("TSC Deliverables", "roadmap.md")
SKILL_PATH = os.path.join("skills", "cosai-tsc-meeting-agenda.md")
MEETINGS_OUT_DIR = os.path.join("TSC Meeting Planner and Tracker", "meetings")

# The subdirectory holding the TSC's own minutes. Everything else is treated as
# a cross-stream source and filtered for TSC relevance only.
TSC_SUBDIR = "tsc"

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4000


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
        # Fall back to the parent of scripts/
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Meeting minutes ──────────────────────────────────────────────────────────

DATE_IN_NAME = re.compile(r"(20\d{2})-?(\d{2})-?(\d{2})")

# Gemini's notes exports embed slide and whiteboard screenshots as base64 data
# URIs, one per line, e.g. `[image7]: <data:image/png;base64,iVBOR...>`. A single
# such line can run to a quarter of a megabyte. Across meeting_minutes/ they are
# 88% of all bytes (23.9 MB of files hold 2.9 MB of text) and would blow past the
# model's context limit on their own, while carrying nothing an agenda can use.
IMAGE_DATA_LINE = re.compile(r"^\[image\d+\]:\s*<data:image/", re.IGNORECASE)


def strip_embedded_images(text: str) -> tuple:
    """
    Drop base64 image-data lines from minutes text.

    Returns (cleaned_text, bytes_removed). A placeholder is left behind so the
    model can see that a visual was shared and discussed, even though the pixels
    are gone.
    """
    kept, dropped_bytes, dropped = [], 0, 0
    for line in text.splitlines(keepends=True):
        if IMAGE_DATA_LINE.match(line):
            dropped_bytes += len(line)
            dropped += 1
            continue
        kept.append(line)

    if dropped:
        kept.append(
            f"\n_[{dropped} embedded screenshot(s) omitted from this transcript "
            f"— images shared during the meeting are not included here.]_\n"
        )

    return "".join(kept), dropped_bytes


def meeting_date_from_name(subdir_path: str, name: str) -> tuple:
    """
    Build a sort key that puts the genuinely newest minutes first.

    Filenames across meeting_minutes/ follow three conventions:
      * `YYYY-MM-DD.md`            — tsc, pgb, adlc, code-sig, agent-credentials
      * `PREFIX-YYYYMMDD.md`       — ws3, ws4, rm-sig
      * topic-named, no date       — ws1, ws2

    A plain reverse filename sort only works for the first convention. It picks
    the wrong file for adlc (`Kick-off-Meeting-20260310.md` sorts above the
    dated files) and rm-sig (`...-Kickoff-20251022.md` sorts above `...-2026*`
    because "K" beats a digit). So extract the date from anywhere in the name
    instead.

    Undated files have no date to compare, so they fall back to filesystem
    mtime and sort after every dated file — a dated meeting is always a better
    "most recent minutes" answer than an undated topic page.

    Returns (has_date, date_string_or_mtime, filename) for use with
    reverse=True, so newest sorts first.
    """
    match = DATE_IN_NAME.search(name)
    if match:
        return (1, "".join(match.groups()), name)

    try:
        mtime = os.path.getmtime(os.path.join(subdir_path, name))
    except OSError:
        mtime = 0.0
    return (0, f"{mtime:020.0f}", name)


def read_recent_minutes(root: str) -> dict:
    """
    Walk each subdirectory of meeting_minutes/ and read the N most recent
    Markdown files, where N comes from MEETINGS_TO_READ.

    Returns {subdir_name: [(filename, content), ...]} with the newest first.
    Recency comes from the date embedded in the filename — see
    meeting_date_from_name for why a plain filename sort is not enough.
    """
    minutes_path = os.path.join(root, MINUTES_DIR)
    if not os.path.isdir(minutes_path):
        print(f"⚠️  No {MINUTES_DIR}/ directory found — skipping minutes.")
        return {}

    collected = {}
    for subdir in sorted(os.listdir(minutes_path)):
        subdir_path = os.path.join(minutes_path, subdir)
        if not os.path.isdir(subdir_path):
            continue

        limit = MEETINGS_TO_READ.get(subdir.lower(), MEETINGS_TO_READ["default"])
        if limit <= 0:
            continue

        files = sorted(
            (f for f in os.listdir(subdir_path) if f.endswith(".md")),
            key=lambda f: meeting_date_from_name(subdir_path, f),
            reverse=True,
        )[:limit]

        entries = []
        labels = []
        for name in files:
            try:
                with open(os.path.join(subdir_path, name), "r", encoding="utf-8") as fh:
                    raw = fh.read()
            except OSError as exc:
                print(f"⚠️  Could not read {subdir}/{name}: {exc}")
                continue

            text, dropped_bytes = strip_embedded_images(raw)
            entries.append((name, text))
            if dropped_bytes:
                labels.append(f"{name} (−{dropped_bytes // 1024} KB images)")
            else:
                labels.append(name)

        if entries:
            collected[subdir] = entries
            print(f"  📄 {subdir}: read {len(entries)} file(s) — "
                  f"{', '.join(labels)}")

    return collected


# ── GitHub milestones ────────────────────────────────────────────────────────

def fetch_milestone_number(iso: str) -> str | None:
    """
    Resolve the milestone number for the meeting date.

    Milestones in this repo are titled by meeting date (e.g. "2026-08-25"), so
    we match on title. Returns the number as a string, or None if no milestone
    exists yet for that date (the agenda then carries a placeholder).
    """
    cmd = [
        "gh", "api",
        f"repos/{REPO}/milestones?state=all&per_page=100",
        "--jq", ".[] | [(.number|tostring), .title] | @tsv",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        print("⚠️  gh CLI not found — milestone number left as a placeholder.")
        return None
    except subprocess.CalledProcessError as exc:
        print(f"⚠️  Could not list milestones: {exc.stderr.strip() or exc}")
        return None

    for line in out.stdout.splitlines():
        number, _, title = line.partition("\t")
        if title.strip() == iso:
            print(f"  🎯 milestone for {iso}: #{number}")
            return number

    print(f"  ⚠️  No milestone titled '{iso}' exists yet — the agenda will "
          "carry a placeholder for you to fill in.")
    return None


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
        "--json", "number,title,body,author,assignees,labels,milestone,createdAt,url",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issues = json.loads(out.stdout or "[]")
        print(f"  🔖 label '{label}': {len(issues)} open issue(s)")
        return issues
    except FileNotFoundError:
        print("⚠️  gh CLI not found — skipping Issues labeled "
              f"'{label}'. Install GitHub CLI to include them.")
    except subprocess.CalledProcessError as exc:
        print(f"⚠️  gh issue list failed for label '{label}': "
              f"{exc.stderr.strip() or exc}")
    except json.JSONDecodeError as exc:
        print(f"⚠️  Could not parse gh output for label '{label}': {exc}")
    return []


def issue_age(created_at: str, meeting_date: date) -> str:
    """
    Describe how long an Issue has been open, as of the meeting date.

    The agenda's formatting rules require carried-over items to state how many
    meetings/weeks they have been carried (e.g. "⚠️ Carried Over (4 weeks)").
    The model cannot derive this reliably — it only sees a couple of minutes
    files — so compute it here and hand it over explicitly. TSC meetings are
    weekly, so weeks ≈ meetings carried.
    """
    if not created_at:
        return "unknown age"
    try:
        created = date.fromisoformat(created_at[:10])
    except ValueError:
        return "unknown age"

    days = (meeting_date - created).days
    if days < 0:
        return "opened after this meeting date"
    weeks = days // 7
    if weeks < 1:
        return f"{days} day(s) old — opened {created.isoformat()}, first meeting"
    return (f"{weeks} week(s) old — opened {created.isoformat()}; carried over "
            f"roughly {weeks} weekly meeting(s)")


def format_issues(issues: list, label: str, meeting_date: date) -> str:
    """
    Render issues as readable Markdown for the prompt.

    The age line is emitted only for `action-item` Issues. Those are the ones
    the agenda tracks as carried-over rows needing a week count. Adding it to
    `proposed` Issues made the model render them as carried-over action items
    too, duplicating them into Review of Previous Action Items when they belong
    in New Topics only.
    """
    if not issues:
        return f"_No open Issues labeled `{label}`._"

    show_age = label == "action-item"

    blocks = []
    for it in issues:
        author = (it.get("author") or {}).get("login", "unknown")
        assignees = ", ".join(a.get("login", "") for a in it.get("assignees") or []) or "unassigned"
        milestone = (it.get("milestone") or {}).get("title", "none")
        labels = ", ".join(l.get("name", "") for l in it.get("labels") or [])
        body = (it.get("body") or "").strip() or "_(no body)_"

        age_line = ""
        if show_age:
            age = issue_age(it.get("createdAt", ""), meeting_date)
            age_line = (
                f"- **Age as of this meeting: {age}** — use this for the "
                f"carried-over week count; do not estimate it yourself\n"
            )

        blocks.append(
            f"### #{it.get('number')} — {it.get('title')}\n"
            f"- URL: {it.get('url')}\n"
            f"- Author (proposer): {author}\n"
            f"- Assignees: {assignees}\n"
            f"- Milestone: {milestone}\n"
            f"- Labels: {labels}\n"
            f"- Opened: {it.get('createdAt')}\n"
            f"{age_line}"
            f"\nBody:\n{body}\n"
        )
    return "\n".join(blocks)


# ── File helpers ─────────────────────────────────────────────────────────────

def read_text(path: str, description: str) -> str:
    """Read a UTF-8 text file, returning a placeholder note if unavailable."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        print(f"⚠️  Could not read {description} at {path}: {exc}")
        return f"_{description} unavailable._"


# ── Prompt assembly ──────────────────────────────────────────────────────────

def build_minutes_section(minutes: dict) -> str:
    """
    Build the minutes portion of the prompt. TSC minutes are included in full
    for detailed extraction; all other streams carry an explicit instruction to
    surface only TSC-relevant items.
    """
    parts = []

    tsc_entries = minutes.get(TSC_SUBDIR, [])
    parts.append("## TSC Meeting Minutes (most recent first)\n")
    if tsc_entries:
        parts.append(
            "These are the TSC's own minutes. Extract action items, decisions, "
            "deferred topics, and cross-stream mentions in full detail. The most "
            "recent file carries the highest-priority action items.\n"
        )
        for name, content in tsc_entries:
            parts.append(f"### meeting_minutes/{TSC_SUBDIR}/{name}\n\n{content}\n")
    else:
        parts.append("_No TSC minutes found._\n")

    other = {k: v for k, v in minutes.items() if k != TSC_SUBDIR}
    parts.append("\n## Other Workstream / Body Minutes (PGB, WS1–WS4, ADLC, etc.)\n")
    if other:
        parts.append(
            "IMPORTANT — for every file in this section, extract **only items "
            "relevant to the TSC**. Do NOT summarize these meetings. A TSC-relevant "
            "item is one that:\n"
            "- requests a TSC decision, approval, or review;\n"
            "- reports a deliverable milestone, blocker, or slip the TSC tracks;\n"
            "- escalates an issue to the TSC or asks for TSC guidance;\n"
            "- names a TSC member, co-chair, or the TSC itself as an owner;\n"
            "- creates a cross-workstream dependency the TSC must coordinate.\n\n"
            "If a file contains nothing TSC-relevant, omit it from the agenda "
            "entirely rather than inventing an update for it. Never pad the agenda "
            "with routine workstream business that does not need TSC attention.\n"
        )
        for subdir, entries in sorted(other.items()):
            for name, content in entries:
                parts.append(
                    f"### meeting_minutes/{subdir}/{name} "
                    f"(stream: {subdir.upper()} — TSC-relevant items only)\n\n{content}\n"
                )
    else:
        parts.append("_No non-TSC minutes found._\n")

    return "\n".join(parts)


def build_user_prompt(meeting_date: date, minutes: dict, proposed: list,
                      action_items: list, roadmap: str,
                      milestone_number: str | None) -> str:
    iso = meeting_date.isoformat()
    long_date = meeting_date.strftime("%A, %B %d, %Y").replace(" 0", " ")

    if milestone_number:
        milestone_line = (
            f"The GitHub milestone for this meeting is number "
            f"**{milestone_number}**. Write the Milestone header field exactly as:\n"
            f"`**Milestone:** [{iso}](../../../../milestone/{milestone_number})`"
        )
    else:
        milestone_line = (
            f"No GitHub milestone exists yet for {iso}. Write the Milestone "
            f"header field exactly as:\n"
            f"`**Milestone:** [{iso}](../../../../milestone/TBD)` — leaving the "
            f"literal `TBD` in the URL so a human can fill in the number once "
            f"the milestone is created. Do not invent a number."
        )

    return f"""Draft the CoSAI TSC meeting agenda for **{long_date}** (`{iso}`).

Follow the agenda template, process, and formatting rules in your system prompt
exactly. Output **only** the finished Markdown agenda — no preamble, no
commentary, and no code fences around the whole document.

Ground every agenda line in the context below. Do not invent Issue numbers,
owners, due dates, or attendees. Where a detail is genuinely unknown, leave the
cell blank or mark it `❓ Unknown` rather than guessing.

Note: Discussions in the `Agenda Suggestions` category are not included in this
run — work only from the Issues and minutes provided here.

## Milestone

{milestone_line}

---

{build_minutes_section(minutes)}

---

## Open Issues labeled `proposed` (member-suggested agenda topics)

These are topics members have asked to put on the agenda. Use them to populate
the **New Topics** section, with the Issue author as the proposer and any time
estimate stated in the body.

These Issues belong in **New Topics only**. Do not also list them in Review of
Previous Action Items — that section is for action items from the minutes and
Issues labeled `action-item`. A `proposed` Issue appears in exactly one section,
even if it is long-running or describes follow-up work.

{format_issues(proposed, "proposed", meeting_date)}

---

## Open Issues labeled `action-item` (carry-over tasks needing a status update)

These are follow-up tasks from previous meetings. Every one of them needs a
status update in the **Review of Previous Action Items** section. Cross-reference
each against the minutes above: an Issue matching a minutes action item is the
canonical tracker for it — merge them into a single row rather than listing both.
Never mark an item ✅ Done without explicit evidence in the minutes or a closed
Issue.

{format_issues(action_items, "action-item", meeting_date)}

---

## TSC Deliverables Roadmap (`{ROADMAP_PATH}`)

Flag any deliverable whose target date falls within 4 weeks of {iso} as needing
a status check.

{roadmap}
"""


# ── Main ─────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Draft a CoSAI TSC meeting agenda for a given meeting date."
    )
    parser.add_argument(
        "meeting_date",
        help="Meeting date in YYYY-MM-DD format (e.g. 2026-08-25).",
    )
    args = parser.parse_args()

    try:
        parsed = date.fromisoformat(args.meeting_date)
    except ValueError:
        parser.error(
            f"Invalid date '{args.meeting_date}'. Use YYYY-MM-DD format "
            "(e.g. 2026-08-25)."
        )
    return parsed


def main():
    meeting_date = parse_args()
    iso = meeting_date.isoformat()
    root = repo_root()

    output_path = os.path.join(root, MEETINGS_OUT_DIR, f"{iso}.md")

    # Exit cleanly if the agenda already exists — never overwrite a draft that
    # may already have been edited by hand.
    if os.path.exists(output_path):
        print(f"✅ Agenda already exists: {os.path.relpath(output_path, root)}")
        print("   Nothing to do — skipping.")
        sys.exit(0)

    # Credentials
    load_dotenv(os.path.join(root, ".env"))
    api_key = os.environ.get("LITELLM_API_KEY")
    base_url = os.environ.get("LITELLM_BASE_URL")
    missing = [n for n, v in (("LITELLM_API_KEY", api_key),
                              ("LITELLM_BASE_URL", base_url)) if not v]
    if missing:
        print(f"❌ Missing in .env: {', '.join(missing)}")
        sys.exit(1)

    # Gather context
    print(f"📚 Gathering context for {iso}...")
    minutes = read_recent_minutes(root)
    milestone_number = fetch_milestone_number(iso)
    proposed = fetch_issues("proposed")
    action_items = fetch_issues("action-item")
    roadmap = read_text(os.path.join(root, ROADMAP_PATH), "Deliverables roadmap")
    system_prompt = read_text(os.path.join(root, SKILL_PATH), "Agenda skill prompt")

    if system_prompt.startswith("_"):
        print(f"❌ The agenda skill at {SKILL_PATH} is required as the system "
              "prompt. Aborting.")
        sys.exit(1)

    user_prompt = build_user_prompt(
        meeting_date, minutes, proposed, action_items, roadmap, milestone_number
    )

    # Generate
    print(f"🤖 Sending context to {MODEL} (~{len(user_prompt):,} chars)...")
    client = Anthropic(api_key=api_key, base_url=base_url)
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except Exception as exc:
        print(f"❌ Claude request failed: {exc}")
        sys.exit(1)

    agenda = "".join(
        block.text for block in response.content
        if getattr(block, "type", None) == "text"
    ).strip()

    if not agenda:
        print("❌ Claude returned no text content — nothing written.")
        sys.exit(1)

    if response.stop_reason == "max_tokens":
        print(f"⚠️  Response hit the {MAX_TOKENS}-token limit — the agenda may "
              "be truncated. Review before use.")

    # Write
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(agenda + "\n")

    print(f"✅ Draft agenda written to: {os.path.relpath(output_path, root)}")
    print("\n📌 Next steps:")
    print("   1. Review the draft — it is a draft, not a published agenda.")
    if milestone_number:
        print("   2. Confirm the call link and notes taker.")
    else:
        print(f"   2. Create the '{iso}' milestone and replace the `TBD` in the "
              "Milestone link.")
    print("   3. Commit when the co-chairs are happy with it.")


if __name__ == "__main__":
    main()
