#!/usr/bin/env python3
"""
generate_meeting.py

Generates a new COSAI TSC meeting Markdown file.

Default behavior (no argument):
    When run on a Tuesday, generates the meeting file for the FOLLOWING
    Tuesday — one week ahead — so members have a full week to propose
    agenda items before the meeting.

With a date argument:
    Generates a meeting file for the specified date, regardless of
    what day it is today. Useful for generating files 6+ weeks ahead.

Usage:
    python scripts/generate_meeting.py               # next-next Tuesday
    python scripts/generate_meeting.py 2026-06-09    # specific date
"""

import os
import re
import sys
from datetime import date, timedelta


# ── Configuration ────────────────────────────────────────────────────────────
# Edit these values once and all future meeting files will use them.

MEETINGS_DIR        = os.path.join("TSC Meeting Planner and Tracker", "meetings")
README_PATH         = os.path.join("TSC Meeting Planner and Tracker", "README.md")
MEETING_TIME        = "10:00 AM PT / 1:00 PM ET"                       # e.g. "10:00 AM ET"
MEETING_LINK        = "https://meet.google.com/gsn-gysc-uyt" # your recurring call link
MILESTONE_BASE_URL  = "../../../../milestone"
# Path from the meetings/ folder up to the tsc-meeting-minutes/ folder.
# Adjust this if the folder structure changes.
TRANSCRIPT_BASE_URL = "../../tsc-meeting-minutes"


# ── Helpers ──────────────────────────────────────────────────────────────────

def next_tuesday(from_date: date) -> date:
    """Return the date of the next Tuesday strictly after from_date."""
    days_ahead = (1 - from_date.weekday()) % 7  # Tuesday = weekday 1
    if days_ahead == 0:
        days_ahead = 7                           # never return from_date itself
    return from_date + timedelta(days=days_ahead)


def tuesday_one_week_ahead() -> date:
    """
    Default auto-generation target.
    When the cron job runs on Tuesday, return the FOLLOWING Tuesday
    (i.e. today + 7 days), so members have a full week to add agenda items.
    """
    today = date.today()
    # If today is Tuesday (weekday 1), jump exactly 7 days forward.
    # If run on any other day, find next Tuesday then add 7 more days.
    if today.weekday() == 1:
        return today + timedelta(days=7)
    else:
        return next_tuesday(today) + timedelta(days=7)


def format_long_date(d: date) -> str:
    """e.g. Tuesday, May 5, 2026"""
    return d.strftime("%A, %B %-d, %Y")


def meeting_template(meeting_date: date, milestone_number: str = "?") -> str:
    """Return the full Markdown content for a meeting file."""
    iso       = meeting_date.isoformat()        # 2026-05-05
    long_date = format_long_date(meeting_date)  # Tuesday, May 5, 2026
    next_tue  = next_tuesday(meeting_date)
    next_iso  = next_tue.isoformat()

    # Note: two trailing spaces after each detail line force a Markdown line break
    return f"""# COSAI TSC Meeting — {long_date}

**Time:** {MEETING_TIME}  
**Location / Call Link:** {MEETING_LINK}  
**Milestone:** [{iso}]({MILESTONE_BASE_URL}/{milestone_number})  
**Facilitator:** Akila Srinivasan and J.R. Rao 
**Notes Taker:** Google Gemini  

---

## 📋 Proposed Agenda Items
> Members can open an Issue tagged to this meeting's Milestone to propose
> an agenda item. Link your Issue here once submitted.

| # | Issue | Topic | Proposer | Time Requested | Status |
|---|---|---|---|---|---|
| 1 | | Welcome and Introductions | Organizer | 5 min | ✅ Confirmed |
| 2 | | _Open for suggestions_ | | | |

**Status Key:** ✅ Confirmed · 🔄 Under Discussion · ❌ Deferred

---

## ✅ Confirmed Agenda

| # | Topic | Presenter | Time |
|---|---|---|---|
| 1 | Welcome and Introductions | Organizer | 5 min |

---

## 📝 Meeting Notes
> To be filled in during or after the meeting.

---

## 📄 Meeting Transcript
> ⏳ Available after the meeting: [{iso} Transcript]({TRANSCRIPT_BASE_URL}/{iso}.md)

---

## 🔁 Action Items
> Issues opened after the meeting. Link them here.

| Issue | Action Item | Owner | Due |
|---|---|---|---|
| | | | |

---

## 📎 References & Pre-Reading
-

---

## ⏭ Next Meeting
[{next_iso}](./{next_iso}.md)
"""


def update_readme(meeting_date: date) -> None:
    """Update the 'Next Meeting' quick link in README.md."""
    iso = meeting_date.isoformat()

    if not os.path.exists(README_PATH):
        print(f"  ⚠️  README not found at {README_PATH} — skipping update.")
        return

    with open(README_PATH, "r") as f:
        content = f.read()

    new_link = f"- [📅 Next Meeting: {iso}](./meetings/{iso}.md)"
    pattern  = r"- \[📅 Next Meeting:.*?\]\(.*?\)"
    updated  = re.sub(pattern, new_link, content)

    if updated == content:
        print("  ⚠️  Could not find 'Next Meeting' link in README.md — please update manually.")
    else:
        with open(README_PATH, "w") as f:
            f.write(updated)
        print(f"  ✅ README.md updated → Next Meeting: {iso}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Determine target date
    if len(sys.argv) > 1:
        try:
            meeting_date = date.fromisoformat(sys.argv[1])
        except ValueError:
            print(f"❌ Invalid date format: {sys.argv[1]}. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        meeting_date = tuesday_one_week_ahead()

    iso         = meeting_date.isoformat()
    output_path = os.path.join(MEETINGS_DIR, f"{iso}.md")

    # Ensure meetings directory exists
    os.makedirs(MEETINGS_DIR, exist_ok=True)

    # Skip silently if file already exists — prevents duplicate PRs
    if os.path.exists(output_path):
        print(f"✅ Meeting file already exists: {output_path}")
        print("   Nothing to do — skipping.")
        sys.exit(0)

    # Write meeting file
    content = meeting_template(meeting_date)
    with open(output_path, "w") as f:
        f.write(content)
    print(f"✅ Created: {output_path}")

    # Update README
    update_readme(meeting_date)

    print(f"\n📌 Next steps:")
    print(f"   1. Go to GitHub → Issues → Milestones → New Milestone")
    print(f"      Title: {iso}   Due date: {iso}")
    print(f"   2. Update the Milestone number in {output_path} if needed")
    print(f"   3. Commit and push:")
    print(f"      git add .")
    print(f"      git commit -m \"agenda: add {iso} meeting file\"")
    print(f"      git push")


if __name__ == "__main__":
    main()