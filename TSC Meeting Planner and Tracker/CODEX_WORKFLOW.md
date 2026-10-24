# Running the TSC workflow in Codex

Use Codex for transcript analysis and agenda drafting, with the connected Google Drive account for meeting-source access. This route does not require a LiteLLM key, a separate model API, or a `gws` OAuth client.

The repository's original Python scripts are unchanged: `process_transcript.py` and `generate_tsc_agenda.py` still use the configured Claude/LiteLLM endpoint when invoked directly. `fetch_meeting_minutes.py` still requires `gws` for its Drive path. The Codex route below performs the equivalent work using the same source directories and agenda rules.

## Each meeting cycle

1. Read `skills/cosai-tsc-meeting-agenda.md`, the latest two committed TSC meeting records, and the current roadmap. Establish the completed meeting date and next agenda date. Do not overwrite an existing agenda.
2. Verify the connected Drive account is the intended account and verify `gh auth status`. No Google login is needed when the connector is already authenticated and can access the source folders.
3. Fetch TSC/PGB history with `.venv/bin/python scripts/fetch_meeting_minutes.py --github-only`. Read its fetched/skipped/error counts; a successful process exit alone is insufficient.
4. Read the authoritative folder IDs in `scripts/fetch_meeting_minutes.py`. List each of the 12 workstream/SIG folders, including dated subfolders where relevant, and check alternative titles/shared documents when recent notes appear absent. Export the relevant native Docs as Markdown through the Drive connector into `meeting_minutes/<group>/YYYY-MM-DD.md`. Preserve complete exports, record source URLs, and verify downloaded sizes and SHA-256 hashes. For agenda drafting, retrieve all available notes in the 14-day window plus the most recent prior record for groups with no in-window notes. This is an agenda-source refresh, not a complete Drive-history mirror.
5. Snapshot all open Issues with bodies, labels, owners, assignees, and comments, plus recently closed Issues. Analyze the completed TSC record in Codex. Match follow-ups to existing Issues before proposing new ones. Do not infer completion, appointment approval, or publication from a proposal or draft minutes.
6. Save an exact reconciliation plan under `workflow_runs/<run-date>/`. Follow the agenda skill's explicit-confirmation rule for reconciliation. After the user approves the concrete plan, recheck that affected Issues have not changed, apply only that plan, and verify each write through GitHub readback. Save an operation receipt. Do not regenerate a different plan during application.
7. Refresh the Issue snapshot after reconciliation. Draft `TSC Meeting Planner and Tracker/meetings/YYYY-MM-DD.md` in Codex, following the agenda skill's six sections and full group names. Copy the Active Deliverables table directly from the current roadmap. Cite meeting sources. Record missing evidence as unknown rather than asserting a group did not meet.
8. Validate the meeting date/time, every eligible Issue's inclusion exactly once in its proper section, all 12 group rows, and the exact 13-row roadmap snapshot (or the current roadmap's actual row count). Check owner/presenter conflicts, draft-versus-approved wording, and source freshness. Review the local draft before publishing it.

## Local files and privacy

- `meeting_minutes/` contains source material and is ignored by Git.
- `workflow_runs/` contains snapshots, plans, manifests, validation reports, and receipts and is ignored by Git. Keep these outside the meeting-source directories so the agenda generator cannot read a receipt as meeting minutes.
- `.venv/` contains the local Python environment and is ignored by Git.
- Only agenda/guidance files and intentional repository changes should be reviewed for commit. Source downloads and credentials must not be committed.

## October 24, 2026 run

- Fresh clone: `cosai-oasis/cosai-tsc`, base commit `5d7c72aa2d4f3b8904a892826c83756b6e51d119`.
- Branch: `codex/tsc-agenda-2026-10-27`.
- GitHub account: `panda-oai`; Drive account: `panda@openai.com`.
- Transcript: October 20; draft agenda: October 27.
- Fetched 41 TSC and 10 PGB Markdown files, plus 19 complete Drive Markdown exports from all 12 configured groups.
- Approved reconciliation: nine status comments, new Issues #125 and #126, zero closures; every write read back and verified.
- Dependencies from `requirements.txt` installed in `.venv`. The pinned Python 3.11.11 executable was terminated by the local host; this run used the existing Python 3.12.12 runtime. The 82 existing tests for the three workflow scripts passed under that runtime.
- No separate `gws` installation/login or Claude/LiteLLM request was performed. The existing Drive connector and Codex supplied those parts of this run.
- Sources are current only through October 24. Refresh before the October 27 meeting. WS3's latest located main-workstream notes are October 1; the agenda flags this gap. Presenter, appointment outcome, owner-field inconsistencies, and roadmap currency require co-chair review.
