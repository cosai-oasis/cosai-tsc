"""Offline regression tests for conservative, resumable citation discovery."""
from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse

SCRIPT = Path(__file__).resolve().parents[1] / "refresh_citation_impact.py"
SPEC = importlib.util.spec_from_file_location("refresh_citation_impact", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to import {SCRIPT}")
REFRESH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REFRESH)
VERIFIED = [{"id": "C01", "source_url": "https://example.com/verified", "cosai_works": ["CoSAI Risk Map"],
             "category": "Formal reference", "verification": "Directly inspected"}]
CANDIDATE = {"url": "https://github.com/external/project/blob/main/README.md", "publisher": "external/project",
             "title": "README.md", "matched_works": ["CoSAI Risk Map"], "first_seen": "2026-08-01", "last_seen": "2026-08-09"}


def response(payload=None, headers=None):
    result = io.BytesIO(json.dumps(payload if payload is not None else {"items": []}).encode())
    result.headers = headers or {}
    return result


def github_payload(incomplete=False):
    return {"incomplete_results": incomplete, "items": [{"html_url": CANDIDATE["url"], "path": "README.md",
            "repository": {"full_name": "external/project", "private": False, "fork": False}}]}


class Clock:
    def __init__(self):
        self.now = 1000.0
        self.sleeps = []

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


class ClockTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        for name, replacement in (("time", self.clock.time), ("monotonic", self.clock.time), ("sleep", self.clock.sleep)):
            patch = mock.patch.object(REFRESH.time, name, side_effect=replacement)
            patch.start()
            self.addCleanup(patch.stop)
        patch = mock.patch.object(REFRESH, "print")
        self.log = patch.start()
        self.addCleanup(patch.stop)


class CitationImpactTests(unittest.TestCase):
    def test_github_refs_deduplicate_and_owner_sources_are_excluded(self):
        self.assertEqual(REFRESH.canonical_url("https://github.com/example/project/blob/012345/docs/report.md"),
                         REFRESH.canonical_url("https://github.com/example/project/blob/main/docs/report.md"))
        self.assertTrue(REFRESH.is_owner_controlled("https://www.coalitionforsecureai.org/report"))
        self.assertTrue(REFRESH.is_owner_controlled("https://github.com/cosai-oasis/repo", "cosai-oasis/repo"))
        self.assertTrue(REFRESH.is_owner_controlled("https://github.com/project-codeguard/rules", "project-codeguard/rules"))
        self.assertFalse(REFRESH.is_owner_controlled("https://github.com/external/project", "external/project"))

    def test_verified_and_excluded_urls_do_not_reappear(self):
        url = "https://github.com/example/project/blob/main/docs/report.md"
        candidate = {**CANDIDATE, "url": url.replace("/main/", "/abcdef/")}
        for verified, excluded in (([{"source_url": url}], []), ([], [{"source_url": url}])):
            self.assertEqual(REFRESH.merge_candidates([candidate], [candidate], verified, date(2026, 10, 5), excluded), [])

    def test_repeated_candidates_merge_works_preserving_first_seen(self):
        discovered = {**CANDIDATE, "matched_works": ["Model Context Protocol (MCP) Security"]}
        candidates = REFRESH.merge_candidates([{**CANDIDATE}], [discovered], [], date(2026, 10, 5))
        self.assertEqual(candidates[0]["first_seen"], "2026-08-01")
        self.assertEqual(candidates[0]["last_seen"], "2026-10-05")
        self.assertEqual(len(candidates[0]["matched_works"]), 2)

    def test_uncertain_findings_visible_but_not_counted_as_verified(self):
        report = REFRESH.render_report(VERIFIED, [CANDIDATE], [], date(2026, 10, 5), True)
        self.assertIn("| Publications citing CoSAI work | **1** |", report)
        self.assertIn("| Total citations | **1** |", report)
        self.assertIn("| Unverified / uncertain findings | **1** |", report)
        self.assertIn(REFRESH.AUTOMATED_REPORT_URL, report)
        self.assertIn("do not require review before publication", report)
        self.assertIn("a successful manual publication does not establish that the scheduled workflow is active", report)
        self.assertIn(REFRESH.UNVERIFIED_STATUS, report)

    def test_report_optional_fields_metrics_and_partial_freshness(self):
        verified = VERIFIED + [{"id": "O01", "source_url": "https://example.com/org", "cosai_works": [],
                                "category": "Organizational mention", "verification": "Directly inspected"}]
        metadata = {"discovery_status": "partial", "last_attempted": "2026-10-05T16:00:00Z", "last_completed": None,
                    "query_coverage": {"completed": 3, "total": 14}}
        report = REFRESH.render_report(verified, [], [], date(2026, 10, 5), True, discovery_metadata=metadata)
        for text in ("| Type of use | **1 formal; 0 substantive** |", "| Organization-only mentions | **1 additional; 2 total** |",
                     "**Last updated: October 5, 2026**", "Snapshot generation date, not evidence",
                     "**Discovery status: partial.**", "**3 of 14 configured queries completed**",
                     "Last fully completed query round: **not recorded**", "[CoSAI Risk Map](https://example.com/verified)"):
            self.assertIn(text, report)
        self.assertLess(report.index("## Complete CoSAI paper-to-source register"), report.index("## Methodology"))
        self.assertLess(report.index("**Discovery status: partial.**"), report.index("## Summary"))

    def test_external_labels_and_link_destinations_cannot_break_markdown(self):
        link = REFRESH.markdown_link("External\n<script>alert(1)</script>|[title]", "https://example.com/a)b<c>\\d e")
        self.assertNotIn("\n", link)
        self.assertNotIn("<script>", link)
        self.assertIn("&lt;script&gt;", link)
        self.assertIn("&#124;", link)
        self.assertIn("https://example.com/a%29b%3Cc%3E%5Cd%20e", link)

    def test_github_searches_and_publishes_explicitly_public_repositories_only(self):
        for query in REFRESH.discovery_queries(10):
            if query["provider"] == "github":
                self.assertIn("is:public", parse_qs(urlparse(query["url"]).query)["q"][0])
        for visibility in (True, None):
            payload = github_payload()
            payload["items"][0]["repository"]["private"] = visibility
            self.assertEqual(REFRESH.github_candidates(payload, "CoSAI Risk Map"), [])
        self.assertEqual(len(REFRESH.github_candidates(github_payload(), "CoSAI Risk Map")), 1)

    def test_crossref_ignores_false_positives_and_owner_material(self):
        payload = {"message": {"items": [
            {"title": ["Unrelated research"], "URL": "https://doi.org/a"},
            {"title": ["CoSAI Risk Map"], "URL": "https://doi.org/b", "publisher": "OASIS"},
            {"title": ["CoSAI Risk Map"], "URL": "https://doi.org/c", "publisher": "External publisher"}]}}
        self.assertEqual([item["url"] for item in REFRESH.crossref_candidates(payload)], ["https://doi.org/c"])


class RequestTests(ClockTests):
    def test_github_requests_and_retries_are_paced(self):
        context = REFRESH.DiscoveryContext({}, 180)
        unavailable = HTTPError(REFRESH.GITHUB_API, 503, "Unavailable", {}, None)
        times = []
        results = iter([response(), unavailable, response()])
        def open_request(*args, **kwargs):
            times.append(self.clock.now)
            result = next(results)
            if isinstance(result, Exception):
                raise result
            return result
        with mock.patch.object(REFRESH, "urlopen", side_effect=open_request):
            REFRESH.request_json(REFRESH.GITHUB_API, context=context)
            REFRESH.request_json(REFRESH.GITHUB_API, context=context)
        self.assertEqual(times, [1000, 1007, 1014])
        self.assertTrue(all(call.kwargs.get("flush") for call in self.log.call_args_list))

    def test_wait_over_sixty_seconds_works_within_global_budget(self):
        limited = HTTPError(REFRESH.GITHUB_API, 429, "Limited", {"Retry-After": "75"}, None)
        with mock.patch.object(REFRESH, "urlopen", side_effect=[limited, response()]) as request:
            self.assertEqual(REFRESH.request_json(REFRESH.GITHUB_API), {"items": []})
        self.assertEqual(request.call_count, 2)
        self.assertEqual(self.clock.sleeps, [75])

    def test_long_retry_persisted_and_respected_across_invocations(self):
        state = {}
        limited = HTTPError(REFRESH.GITHUB_API, 403, "Limited", {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "2000"}, None)
        with mock.patch.object(REFRESH, "urlopen", side_effect=limited) as request:
            with self.assertRaises(REFRESH.DiscoveryDeferred):
                REFRESH.request_json(REFRESH.GITHUB_API, context=REFRESH.DiscoveryContext(state, 180))
        self.assertEqual(request.call_count, 1)
        self.assertEqual(self.clock.sleeps, [])
        self.assertEqual(REFRESH.timestamp_seconds(state["providers"]["github"]["next_retry_at"]), 2001)
        self.clock.now = 1800
        with mock.patch.object(REFRESH, "urlopen") as request:
            with self.assertRaises(REFRESH.DiscoveryDeferred):
                REFRESH.request_json(REFRESH.GITHUB_API, context=REFRESH.DiscoveryContext(state, 180))
        request.assert_not_called()
        self.clock.now = 2001
        with mock.patch.object(REFRESH, "urlopen", return_value=response()) as request:
            REFRESH.request_json(REFRESH.GITHUB_API, context=REFRESH.DiscoveryContext(state, 180))
        request.assert_called_once()

    def test_retry_after_and_reset_both_respected_including_http_dates(self):
        for retry_after in ("20", "Thu, 01 Jan 1970 00:17:00 GMT"):
            with self.subTest(retry_after=retry_after):
                self.clock.now = 1000
                self.clock.sleeps = []
                headers = {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1010", "Retry-After": retry_after}
                limited = HTTPError(REFRESH.GITHUB_API, 429, "Limited", headers, None)
                with mock.patch.object(REFRESH, "urlopen", side_effect=[limited, response()]):
                    REFRESH.request_json(REFRESH.GITHUB_API)
                self.assertEqual(self.clock.sleeps, [20])

    def test_success_rate_limit_headers_checkpointed(self):
        state = {}
        checkpoint = mock.Mock()
        context = REFRESH.DiscoveryContext(state, 180, checkpoint)
        headers = {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1010"}
        with mock.patch.object(REFRESH, "urlopen", side_effect=[response(headers=headers), response()]):
            REFRESH.request_json(REFRESH.GITHUB_API, context=context)
            self.assertEqual(REFRESH.timestamp_seconds(state["providers"]["github"]["next_retry_at"]), 1011)
            REFRESH.request_json(REFRESH.GITHUB_API, context=context)
        self.assertEqual(self.clock.sleeps, [11])
        self.assertGreaterEqual(checkpoint.call_count, 3)

    def test_global_budget_bounds_waits_and_request_timeout(self):
        limited = HTTPError(REFRESH.GITHUB_API, 429, "Limited", {"Retry-After": "60"}, None)
        with mock.patch.object(REFRESH, "urlopen", side_effect=limited) as request:
            with self.assertRaises(REFRESH.DiscoveryDeferred):
                REFRESH.request_json(REFRESH.GITHUB_API, context=REFRESH.DiscoveryContext({}, 121))
        self.assertEqual(request.call_count, 3)
        self.assertEqual(self.clock.sleeps, [60, 60])
        self.assertEqual(request.call_args.kwargs["timeout"], 1)

    def test_transient_failures_stop_after_five_attempts(self):
        unavailable = HTTPError(REFRESH.GITHUB_API, 503, "Unavailable", {}, None)
        with mock.patch.object(REFRESH, "urlopen", side_effect=unavailable) as request:
            with self.assertRaises(REFRESH.DiscoveryDeferred):
                REFRESH.request_json(REFRESH.GITHUB_API)
        self.assertEqual(request.call_count, 5)
        self.assertEqual(self.clock.sleeps, [7, 7, 7, 8])

    def test_rate_limit_without_exhausted_header_keeps_sixty_second_minimum(self):
        headers = {"X-RateLimit-Remaining": "8", "X-RateLimit-Reset": "3700"}
        limited = HTTPError(REFRESH.GITHUB_API, 429, "Limited", headers, None)
        with mock.patch.object(REFRESH, "urlopen", side_effect=[limited, response()]):
            REFRESH.request_json(REFRESH.GITHUB_API)
        self.assertEqual(self.clock.sleeps, [60])


class CheckpointTests(ClockTests):
    def setUp(self):
        super().setUp()
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.write("sources.json", VERIFIED)
        self.write("excluded-sources.json", [])
        for name, value in (("WORKS", {"First work": ('"first"', ("first",)), "Second work": ('"second"', ("second",))}),
                            ("CROSSREF_SEARCHES", ("CoSAI",))):
            patch = mock.patch.object(REFRESH, name, value)
            patch.start()
            self.addCleanup(patch.stop)
        patch = mock.patch.object(REFRESH, "github_token", return_value="test-token")
        patch.start()
        self.addCleanup(patch.stop)

    def write(self, name, data, directory=None):
        (directory or self.directory).joinpath(name).write_text(json.dumps(data))

    def read(self, name):
        return json.loads(self.directory.joinpath(name).read_text())

    def run_refresh(self, request=None, extra=(), discover=True):
        arguments = ["--output-dir", str(self.directory), "--as-of", "2026-10-05", "--fail-on-discovery-error", *extra]
        if discover:
            arguments.append("--discover")
        with mock.patch.object(REFRESH, "request_json", side_effect=request or self.empty_payload):
            return REFRESH.main(arguments)

    def empty_payload(self, url, **kwargs):
        return {"items": [], "incomplete_results": False} if kwargs["provider"] == "github" else {"message": {"items": []}}

    def test_completed_queries_and_candidates_survive_interruption_then_resume(self):
        calls = []
        def interrupted(url, **kwargs):
            calls.append(url)
            if len(calls) == 1:
                return github_payload()
            saved = self.read("discovery-state.json")
            self.assertEqual(saved["completed_queries"], ["github:First work"])
            self.assertEqual(len(saved["candidates"]), 1)
            raise RuntimeError("simulated fatal interruption")
        with self.assertRaisesRegex(RuntimeError, "fatal interruption"):
            self.run_refresh(interrupted)
        calls.clear()
        def resumed(url, **kwargs):
            calls.append(url)
            return self.empty_payload(url, **kwargs)
        self.assertEqual(self.run_refresh(resumed), 0)
        self.assertEqual(len(calls), 2)
        payload = self.read("discovered-candidates.json")
        self.assertEqual(payload["discovery_status"], "complete")
        self.assertEqual(payload["query_coverage"]["completed"], 3)
        self.assertEqual(payload["last_completed"], REFRESH.timestamp())
        self.assertEqual(len(payload["candidates"]), 1)

    def test_incomplete_results_saves_candidates_without_completing_query(self):
        calls = []
        def partial(url, **kwargs):
            calls.append(url)
            return github_payload(True) if len(calls) == 1 else self.empty_payload(url, **kwargs)
        self.assertEqual(self.run_refresh(partial), 2)
        payload = self.read("discovered-candidates.json")
        self.assertEqual(payload["discovery_status"], "partial")
        self.assertIsNone(payload["last_completed"])
        self.assertEqual(payload["query_coverage"]["completed"], 2)
        self.assertEqual(len(payload["candidates"]), 1)
        calls.clear()
        def resumed(url, **kwargs):
            calls.append(url)
            return github_payload(False)
        self.assertEqual(self.run_refresh(resumed), 0)
        self.assertEqual(len(calls), 1)
        self.assertEqual(self.read("discovered-candidates.json")["discovery_warnings"], [])

    def test_global_budget_checkpoints_partial_progress(self):
        def use_budget(url, **kwargs):
            self.clock.now += 180
            return github_payload()
        self.assertEqual(self.run_refresh(use_budget), 2)
        payload = self.read("discovered-candidates.json")
        self.assertEqual(payload["query_coverage"]["completed"], 1)
        self.assertEqual(len(payload["candidates"]), 1)
        self.assertTrue(any("budget" in warning for warning in payload["discovery_warnings"]))

    def test_provider_failure_does_not_block_other_provider_or_erase_candidates(self):
        self.write("discovered-candidates.json", {"candidates": [CANDIDATE]})
        calls = []
        def deferred(url, **kwargs):
            calls.append(kwargs["provider"])
            if kwargs["provider"] == "github":
                raise REFRESH.DiscoveryDeferred("next retry tomorrow")
            return self.empty_payload(url, **kwargs)
        self.assertEqual(self.run_refresh(deferred), 2)
        self.assertEqual(calls, ["github", "crossref"])
        payload = self.read("discovered-candidates.json")
        self.assertEqual(payload["query_coverage"]["completed"], 1)
        self.assertEqual(len(payload["candidates"]), 1)
        self.assertIsNone(payload["last_completed"])

    def test_legacy_metadata_and_render_only_do_not_claim_discovery_completed(self):
        self.write("discovered-candidates.json", {"last_refreshed": "2026-08-09", "discovery_enabled": True,
                   "last_completed": "2026-08-09T00:00:00Z", "candidates": [CANDIDATE]})
        self.assertEqual(self.run_refresh(discover=False), 0)
        payload = self.read("discovered-candidates.json")
        self.assertEqual(payload["discovery_status"], "not_run")
        self.assertIsNone(payload["last_attempted"])
        self.assertIsNone(payload["last_completed"])
        self.assertEqual(payload["candidates"][0]["last_seen"], "2026-08-09")

    def test_resume_is_data_only_with_current_verification_and_exclusions(self):
        resume = self.directory / "resume"
        resume.mkdir()
        self.write("discovered-candidates.json", {"candidates": [CANDIDATE, {**CANDIDATE, "url": VERIFIED[0]["source_url"]},
                   {**CANDIDATE, "url": "https://example.com/excluded"}]}, resume)
        self.write("sources.json", [{"id": "not-authoritative"}], resume)
        self.write("excluded-sources.json", [], resume)
        (resume / "refresh_citation_impact.py").write_text("raise AssertionError('must never execute')")
        self.write("excluded-sources.json", [{"source_url": "https://example.com/excluded", "reason": "false positive"}])
        original = (self.directory / "sources.json").read_bytes()
        self.assertEqual(self.run_refresh(extra=("--resume-from", str(resume)), discover=False), 0)
        payload = self.read("discovered-candidates.json")
        self.assertEqual(len(payload["candidates"]), 1)
        self.assertEqual(payload["candidates"][0]["last_seen"], "2026-08-09")
        self.assertEqual((self.directory / "sources.json").read_bytes(), original)

    def test_skip_crossref_is_partial_without_advancing_last_completed(self):
        self.assertEqual(self.run_refresh(), 0)
        completed = self.read("discovered-candidates.json")["last_completed"]
        self.clock.now += 100
        self.assertEqual(self.run_refresh(extra=("--skip-crossref",)), 2)
        payload = self.read("discovered-candidates.json")
        self.assertEqual(payload["last_completed"], completed)
        self.assertNotEqual(payload["last_attempted"], completed)
        self.assertEqual(payload["query_coverage"]["completed"], 2)

    def test_changed_query_plan_resets_progress_not_cooldown(self):
        self.assertEqual(self.run_refresh(extra=("--skip-crossref",)), 2)
        state = self.read("discovery-state.json")
        state["providers"] = {"github": {"next_retry_at": REFRESH.timestamp(2000)}}
        self.write("discovery-state.json", state)
        new_state, _ = REFRESH.load_discovery_data(self.directory, None, REFRESH.discovery_queries(20))
        self.assertEqual(new_state["completed_queries"], [])
        self.assertEqual(new_state["providers"]["github"]["next_retry_at"], REFRESH.timestamp(2000))
        self.assertIsNone(new_state["last_completed"])

    def test_newer_render_does_not_override_newer_discovery_progress(self):
        self.assertEqual(self.run_refresh(extra=("--skip-crossref",)), 2)
        current = self.read("discovery-state.json")
        resume = self.directory / "resume"
        resume.mkdir()
        newer = {**current, "last_attempted": REFRESH.timestamp(1100), "updated_at": REFRESH.timestamp(1100),
                 "completed_queries": [*current["completed_queries"], "crossref:CoSAI"]}
        self.write("discovery-state.json", newer, resume)
        current["updated_at"] = REFRESH.timestamp(1200)
        self.write("discovery-state.json", current)
        selected, _ = REFRESH.load_discovery_data(self.directory, resume, REFRESH.discovery_queries(10))
        self.assertEqual(selected["last_attempted"], REFRESH.timestamp(1100))
        self.assertEqual(len(selected["completed_queries"]), 3)

    def test_invalid_state_or_response_is_fatal_not_partial(self):
        self.write("discovery-state.json", {"schema_version": 999})
        with self.assertRaises(ValueError):
            self.run_refresh()
        (self.directory / "discovery-state.json").unlink()
        with self.assertRaises(ValueError):
            self.run_refresh(lambda *args, **kwargs: {"unexpected": "response"})

    def test_invalid_cli_uses_fatal_exit_one(self):
        with self.assertRaises(SystemExit) as error:
            REFRESH.parse_args(["--does-not-exist"])
        self.assertEqual(error.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
