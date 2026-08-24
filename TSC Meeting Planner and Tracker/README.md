# COSAI TSC Meeting Planner and Tracker

This folder manages the weekly COSAI Technical Steering Committee (TSC)
meetings, including AI-generated agendas, deliverables tracking, and
meeting planning.

> For other TSC repository content, see the [repo root](../).

---

## 🗂 How This Is Organized

| Feature | How It's Managed |
|---|---|
| Weekly meeting agendas | AI-generated Markdown files in [`meetings/`](./meetings/) |
| Deliverables tracking | [`../TSC Deliverables/roadmap.md`](../TSC%20Deliverables/roadmap.md) |
| Agenda generation | `scripts/generate_tsc_agenda.py` |
| Meeting minutes fetch | `scripts/fetch_meeting_minutes.py` |
| Agenda format and rules | `skills/cosai-tsc-meeting-agenda.md` |
| GitHub Milestones | One per meeting date — tracks Issues for that meeting |
| Member agenda suggestions | GitHub Issues labeled `proposed` |
| Member deliverable proposals | GitHub Issues labeled `proposed-deliverable` |
| Action item tracking | GitHub Issues labeled `action-item` |

---

## 📋 Quick Links

- [📁 All Meeting Files](./meetings/)
- [📊 Deliverables Roadmap](../TSC%20Deliverables/roadmap.md)
- [➕ Suggest an Agenda Item](../../issues/new?template=agenda-suggestion.md)
- [➕ Propose a Deliverable](../../issues/new?template=deliverable.md)
- [🏷 View All Proposed Items](../../issues?q=is%3Aopen+label%3Aproposed)
- [🏷 View All Action Items](../../issues?q=is%3Aopen+label%3Aaction-item)
- [🏷 View All Proposed Deliverables](../../issues?q=is%3Aopen+label%3Aproposed-deliverable)

---

## 👥 Members

All TSC members have Write access to this repository and can open
Issues directly to suggest agenda items or propose deliverables.

---

## 🤖 How Agendas Are Generated

Agendas are generated using an AI script that reads from multiple
sources and produces a structured draft for co-chair review.

### What the script reads
- TSC meeting minutes from `tsc-meeting-minutes/` (last 2 meetings)
- PGB meeting minutes (last 1 meeting) — filtered for TSC-relevant items
- WS1, WS2, WS3, WS4 minutes (last 1 meeting each) — filtered for TSC-relevant items
- ADLC, Code-SIG, RM-SIG, Agent-Credentials minutes (last 1 meeting each)
- Open GitHub Issues labeled `proposed`, `action-item`, `proposed-deliverable`
- `TSC Deliverables/roadmap.md`

### How to fetch meeting minutes
```bash
# Fetch all minutes (Drive + GitHub)
python scripts/fetch_meeting_minutes.py --skip-existing

# Fetch GitHub sources only (no gws needed)
python scripts/fetch_meeting_minutes.py --github-only --skip-existing

# Fetch TSC minutes only
python scripts/fetch_meeting_minutes.py --tsc-only --skip-existing
```

### How to generate an agenda
```bash
python scripts/generate_tsc_agenda.py 2026-09-01
```

The script writes a draft to `TSC Meeting Planner and Tracker/meetings/YYYY-MM-DD.md`
for co-chair review before sharing with TSC members.

### Prerequisites
- Python 3.11.11 with dependencies from `requirements.txt`
- `.env` file with `LITELLM_API_KEY` and `LITELLM_BASE_URL`
- `gws` CLI authenticated with Google account for Drive access
- `gh` CLI authenticated for GitHub Issues access

---

## 📌 Weekly Workflow

### Before the Meeting (Monday)
1. Fetch latest meeting minutes:
   ```bash
   python scripts/fetch_meeting_minutes.py --skip-existing
   ```
2. Generate the agenda:
   ```bash
   python scripts/generate_tsc_agenda.py YYYY-MM-DD
   ```
3. Review the draft agenda in `meetings/YYYY-MM-DD.md`
4. Update the Milestone number in the agenda file
5. Commit, push, and open a PR for co-chair review
6. Merge and share the link with TSC members

### During the Meeting (Tuesday)
- Co-chairs facilitate using the agenda file as the guide
- Gemini generates meeting notes automatically

### After the Meeting
- Meeting transcript appears in `tsc-meeting-minutes/YYYY-MM-DD.md`
- Open GitHub Issues for any new action items (label: `action-item`)
- Update `TSC Deliverables/roadmap.md` with any stage changes
- The transcript link in the agenda file activates automatically

---

## 🏷 Issue Labels

| Label | Meaning |
|---|---|
| `proposed` | Member-suggested agenda item — not yet confirmed |
| `agenda-item` | Confirmed on a meeting agenda |
| `action-item` | Follow-up task from a meeting |
| `carry-over` | Item moved from a prior meeting |
| `in-progress` | Action item actively being worked on |
| `proposed-deliverable` | Member proposal for a new TSC deliverable |
| `deliverable-paper` | Position paper or point of view document |
| `deliverable-blog` | Blog post |
| `deliverable-tool` | Tool or software deliverable |
| `deliverable-presentation` | Presentation or talk |
| `deliverable-publication` | External publication or release |

---

## 📁 Meetings Folder Structure

```
meetings/
├── 2026-08-25.md
├── 2026-09-01.md
└── ...
```

Each meeting file contains:
- Meeting header (time, call link, co-chairs, notes taker)
- Administrative items with deadlines and polls
- New topics for discussion
- Review of previous action items
- Active deliverables snapshot
- Workstream and SIG updates (fallback)
- Link to meeting transcript (active after the meeting)
- Link to next meeting
