# Citation report automation

The [live report](https://github.com/cosai-oasis/cosai-tsc/blob/automation/citation-impact-report/TSC%20Deliverables/citation-impact/README.md) is published on `automation/citation-impact-report`. The copy on `main` is a source snapshot, not the live publication. The original `codex/cosai-citation-impact-report` branch is not maintained by this workflow.

## Publication and uncertainty

- Scheduled runs publish report updates directly to the live branch, without a report-review PR or manual approval.
- Automatically found references are published as **unverified / uncertain**, separate from the verified citation totals. A search hit is not proof of adoption or an independently verified citation.
- Rate limits and provider outages produce a clearly labelled partial result, not a claim that no references exist or that the search completed.
- The report distinguishes generation time, the latest discovery attempt, and the last completed discovery round. A completed round covers the configured bounded GitHub and Crossref queries, not the entire web or an exhaustive citation census.
- Partial candidates and query checkpoints survive subsequent runs, including before any changes are merged to `main`. Existing reviewed exclusions and the verified source register remain authoritative.

## Running and diagnosing

The `Refresh CoSAI Citation Impact Report` workflow runs Mondays at noon in `America/New_York`, including daylight-saving changes. It can also be dispatched manually. Branch-only validation does not publish unless the explicit publication input is enabled.

Searches are paced, retry headers are respected, and a bounded discovery budget prevents silent, hour-long waits. A deferred provider records when it can be retried; a later run resumes unfinished queries. Fatal errors and failed tests prevent publication. Incomplete discovery can publish its labelled results while still reporting an unsuccessful discovery-health check.

Inspect the run summary and the `citation-impact-refresh` artifact for diagnostics. Artifact presence alone is not proof of a completed search. Check `discovery_status`, `last_attempted`, `last_completed`, and `discovery_warnings` in `discovered-candidates.json`; resumable progress lives in `discovery-state.json`.

`sources.json` and `excluded-sources.json` are never automatically rewritten by discovery. No broader token, branch-protection bypass, or repository setting change is required for routine report publication. Installing changes to the workflow on `main` still follows the repository's normal code-review rules.
