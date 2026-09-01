"""Regression tests for the CoSAI Week in Review helpers.

These cover the pure date/window logic that decides which minutes file
represents each group's "Last Met" date — the part that silently reported
"Did not meet" for every group while Drive fetching was broken.
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "generate_tsc_agenda.py"
SPEC = importlib.util.spec_from_file_location("generate_tsc_agenda", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to import {SCRIPT}")
GEN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEN)

MEETING = date(2026, 9, 1)


class ParseDateFromNameTests(unittest.TestCase):
    def test_parses_both_filename_conventions(self):
        cases = {
            "2026-08-27.md": date(2026, 8, 27),
            "WS4-20260827.md": date(2026, 8, 27),
            "WS3-CoSAI-RM-SIG-20260826.md": date(2026, 8, 26),
            "WS1-20260819.md": date(2026, 8, 19),
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                self.assertEqual(GEN.parse_date_from_name(name), expected)

    def test_undated_names_return_none(self):
        for name in ("2025.md", "Model-Signing-SIG.md", "Zero-Trust.md"):
            with self.subTest(name=name):
                self.assertIsNone(GEN.parse_date_from_name(name))

    def test_impossible_date_returns_none_rather_than_raising(self):
        # A stray 8-digit run that is not a calendar date must not abort the run.
        self.assertIsNone(GEN.parse_date_from_name("WS4-20261399.md"))


class WeekInReviewTestCase(unittest.TestCase):
    """Base class providing a temporary meeting_minutes/ tree."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "meeting_minutes").mkdir()
        self.addCleanup(self._tmp.cleanup)

    def write_minutes(self, subdir, *filenames, body="Discussion notes.\n"):
        path = self.root / "meeting_minutes" / subdir
        path.mkdir(parents=True, exist_ok=True)
        for name in filenames:
            (path / name).write_text(f"# {name}\n\n{body}", encoding="utf-8")

    def collect(self):
        return GEN.collect_week_in_review(str(self.root), MEETING)

    def by_subdir(self):
        return {row["subdir"]: row for row in self.collect()}


class CollectWeekInReviewTests(WeekInReviewTestCase):
    def test_all_eight_groups_always_present(self):
        rows = self.collect()
        self.assertEqual(len(rows), 8)
        self.assertEqual(len(GEN.WEEK_IN_REVIEW_GROUPS), 8)
        # With no files at all, every group is "Did not meet", never missing.
        self.assertTrue(all(row["last_met"] is None for row in rows))

    def test_group_order_and_labels_match_config(self):
        rows = self.collect()
        self.assertEqual(
            [r["subdir"] for r in rows],
            [s for s, _ in GEN.WEEK_IN_REVIEW_GROUPS],
        )
        self.assertEqual(
            [r["label"] for r in rows],
            [l for _, l in GEN.WEEK_IN_REVIEW_GROUPS],
        )

    def test_picks_most_recent_in_window_file(self):
        self.write_minutes("ws4", "WS4-20260813.md", "WS4-20260827.md",
                           "WS4-20260820.md")
        row = self.by_subdir()["ws4"]
        self.assertEqual(row["last_met"], "2026-08-27")
        self.assertEqual(row["source"], "WS4-20260827.md")

    def test_file_older_than_window_is_did_not_meet(self):
        # WS2 last met 2026-06-30 — far outside the 14-day window.
        self.write_minutes("ws2", "WS2-20260630.md")
        row = self.by_subdir()["ws2"]
        self.assertIsNone(row["last_met"])
        self.assertEqual(row["excerpt"], "")

    def test_file_dated_after_meeting_is_excluded(self):
        # A meeting after this agenda's date is not "since the last TSC meeting".
        self.write_minutes("ws3", "WS3-20260915.md")
        self.assertIsNone(self.by_subdir()["ws3"]["last_met"])

    def test_window_boundary_is_inclusive_at_cutoff(self):
        cutoff = MEETING - timedelta(days=GEN.WEEK_IN_REVIEW_WINDOW_DAYS)
        self.write_minutes("ws1", f"WS1-{cutoff.strftime('%Y%m%d')}.md")
        self.assertEqual(self.by_subdir()["ws1"]["last_met"], cutoff.isoformat())

    def test_day_before_cutoff_is_excluded(self):
        stale = MEETING - timedelta(days=GEN.WEEK_IN_REVIEW_WINDOW_DAYS + 1)
        self.write_minutes("ws1", f"WS1-{stale.strftime('%Y%m%d')}.md")
        self.assertIsNone(self.by_subdir()["ws1"]["last_met"])

    def test_undated_aggregate_files_are_ignored(self):
        # ws1/2025.md and topic pages carry no date and cannot be placed in the
        # window, so they must never be chosen as "Last Met".
        self.write_minutes("ws1", "2025.md", "Model-Signing-SIG.md")
        self.assertIsNone(self.by_subdir()["ws1"]["last_met"])

    def test_non_markdown_files_are_ignored(self):
        path = self.root / "meeting_minutes" / "ws4"
        path.mkdir(parents=True)
        (path / "WS4-20260827.mp4").write_bytes(b"video")
        self.assertIsNone(self.by_subdir()["ws4"]["last_met"])

    def test_excerpt_is_truncated(self):
        self.write_minutes("adlc", "2026-08-26.md", body="x" * 50_000)
        excerpt = self.by_subdir()["adlc"]["excerpt"]
        self.assertEqual(len(excerpt), GEN.WEEK_IN_REVIEW_EXCERPT_CHARS)

    def test_embedded_images_stripped_from_excerpt(self):
        self.write_minutes(
            "ws4", "WS4-20260827.md",
            body=("Real discussion.\n"
                  "[image7]: <data:image/png;base64,AAAABBBBCCCC>\n"
                  "More discussion.\n"),
        )
        excerpt = self.by_subdir()["ws4"]["excerpt"]
        self.assertNotIn("base64", excerpt)
        self.assertIn("Real discussion.", excerpt)
        self.assertIn("More discussion.", excerpt)

    def test_missing_minutes_directory_does_not_raise(self):
        empty = Path(self._tmp.name) / "nonexistent"
        rows = GEN.collect_week_in_review(str(empty), MEETING)
        self.assertEqual(len(rows), 8)
        self.assertTrue(all(r["last_met"] is None for r in rows))


class BuildWeekInReviewSectionTests(WeekInReviewTestCase):
    def test_section_renders_all_groups_and_did_not_meet(self):
        self.write_minutes("ws4", "WS4-20260827.md")
        section = GEN.build_week_in_review_section(self.collect())

        for _, label in GEN.WEEK_IN_REVIEW_GROUPS:
            with self.subTest(label=label):
                self.assertIn(label, section)
        self.assertIn("Did not meet", section)
        self.assertIn("**Last Met:** 2026-08-27", section)

    def test_section_instructs_summarizing_not_filtering(self):
        # Section 4 is the one place the TSC-relevance filter must not apply.
        section = GEN.build_week_in_review_section(self.collect())
        self.assertIn("summarize", section.lower())
        self.assertIn("all eight", section.lower())

    def test_did_not_meet_group_carries_no_source_path(self):
        section = GEN.build_week_in_review_section(self.collect())
        self.assertNotIn("**Source file:**", section)


if __name__ == "__main__":
    unittest.main()
