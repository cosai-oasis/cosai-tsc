# Running the TSC workflow in Codex

Use Codex for transcript analysis and agenda drafting, with the native Google Drive connector for meeting-source access. Follow the format and source rules in [the agenda skill](../skills/cosai-tsc-meeting-agenda.md).

The original Python scripts remain unchanged. `process_transcript.py` and `generate_tsc_agenda.py` require their configured Claude/LiteLLM endpoint. `fetch_meeting_minutes.py` uses `gws` for Drive access. The workflow below uses Codex and the Drive connector for those steps; it does not claim that the scripts' model calls or `gws` authentication ran successfully.

## 1. Process the completed meeting transcript

Read the latest completed meeting's committed record in `tsc-meeting-minutes/YYYY-MM-DD.md`. If it has not been fetched yet, retrieve that prerequisite first. Snapshot current open Issues, their comments, and recently closed Issues, then match the transcript's follow-ups to existing trackers before proposing new ones. Treat draft minutes as draft evidence; do not infer completion, appointment approval, or publication.

Save an exact reconciliation plan outside the minutes cache. The agenda skill requires separately confirmed reconciliation. After approval, recheck affected Issues, apply only that plan, and verify each write through readback. On a rerun, skip changes already present and preserve later human edits or deletions. Never regenerate a different plan during application.

## 2. Fetch meeting minutes

Verify the GitHub identity and connected Drive account. An authenticated Drive connector with access to the source folders does not require a separate `gws` login.

Fetch the TSC and PGB GitHub sources with the original Python fetcher. Check its fetched/skipped/error counts; process exit alone does not establish completeness. Use a separate output directory for a new run, or `--skip-existing` when preserving an existing cache. That flag does not refresh files already present.

Read the folder IDs from `scripts/fetch_meeting_minutes.py`. List all 12 workstream/SIG folders and inspect relevant dated subfolders and alternative titles. Export all available notes in the agenda's 14-day window, plus the latest older record when a group has no in-window notes. Keep complete exports in `meeting_minutes/<group>/YYYY-MM-DD.md`, record canonical source URLs, and verify download sizes and hashes. This is an agenda-source refresh, not a complete Drive-history mirror.

Read each group's minutes individually, the latest two TSC records, and the latest PGB record. Review summaries, decisions, and next steps, and consult detailed notes when wording is ambiguous. Record the source dates and any gaps. A missing recent file does not prove that a meeting did not happen.

## 3. Generate, review, and publish the agenda

Refresh Issues and the roadmap, then draft `TSC Meeting Planner and Tracker/meetings/YYYY-MM-DD.md` using the skill's six sections. Keep a separate draft when preserving an existing output; replace the canonical date file when the user authorizes revision.

Route every eligible Issue exactly once, with the feature-presentation overlay taking precedence. Copy the Active Deliverables table from the current roadmap. Cite meeting sources and flag uncertain dates, presenter/owner conflicts, and draft-versus-approved distinctions.

Validate the date/time, all eligible Issues, all 12 group rows, and the exact roadmap table. When publishing is authorized, review the complete diff, commit the intended agenda/guidance changes, push the branch, and open a PR for co-chair review. Opening a PR does not mean the agenda has been merged or approved.

## Local evidence

- `meeting_minutes/` contains downloaded sources and is ignored by Git.
- `workflow_runs/` contains plans, snapshots, manifests, validation reports, and receipts and is ignored by Git. Keep these outside the minutes directories so the generator cannot mistake them for meeting notes.
- `.venv/` contains the local Python environment and is ignored by Git.
- Commit only intentional repository changes. Do not commit downloaded source caches, credentials, or local execution logs.
