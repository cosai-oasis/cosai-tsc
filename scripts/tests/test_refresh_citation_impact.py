"""Regression tests for conservative CoSAI citation reporting."""

from __future__ import annotations

import importlib.util
import io
import unittest
from datetime import date
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError


SCRIPT = Path(__file__).resolve().parents[1] / "refresh_citation_impact.py"
SPEC = importlib.util.spec_from_file_location("refresh_citation_impact", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to import {SCRIPT}")
REFRESH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REFRESH)


class CitationImpactTests(unittest.TestCase):
    def test_github_commit_and_branch_links_deduplicate(self):
        commit = "https://github.com/example/project/blob/0123456789abcdef/docs/report.md"
        branch = "https://github.com/example/project/blob/main/docs/report.md"
        self.assertEqual(REFRESH.canonical_url(commit), REFRESH.canonical_url(branch))

    def test_owner_controlled_sources_are_excluded(self):
        self.assertTrue(REFRESH.is_owner_controlled("https://www.coalitionforsecureai.org/report"))
        self.assertTrue(REFRESH.is_owner_controlled("https://github.com/cosai-oasis/cosai-tsc/blob/main/README.md", "cosai-oasis/cosai-tsc"))
        self.assertFalse(REFRESH.is_owner_controlled("https://github.com/external/project/blob/main/README.md", "external/project"))

    def test_verified_urls_are_not_added_as_pending_candidates(self):
        verified = [{"source_url": "https://github.com/example/project/blob/main/docs/report.md"}]
        discovered = [{"url": "https://github.com/example/project/blob/a1234/docs/report.md", "matched_works": ["CoSAI Risk Map"]}]
        self.assertEqual(REFRESH.merge_candidates([], discovered, verified, date(2026, 8, 9)), [])

    def test_reviewed_exclusions_do_not_reappear_as_pending_candidates(self):
        excluded = [{"source_url": "https://github.com/example/project/blob/main/docs/mirror.md"}]
        existing = [{"url": "https://github.com/example/project/blob/012345/docs/mirror.md"}]
        discovered = [{"url": "https://github.com/example/project/blob/abcdef/docs/mirror.md", "matched_works": ["CoSAI Risk Map"]}]
        self.assertEqual(REFRESH.merge_candidates(existing, discovered, [], date(2026, 8, 9), excluded), [])

    def test_repeated_candidates_merge_distinct_underlying_works(self):
        existing = [{"url": "https://github.com/example/project/blob/main/README.md", "publisher": "example/project", "title": "README.md", "matched_works": ["CoSAI Risk Map"], "first_seen": "2026-08-01"}]
        discovered = [{"url": "https://github.com/example/project/blob/a1234/README.md", "matched_works": ["Model Context Protocol (MCP) Security"]}]
        candidates = REFRESH.merge_candidates(existing, discovered, [], date(2026, 8, 9))
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["first_seen"], "2026-08-01")
        self.assertEqual(candidates[0]["last_seen"], "2026-08-09")
        self.assertEqual(candidates[0]["matched_works"], ["CoSAI Risk Map", "Model Context Protocol (MCP) Security"])

    def test_unreviewed_candidates_do_not_change_verified_totals(self):
        verified = [
            {"id": "C01", "source_url": "https://example.com/a", "cosai_works": ["CoSAI Risk Map"], "category": "Formal reference", "verification": "Directly inspected"},
            {"id": "O01", "source_url": "https://example.com/b", "cosai_works": [], "category": "Organizational mention", "verification": "Directly inspected"},
        ]
        for required in ("C02", "C04", "C08", "C09", "C05", "C10"):
            verified.append({"id": required, "source_url": f"https://example.com/{required}", "cosai_works": [], "category": "Organizational mention", "verification": "Directly inspected"})
        candidate = {"publisher": "external/project", "title": "README.md", "url": "https://github.com/external/project/blob/main/README.md", "matched_works": ["CoSAI Risk Map"]}
        report = REFRESH.render_report(verified, [candidate], [], date(2026, 8, 9), True)
        self.assertIn("**1 external publications**", report)
        self.assertIn("**1 distinct publication-to-work citations**", report)
        self.assertIn("**1 candidate references**", report)

    def test_snapshot_explains_each_metric_and_shows_last_updated_date(self):
        verified = [
            {"id": "C01", "source_url": "https://example.com/a", "cosai_works": ["CoSAI Risk Map"], "category": "Formal reference", "verification": "Directly inspected"},
            {"id": "O01", "source_url": "https://example.com/b", "cosai_works": [], "category": "Organizational mention", "verification": "Directly inspected"},
        ]
        report = REFRESH.render_report(verified, [], [], date(2026, 8, 9), False)
        self.assertIn("| Measure | Verified minimum | What this means |", report)
        self.assertIn("Those 1 documents make 1 unique connections to CoSAI works", report)
        self.assertIn("**Last updated: August 9, 2026**", report)
        self.assertIn("every Monday at **12:00 p.m. Eastern Time**", report)
        self.assertIn("| CoSAI publication or framework | Distinct citing publications | Selected external citations |", report)
        self.assertIn("## Complete CoSAI paper-to-source register", report)
        self.assertIn("[CoSAI Risk Map](https://example.com/a)", report)

    def test_review_ledger_retains_verified_pending_and_excluded_discoveries(self):
        verified = [{
            "id": "C01", "publisher": "Verified publisher", "citing_publication": "Verified paper",
            "source_url": "https://example.com/verified", "cosai_works": ["CoSAI Risk Map"],
            "category": "Formal reference", "verification": "Directly inspected", "discovery_provider": "GitHub public code search",
        }]
        candidates = [{"publisher": "Pending publisher", "title": "Pending paper", "url": "https://example.com/pending", "matched_works": ["CoSAI Risk Map"]}]
        excluded = [{"source_url": "https://github.com/example/project/blob/main/docs/mirror.md", "matched_works": ["CoSAI Risk Map"], "reason": "Copied source material."}]
        report = REFRESH.render_report(verified, candidates, [], date(2026, 8, 9), False, excluded)
        self.assertIn("Automated discovery identified **3 references**", report)
        self.assertIn("Verified — included in totals", report)
        self.assertIn("Pending human review — not counted", report)
        self.assertIn("Excluded — Copied source material.", report)

    def test_transient_search_failures_are_retried(self):
        unavailable = HTTPError("https://api.github.com/search/code", 503, "Service Unavailable", None, None)
        success = mock.MagicMock()
        success.__enter__.return_value = io.BytesIO(b'{"items": []}')
        with mock.patch.object(REFRESH, "urlopen", side_effect=[unavailable, success]) as urlopen:
            with mock.patch.object(REFRESH.time, "sleep") as sleep:
                result = REFRESH.request_json("https://api.github.com/search/code")
        self.assertEqual(result, {"items": []})
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
