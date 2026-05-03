# COSAI TSC Meeting Planner and Tracker

This folder manages the weekly COSAI Technical Steering Committee (TSC) 
cross-industry security meetings, including agendas, action items, and 
scheduling.

> For other TSC repository content, see the [repo root](../).

---

## 🗂 How This Is Organized

| Feature | How It's Managed |
|---|---|
| Weekly meeting agendas | One Markdown file per meeting in the [`meetings/`](./meetings/) folder |
| Weekly meeting containers | GitHub Milestones (one per meeting date) |
| Agenda item suggestions | GitHub Issues using the Agenda Suggestion template |
| Action item tracking | GitHub Issues using the Action Item template |
| Cross-meeting overview | [GitHub Projects Board](../../../../projects) |

---

## 📋 Quick Links
- [📁 All Meeting Files](./meetings/)
- [📅 Next Meeting: 2026-05-05](./meetings/2026-05-05.md)
- [Suggest an Agenda Item](../../../../issues/new/choose)
- [View All Open Action Items](../../../../issues?q=is%3Aopen+label%3Aaction-item)
- [View All Proposed Items](../../../../issues?q=is%3Aopen+label%3Aproposed)
- [Projects Board](../../../../projects)

---

## 👥 Members
All members have Write access to this repository and can open Issues directly.

---

## 📌 Workflow

### Before the Meeting
1. Organizer creates a new meeting file in [`meetings/`](./meetings/) 
   (e.g., `meetings/2026-05-05.md`)
2. Organizer creates a matching GitHub Milestone (e.g., `2026-05-05`) 
   with the meeting date as the due date
3. Members suggest agenda items by opening an Issue using the 
   **Agenda Item Suggestion** template, assigned to that week's Milestone
4. Members link their Issue in the **Proposed Agenda Items** table 
   in the meeting file
5. Discussion happens in the Issue thread — the group debates 
   whether to include the item
6. Organizer confirms items by moving them to the **Confirmed Agenda** 
   table in the meeting file and changing the label from 
   `proposed` → `agenda-item`

### After the Meeting
7. Organizer or notes taker fills in **Meeting Notes** in the meeting file
8. Follow-up tasks are tracked by opening Issues using the 
   **Action Item** template, assigned to the responsible person
9. Action Item Issues are linked in the **Action Items** table 
   in the meeting file

---

## 🏷 Issue Labels

| Label | Meaning |
|---|---|
| `proposed` | Agenda item suggested, not yet confirmed |
| `agenda-item` | Confirmed on a meeting agenda |
| `action-item` | Follow-up task from a meeting |
| `carry-over` | Item deferred from a prior meeting |
| `in-progress` | Action item actively being worked on |

---

## 📁 Meetings Folder Structure