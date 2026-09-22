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
  4. Open GitHub Issues labeled `feature-presentation` — deep-dive slots. This
     is an overlay label: such Issues also carry `proposed` or `action-item`,
     and are removed from those lists so each appears in exactly one section.
     Issues labeled `deferred-indefinitely` are dropped from the backlog.
  5. TSC Deliverables/roadmap.md
  6. skills/cosai-tsc-meeting-agenda.md — used as the system prompt.
  7. Week in Review material: the most recent minutes for each workstream and
     SIG dated within WEEK_IN_REVIEW_WINDOW_DAYS of the meeting, with Last Met
     dates computed here rather than inferred by the model.

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
from datetime import date, datetime, timedelta

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

# ── CoSAI Week in Review ─────────────────────────────────────────────────────
# Section 4 of the agenda summarizes every workstream and SIG since the last TSC
# meeting. Unlike the rest of the prompt — which extracts only TSC-relevant
# items — this section needs an actual summary of each group's meeting, and it
# must list all eight groups even when a group did not meet.
#
# Group labels must match the skill's Section 4 table rows exactly, in order.
WEEK_IN_REVIEW_GROUPS = [
    ("ws1", "WS1 — Software Supply Chain Security for AI Systems"),
    ("ws2", "WS2 — Preparing Defenders for a Changing Cybersecurity Landscape"),
    ("ws3", "WS3 — AI Security Risk Governance"),
    ("ws4", "WS4 — Secure Design Patterns for Agentic Systems"),
    ("rm-sig", "CoSAI-RM SIG — Coalition for Secure AI Risk Map"),
    ("code-sig", "Code SIG — Security of AI-Assisted Code Generation"),
    ("adlc", "ADLC SIG — Security of Agent Development Lifecycle"),
    ("agent-credentials", "Agent Credentials Group"),
]

# A group's minutes count toward the Week in Review only if dated within this
# many days of the meeting date. The skill defines the window as 14 days.
WEEK_IN_REVIEW_WINDOW_DAYS = 14

# How much of each in-window file to pass for summarization. Gemini notes lead
# with a "Quick notes" digest and then repeat everything as a full transcript;
# the digest is what a summary needs, and the transcripts run to ~500 KB each,
# which would blow the context window if passed whole.
WEEK_IN_REVIEW_EXCERPT_CHARS = 12000

# Issues closed since shortly before the last TSC meeting are passed to the
# model so it can mark settled work Done — or omit it — instead of inferring
# "Carried Over" from minutes that predate the closure. Without this, an action
# item reconciled into a closed Issue reappears as an open row every week.
CLOSED_ISSUE_WINDOW_DAYS = 21

MODEL = "claude-sonnet-4-6"
# 4000 was sized before the agenda gained Section 4 CoSAI Week in Review, whose
# eight summary rows push a full agenda past that cap and truncate Section 6.
MAX_TOKENS = 8000


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


# ── CoSAI Week in Review ─────────────────────────────────────────────────────

def parse_date_from_name(name: str):
    """
    Extract a date from a minutes filename, or None if it carries no date.

    Handles both `YYYY-MM-DD.md` and `PREFIX-YYYYMMDD.md`. An impossible date
    (e.g. a stray 8-digit run that is not a calendar date) returns None rather
    than raising, so an oddly named file cannot abort the run.
    """
    match = DATE_IN_NAME.search(name)
    if not match:
        return None
    try:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None


def collect_week_in_review(root: str, meeting_date: date) -> list:
    """
    Find the most recent in-window minutes file for each Week in Review group.

    Returns one entry per group in WEEK_IN_REVIEW_GROUPS order, each a dict with
    `subdir`, `label`, `last_met` (ISO date or None) and `excerpt`. A group with
    no dated file inside the window gets last_met None, which the prompt renders
    as "Did not meet" — the skill requires all eight groups to appear either way.

    Undated files (topic-named aggregates like ws1/2025.md) are ignored: without
    a date they cannot be placed inside or outside the window.
    """
    cutoff = meeting_date - timedelta(days=WEEK_IN_REVIEW_WINDOW_DAYS)
    minutes_path = os.path.join(root, MINUTES_DIR)
    rows = []

    for subdir, label in WEEK_IN_REVIEW_GROUPS:
        subdir_path = os.path.join(minutes_path, subdir)
        best_name, best_date = None, None

        if os.path.isdir(subdir_path):
            for name in os.listdir(subdir_path):
                if not name.endswith(".md"):
                    continue
                parsed = parse_date_from_name(name)
                # Strictly after the cutoff and not in the future relative to
                # the meeting: a file dated after the meeting is not "since the
                # last TSC meeting".
                if not parsed or parsed < cutoff or parsed > meeting_date:
                    continue
                if best_date is None or parsed > best_date:
                    best_name, best_date = name, parsed

        excerpt = ""
        if best_name:
            try:
                with open(os.path.join(subdir_path, best_name), "r",
                          encoding="utf-8") as fh:
                    raw = fh.read()
                text, _ = strip_embedded_images(raw)
                excerpt = text[:WEEK_IN_REVIEW_EXCERPT_CHARS]
            except OSError as exc:
                print(f"⚠️  Could not read {subdir}/{best_name}: {exc}")
                best_date = None

        rows.append({
            "subdir": subdir,
            "label": label,
            "last_met": best_date.isoformat() if best_date else None,
            "source": best_name,
            "excerpt": excerpt,
        })

    met = sum(1 for r in rows if r["last_met"])
    print(f"  📅 Week in Review: {met}/{len(rows)} group(s) met since "
          f"{cutoff.isoformat()}")
    for row in rows:
        state = row["last_met"] or "did not meet"
        print(f"     • {row['subdir']}: {state}")
    return rows


def build_week_in_review_section(rows: list) -> str:
    """
    Build the Week in Review portion of the prompt.

    This is deliberately separate from build_minutes_section: that section says
    "do NOT summarize these meetings", which is the opposite of what Section 4
    needs. The Last Met dates are computed here rather than left to the model,
    which cannot reliably infer them from file contents.
    """
    parts = [
        "## CoSAI Week in Review source material (agenda Section 4)\n",
        "Write **Section 4 CoSAI Week in Review** from the material below.\n\n"
        "This section is an exception to the TSC-relevance filter above: here "
        "you SHOULD summarize what each group discussed, not just extract "
        "TSC-relevant items. Rules:\n"
        "- Include **all eight** groups as table rows, in the order given below, "
        "using exactly the group labels shown.\n"
        "- Use the **Last Met** value given for each group verbatim. Do not "
        "infer, adjust, or recompute it.\n"
        "- For a group marked `Did not meet`, put `Did not meet` in the Last Met "
        "column and `Did not meet` as the summary. Do not invent activity.\n"
        "- Each summary is one short paragraph: topics discussed, key decisions, "
        "and anything with direct TSC relevance.\n"
        "- Do not include timestamps, meeting times, or CEST/CET/ET references.\n"
        "- Excerpts are truncated and may end mid-sentence; summarize only what "
        "is present and never invent a conclusion to fill the gap.\n",
    ]

    for row in rows:
        parts.append(f"\n### {row['label']}\n")
        if not row["last_met"]:
            parts.append(
                "**Last Met:** Did not meet\n\n"
                "_No minutes dated within the review window. Render this row as "
                "`Did not meet`._\n"
            )
            continue
        parts.append(
            f"**Last Met:** {row['last_met']}\n"
            f"**Source file:** `{MINUTES_DIR}/{row['subdir']}/{row['source']}`\n\n"
            f"{row['excerpt']}\n"
        )

    return "\n".join(parts)


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
        "--json", "number,title,body,author,assignees,labels,createdAt,url",
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


def fetch_closed_issues(meeting_date: date) -> list:
    """
    Fetch action-item and proposed Issues closed within
    CLOSED_ISSUE_WINDOW_DAYS before `meeting_date`.

    These are context only — never agenda rows. They exist so the model can
    tell that a minutes-derived action item has since been closed, which the
    open-Issue list alone cannot convey.
    """
    cutoff = meeting_date - timedelta(days=CLOSED_ISSUE_WINDOW_DAYS)
    by_number = {}
    for label in ("action-item", "proposed"):
        cmd = [
            "gh", "issue", "list",
            "--repo", REPO,
            "--label", label,
            "--state", "closed",
            "--limit", "50",
            "--json", "number,title,closedAt,stateReason",
        ]
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, check=True)
            rows = json.loads(out.stdout or "[]")
        except (subprocess.CalledProcessError, json.JSONDecodeError,
                FileNotFoundError) as exc:
            print(f"⚠️  Could not fetch closed Issues for '{label}': {exc}")
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

    closed = sorted(by_number.values(), key=lambda r: r["closedDate"],
                    reverse=True)
    print(f"  🗄  {len(closed)} Issue(s) closed in the last "
          f"{CLOSED_ISSUE_WINDOW_DAYS} days (context only)")
    return closed


def format_closed_issues(closed: list) -> str:
    """Render closed Issues as a compact list for the prompt."""
    if not closed:
        return "_No Issues closed recently._"
    return "\n".join(
        f"- Issue #{row['number']} — closed {row['closedDate']}"
        + (f" ({row['stateReason'].lower()})" if row.get("stateReason") else "")
        + f" — {row.get('title', '(no title)')}"
        for row in closed
    )


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


def has_label(issue: dict, name: str) -> bool:
    """True if `issue` carries the label `name`."""
    return any(lbl.get("name") == name
               for lbl in issue.get("labels") or [])


def partition_feature_presentations(proposed: list, action_items: list,
                                    features: list) -> tuple:
    """
    Remove `feature-presentation` Issues from the base-label lists.

    `feature-presentation` is an overlay, never an Issue's only label: #79
    carries `proposed` too, #49 carries `action-item`. Left in both lists, each
    Issue is offered to the model twice and lands in both the Feature
    Presentations and Issues sections. The skill states the precedence rule,
    but relying on the prompt alone to de-duplicate has failed before — see
    format_issues below — so enforce it here where the outcome is deterministic.
    """
    feature_numbers = {it["number"] for it in features}
    keep = [it for it in proposed if it["number"] not in feature_numbers]
    keep_ai = [it for it in action_items if it["number"] not in feature_numbers]
    return keep, keep_ai


def drop_deferred(issues: list) -> list:
    """
    Drop Issues labeled `deferred-indefinitely` from the Issues backlog.

    Backlogged work that needs no active discussion, per the 2026-09-15 TSC
    decision. Applied only to the Issues section: a deferred Issue that also
    carries `feature-presentation` still gets its presentation slot.
    """
    return [it for it in issues if not has_label(it, "deferred-indefinitely")]


def format_issues(issues: list, label: str, meeting_date: date) -> str:
    """
    Render issues as readable Markdown for the prompt.

    The age line is emitted only for `action-item` Issues. Those are the ones
    the agenda tracks as carried-over rows needing a week count. Adding it to
    `proposed` Issues made the model render them as carried-over action items
    too, duplicating them into the action-item section when they belonged in
    New Topics only. That failure is why the `feature-presentation` overlay is
    now subtracted in code (partition_feature_presentations) rather than by
    prompt instruction alone.

    `feature-presentation` is deliberately not in the age set: a presentation
    slot is not a carried-over row, and the age line would push the model back
    toward rendering it as one.
    """
    if not issues:
        return f"_No open Issues labeled `{label}`._"

    show_age = label == "action-item"

    blocks = []
    for it in issues:
        author = (it.get("author") or {}).get("login", "unknown")
        assignees = ", ".join(a.get("login", "") for a in it.get("assignees") or []) or "unassigned"
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
                      action_items: list, feature_presentations: list,
                      closed_issues: list, roadmap: str,
                      week_in_review: list) -> str:
    iso = meeting_date.isoformat()
    long_date = meeting_date.strftime("%A, %B %d, %Y").replace(" 0", " ")

    return f"""Draft the CoSAI TSC meeting agenda for **{long_date}** (`{iso}`).

Follow the agenda template, process, and formatting rules in your system prompt
exactly. Output **only** the finished Markdown agenda — no preamble, no
commentary, and no code fences around the whole document.

Ground every agenda line in the context below. Do not invent Issue numbers,
owners, due dates, or attendees. Where a detail is genuinely unknown, leave the
cell blank or mark it `❓ Unknown` rather than guessing.

Note: Discussions in the `Agenda Suggestions` category are not included in this
run — work only from the Issues and minutes provided here.

## Header fields

This project does not use GitHub Milestones. Do **not** emit a
`**Milestone:**` line in the agenda header, and do not link to
`/milestone/...` anywhere in the document. The header runs straight from
the phone line to `**Co-chairs:**`.

---

{build_minutes_section(minutes)}

---

{build_week_in_review_section(week_in_review)}

---

## Open Issues labeled `feature-presentation` (deep-dive presentation slots)

These are the deep dives for **Section 2 Feature Presentations**, which runs
first and holds the substantive floor time. `feature-presentation` is an
**overlay label**: every one of these Issues also carries `proposed` or
`action-item`. They have already been removed from the two lists below, so each
appears in exactly one section.

Put each in **Section 2 only**. Do not also list it in Section 3 Issues, even
though its other label would otherwise place it there.

Carry the full tracking state into the row. An Issue that also carries
`action-item` keeps its owner, due date, and status — a presentation slot does
not discard accountability data. `in-progress` renders as 🔄 In Progress; a
`proposed`-only presentation is 🔄 Under Discussion.

For the Presenter column use the `## Presenter / Requester` field from the Issue
body where present; otherwise the Issue author. Reproduce that field as written,
including every name it lists.

{format_issues(feature_presentations, "feature-presentation", meeting_date)}

---

## Section 3 Issues — one consolidated backlog

Section 3 Issues is a single table with fixed columns
`| Source | Item | Owner / Proposer | Due | Status |`. Both member-suggested
topics and carry-over action items go in it, distinguished by their Status
value, not by separate tables. Source is always the first column and the item
description always the second.

It is a **fallback section reviewed offline** — no fixed time budget. Keep rows
compact.

---

## Open Issues labeled `proposed` (member-suggested agenda topics)

These are topics members have asked to put on the agenda. Use them to populate
the **Section 3 Issues** table, with the Issue author in the Owner / Proposer
column and any time estimate stated in the body.

Issues labeled `feature-presentation` have already been filtered out of this
list — do not add them back.

{format_issues(proposed, "proposed", meeting_date)}

---

## Open Issues labeled `action-item` (carry-over tasks needing a status update)

These are follow-up tasks from previous meetings. Every one of them needs a
status update in the **Section 3 Issues** table. Cross-reference each against
the minutes above: an Issue matching a minutes action item is the canonical
tracker for it — merge them into a single row rather than listing both.
Never mark an item ✅ Done without explicit evidence in the minutes or a closed
Issue.

Issues labeled `feature-presentation` have already been filtered out of this
list — do not add them back.

An Issue is the canonical tracker for its action item. When a minutes action
item is tracked by any Issue — open above, or closed in the next section — emit
the `#NN` row ONLY. Never emit a `<date> minutes` row for work an Issue already
covers, and never emit both. A `<date> minutes` row is correct only for an
action item with no Issue at all.

{format_issues(action_items, "action-item", meeting_date)}

---

## Issues closed recently (context only — NOT agenda rows)

This work is settled. Do NOT emit a row for any of these, and do NOT resurrect
the matching minutes action item as 🔄 In Progress or ⚠️ Carried Over — the
minutes predate the closure, so a minutes entry matching one of these describes
work that is already done. Omit it.

{format_closed_issues(closed_issues)}

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


# ── Section 3 de-duplication ─────────────────────────────────────────────────

# Matches a Section 3 row whose Source cell is "<YYYY-MM-DD> minutes" — an
# action item attributed to minutes rather than to an Issue.
MINUTES_ROW_RE = re.compile(r"^\|\s*\d{4}-\d{2}-\d{2}\s+minutes\s*\|")

# Words carrying no distinguishing signal when comparing an action item's text
# against an Issue title.
_STOPWORDS = frozenset("""
a an and are as at be by for from has have in into is it its of on or that the
to via with will shall should must be being been this these those
action item items issue github close closed following follow up update updates
""".split())

# Minutes describe an action ("Finalize telemetry documentation…") while Issue
# titles name the subject ("Present telemetry documentation to Workstream 4").
# The verbs differ almost every time, so they are discounted and matching rests
# on the subject nouns, which are what actually identify the work.
_WEAK_VERBS = frozenset("""
present finalize develop create open comment defer sync send share coordinate
notify prepare draft review discuss schedule organize recruit track produce
provide deliver complete confirm establish define document publish
""".split())

# Nouns appearing in nearly every TSC action item. Alone they cannot identify
# one: "meeting" matched an ODIS row against an unrelated review-template Issue
# purely on that word, so these are discounted alongside the weak verbs.
_GENERIC_NOUNS = frozenset("""
meeting meetings tsc cosai group groups next previous week weekly agenda
member members team teams work working
""".split())


def _tokens(text: str) -> set:
    """Content words of `text`, lowercased, for overlap comparison."""
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 2}


def _similar(a: str, b: str, threshold: float = 0.5) -> bool:
    """
    True if `a` and `b` look like the same action item.

    Compares subject nouns, discounting the weak verbs that differ between a
    minutes phrasing and an Issue title. Overlap is measured against the
    smaller token set so a terse Issue title still matches a verbose minutes
    row describing the same work.

    Verified against the seven duplicate rows in the 2026-09-08 draft: all
    seven match, and no Issue-sourced or genuinely distinct row does.
    """
    weak = _WEAK_VERBS | _GENERIC_NOUNS
    ta, tb = _tokens(a) - weak, _tokens(b) - weak
    if not ta or not tb:
        return False
    overlap = ta & tb
    if not overlap:
        return False
    # One shared token identifies an action item only when it is distinctive.
    # "meeting" matched an ODIS row against an unrelated review-template Issue;
    # "odis" or "telemetry" genuinely does pin down the subject. Length is a
    # crude proxy for specificity, but it separates the two cases here without
    # needing a corpus.
    if len(overlap) == 1 and len(next(iter(overlap))) < 4:
        return False
    return len(overlap) / min(len(ta), len(tb)) >= threshold


def dedupe_action_items(agenda: str, action_items: list,
                        closed_issues: list) -> tuple:
    """
    Drop Section 3 rows sourced from minutes that duplicate a tracked Issue.

    The prompt already asks the model to merge these, but that instruction does
    not hold reliably: the 2026-09-08 draft carried seven such rows, two of them
    for Issues closed the day before. Filtering here makes the outcome
    deterministic instead of advisory.

    Rows whose Source cell is an Issue reference are never touched — only
    "<date> minutes" rows, and only when their text matches an Issue title.

    Column order is load-bearing: this reads Source from cells[0] and the
    description from cells[1]. The Issues section table is specified as
    `| Source | Item | Owner / Proposer | Due | Status |` for that reason.
    Inserting a column ahead of Source, or swapping the first two, makes this
    compare the wrong cell and silently stop de-duplicating. The filter is also
    global rather than section-scoped — it matches any "<date> minutes" row
    anywhere in the document.

    Returns (agenda, dropped) where `dropped` lists one note per removed row.
    """
    titles = [(f"#{it['number']}", it.get("title", ""))
              for it in action_items]
    titles += [(f"#{it['number']} (closed {it.get('closedDate', '?')})",
                it.get("title", ""))
               for it in closed_issues]
    if not titles:
        return agenda, []

    kept, dropped = [], []
    for line in agenda.split("\n"):
        if not MINUTES_ROW_RE.match(line):
            kept.append(line)
            continue

        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        description = cells[1] if len(cells) > 1 else ""

        match = next((ref for ref, title in titles
                      if _similar(description, title)), None)
        if match:
            dropped.append(f"{cells[0]}: {description[:60]} → tracked by {match}")
        else:
            kept.append(line)

    return "\n".join(kept), dropped


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
    week_in_review = collect_week_in_review(root, meeting_date)
    proposed = fetch_issues("proposed")
    action_items = fetch_issues("action-item")
    feature_presentations = fetch_issues("feature-presentation")
    closed_issues = fetch_closed_issues(meeting_date)

    # `feature-presentation` is an overlay label, so these Issues arrive in the
    # base-label lists too. Subtract them here so each lands in exactly one
    # section, then drop backlogged items from the Issues section only.
    proposed, action_items = partition_feature_presentations(
        proposed, action_items, feature_presentations
    )
    before = len(proposed) + len(action_items)
    proposed = drop_deferred(proposed)
    action_items = drop_deferred(action_items)
    deferred_count = before - len(proposed) - len(action_items)
    if feature_presentations:
        print(f"  🎤 {len(feature_presentations)} feature presentation(s); "
              f"Issues backlog now {len(proposed)} proposed + "
              f"{len(action_items)} action-item")
    if deferred_count:
        print(f"  🗄  {deferred_count} deferred-indefinitely Issue(s) omitted "
              "from the backlog")
    roadmap = read_text(os.path.join(root, ROADMAP_PATH), "Deliverables roadmap")
    system_prompt = read_text(os.path.join(root, SKILL_PATH), "Agenda skill prompt")

    if system_prompt.startswith("_"):
        print(f"❌ The agenda skill at {SKILL_PATH} is required as the system "
              "prompt. Aborting.")
        sys.exit(1)

    user_prompt = build_user_prompt(
        meeting_date, minutes, proposed, action_items, feature_presentations,
        closed_issues, roadmap, week_in_review
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

    # Drop minutes-derived Section 3 rows that an Issue already tracks. The
    # prompt asks for this merge, but does not reliably deliver it.
    agenda, dropped = dedupe_action_items(agenda, action_items, closed_issues)
    if dropped:
        print(f"🧹 Removed {len(dropped)} duplicate action item row(s) from "
              "the Issues section:")
        for note in dropped:
            print(f"   • {note}")

    # Write
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(agenda + "\n")

    print(f"✅ Draft agenda written to: {os.path.relpath(output_path, root)}")
    print("\n📌 Next steps:")
    print("   1. Review the draft — it is a draft, not a published agenda.")
    print("   2. Confirm the call link and notes taker.")
    print("   3. Commit when the co-chairs are happy with it.")


if __name__ == "__main__":
    main()
