"""Regression tests for the staleness guard in fetch_meeting_minutes.py.

Three sources — WS2, WS4 and WS3 — have each had their Google Calendar event
renamed, which stops the title pattern matching. The failure is silent: no
error, no missing file, the group just looks like it stopped meeting and the
agenda reports "Did not meet". Each was caught only by querying Drive by hand.

The thresholds here are calibrated against those three real incidents, so the
tests pin that calibration rather than an arbitrary number.
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "fetch_meeting_minutes.py"
SPEC = importlib.util.spec_from_file_location("fetch_meeting_minutes", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to import {SCRIPT}")
FETCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FETCH)


class NewestMeetingDateTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, *names):
        for name in names:
            (self.dir / name).write_text("notes\n", encoding="utf-8")

    def test_parses_both_filename_conventions(self):
        self.write("2026-10-06.md", "WS4-20261008.md")
        self.assertEqual(FETCH.newest_meeting_date(self.dir), date(2026, 10, 8))

    def test_undated_files_are_ignored(self):
        # ws1/2025.md and topic pages carry no meeting date.
        self.write("2025.md", "Model-Signing-SIG.md")
        self.assertIsNone(FETCH.newest_meeting_date(self.dir))

    def test_undated_file_does_not_mask_a_dated_one(self):
        self.write("2025.md", "WS1-20260826.md")
        self.assertEqual(FETCH.newest_meeting_date(self.dir), date(2026, 8, 26))

    def test_impossible_date_is_skipped_not_raised(self):
        self.write("WS4-20261399.md")
        self.assertIsNone(FETCH.newest_meeting_date(self.dir))

    def test_missing_directory_returns_none(self):
        self.assertIsNone(FETCH.newest_meeting_date(self.dir / "nope"))

    def test_non_markdown_is_ignored(self):
        (self.dir / "WS4-20261008.mp4").write_bytes(b"video")
        self.assertIsNone(FETCH.newest_meeting_date(self.dir))


class CheckSourceStalenessTests(unittest.TestCase):
    """The guard reads real directories, so each test builds a minutes tree."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self._orig = FETCH.OUTPUT_DIR
        FETCH.OUTPUT_DIR = self.root
        self.addCleanup(lambda: setattr(FETCH, "OUTPUT_DIR", self._orig))

    def source(self, name, cadence, subdir):
        return {"name": name, "cadence_days": cadence, "subdir": subdir,
                "type": "drive"}

    def write_meeting(self, subdir, meeting_date):
        d = self.root / subdir
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{meeting_date.isoformat()}.md").write_text("x", encoding="utf-8")

    def test_fresh_source_is_not_flagged(self):
        src = self.source("WS4", 7, "ws4")
        self.write_meeting("ws4", date(2026, 10, 8))
        self.assertEqual(
            FETCH.check_source_staleness([src], today=date(2026, 10, 13)), []
        )

    def test_stale_source_is_flagged_with_its_threshold(self):
        src = self.source("WS1", 7, "ws1")
        self.write_meeting("ws1", date(2026, 8, 26))
        rows = FETCH.check_source_staleness([src], today=date(2026, 10, 13))
        self.assertEqual(len(rows), 1)
        name, newest, days_stale, threshold = rows[0]
        self.assertEqual((name, newest, days_stale), ("WS1", date(2026, 8, 26), 48))
        self.assertEqual(threshold, 14)

    def test_biweekly_group_gets_more_slack_than_weekly(self):
        weekly = self.source("Weekly", 7, "weekly")
        biweekly = self.source("Biweekly", 14, "biweekly")
        # 20 days stale: past a weekly group's 14-day threshold, inside a
        # bi-weekly group's 28-day one.
        for sub in ("weekly", "biweekly"):
            self.write_meeting(sub, date(2026, 10, 13) - timedelta(days=20))
        flagged = {
            row[0]
            for row in FETCH.check_source_staleness(
                [weekly, biweekly], today=date(2026, 10, 13)
            )
        }
        self.assertEqual(flagged, {"Weekly"})

    def test_source_without_cadence_is_skipped(self):
        src = {"name": "NoCadence", "subdir": "nc", "type": "drive"}
        self.write_meeting("nc", date(2025, 1, 1))
        self.assertEqual(
            FETCH.check_source_staleness([src], today=date(2026, 10, 13)), []
        )

    def test_source_with_no_dated_files_is_skipped(self):
        # A different problem, and already visible in the fetch output.
        src = self.source("Empty", 7, "empty")
        (self.root / "empty").mkdir()
        self.assertEqual(
            FETCH.check_source_staleness([src], today=date(2026, 10, 13)), []
        )

    def test_rows_are_ordered_most_stale_first(self):
        a = self.source("A", 7, "a")
        b = self.source("B", 7, "b")
        self.write_meeting("a", date(2026, 9, 1))
        self.write_meeting("b", date(2026, 7, 1))
        rows = FETCH.check_source_staleness([a, b], today=date(2026, 10, 13))
        self.assertEqual([row[0] for row in rows], ["B", "A"])

    def test_exactly_at_threshold_is_not_flagged(self):
        src = self.source("Weekly", 7, "w")
        self.write_meeting("w", date(2026, 10, 13) - timedelta(days=14))
        self.assertEqual(
            FETCH.check_source_staleness([src], today=date(2026, 10, 13)), []
        )


class RenameIncidentCalibrationTests(unittest.TestCase):
    """
    The three renames that actually occurred must trip the guard.

    Each pair below is (cadence, days stale when the rename was caught) taken
    from the real incidents. A 3x multiplier was tried first and would have
    missed all three — these cases exist so that regression cannot return.
    """

    INCIDENTS = [
        ("WS2", 14, 35),   # caught 2026-09-29; pattern reached only 2026-08-25
        ("WS4", 7, 18),    # caught 2026-10-05; pattern reached only 2026-09-17
        ("WS3", 14, 40),   # caught 2026-10-13; pattern reached only 2026-09-03
    ]

    def test_every_real_rename_exceeds_its_threshold(self):
        for name, cadence, days_stale in self.INCIDENTS:
            with self.subTest(source=name):
                threshold = max(
                    cadence * FETCH.STALENESS_CADENCE_MULTIPLIER,
                    FETCH.STALENESS_FLOOR_DAYS,
                )
                self.assertGreater(
                    days_stale, threshold,
                    f"{name} was {days_stale}d stale but the threshold is "
                    f"{threshold}d — this rename would go unnoticed",
                )

    def test_every_configured_source_declares_a_cadence(self):
        missing = [s["name"] for s in FETCH.SOURCES if not s.get("cadence_days")]
        self.assertEqual(missing, [], f"sources without cadence_days: {missing}")


if __name__ == "__main__":
    unittest.main()
