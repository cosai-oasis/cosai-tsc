"""Regression tests for the CoSAI Week in Review helpers.

These cover the pure date/window logic that decides which minutes file
represents each group's "Last Met" date — the part that silently reported
"Did not meet" for every group while Drive fetching was broken.
"""

from __future__ import annotations

import importlib.util
import re
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
    def test_every_group_always_present(self):
        # Pinned to the config, not a literal, so adding a group (the
        # Telemetry SIG was the ninth) does not need this test edited.
        rows = self.collect()
        self.assertEqual(len(rows), len(GEN.WEEK_IN_REVIEW_GROUPS))
        # With no files at all, every group is "Did not meet", never missing.
        self.assertTrue(all(row["last_met"] is None for row in rows))

    def test_telemetry_sig_is_its_own_group(self):
        # The Telemetry SIG is a WS2 sub-group but reports separately; it must
        # never be folded into the WS2 row.
        subdirs = [sub for sub, _ in GEN.WEEK_IN_REVIEW_GROUPS]
        self.assertIn("telemetry-sig", subdirs)
        self.assertIn("ws2", subdirs)
        rows = self.by_subdir()
        self.assertIn("telemetry-sig", rows)
        self.assertNotEqual(rows["telemetry-sig"]["label"],
                            rows["ws2"]["label"])

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
        self.assertEqual(len(rows), len(GEN.WEEK_IN_REVIEW_GROUPS))
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
        # The count must be derived from WEEK_IN_REVIEW_GROUPS, not hardcoded:
        # a stale literal told the model "all eight" while handing it 12 rows,
        # and it dropped three groups from the 2026-09-29 draft.
        self.assertRegex(
            section.lower(),
            rf"all \**{len(GEN.WEEK_IN_REVIEW_GROUPS)}\** groups",
        )

    def test_did_not_meet_group_carries_no_source_path(self):
        section = GEN.build_week_in_review_section(self.collect())
        self.assertNotIn("**Source file:**", section)


class MeetingTimeTests(unittest.TestCase):
    """
    The TSC meets at 12:00 PM ET except the second Tuesday of the month, which
    is 7:00 PM ET for Asia-Pacific (agreed 2026-09-29, closing #56 and #70).
    The time was previously hardcoded in the skill template, which is the same
    shape of defect that put the wrong weekday on the 2026-09-08 agenda.
    """

    def test_first_tuesday_is_midday(self):
        self.assertEqual(GEN.meeting_time_for(date(2026, 10, 6)),
                         GEN.MEETING_TIME_DEFAULT)

    def test_second_tuesday_is_evening(self):
        self.assertEqual(GEN.meeting_time_for(date(2026, 10, 13)),
                         GEN.MEETING_TIME_LATE)

    def test_third_and_fourth_tuesdays_are_midday(self):
        for day in (20, 27):
            with self.subTest(day=day):
                self.assertEqual(GEN.meeting_time_for(date(2026, 10, day)),
                                 GEN.MEETING_TIME_DEFAULT)

    def test_exactly_one_evening_slot_per_month(self):
        # Three weeks out of four at midday, per the agreed schedule.
        for year, month in ((2026, 10), (2026, 11), (2026, 12), (2027, 1)):
            tuesdays = [
                date(year, month, day)
                for day in range(1, 32)
                if _valid(year, month, day)
                and date(year, month, day).weekday() == 1
            ]
            late = [d for d in tuesdays
                    if GEN.meeting_time_for(d) == GEN.MEETING_TIME_LATE]
            with self.subTest(month=f"{year}-{month:02d}"):
                self.assertEqual(len(late), 1)
                self.assertEqual((late[0].day - 1) // 7 + 1, 2)

    def test_check_meeting_time_accepts_the_expected_slot(self):
        agenda = ("# CoSAI TSC Meeting\n## Tuesday, October 6, 2026\n\n"
                  f"**Time:** {GEN.MEETING_TIME_DEFAULT}  \n")
        self.assertEqual(GEN.check_meeting_time(agenda, date(2026, 10, 6)), "")

    def test_check_meeting_time_rejects_the_wrong_slot(self):
        # The stale hardcoded value the skill used to carry.
        agenda = "**Time:** 1:00 PM – 2:00 PM ET  \n"
        warning = GEN.check_meeting_time(agenda, date(2026, 10, 6))
        self.assertIn("expected", warning)
        self.assertIn("12:00 PM", warning)

    def test_check_meeting_time_rejects_midday_on_an_evening_week(self):
        agenda = f"**Time:** {GEN.MEETING_TIME_DEFAULT}  \n"
        self.assertIn("7:00 PM",
                      GEN.check_meeting_time(agenda, date(2026, 10, 13)))

    def test_check_meeting_time_reports_a_missing_header(self):
        self.assertIn("No **Time:**",
                      GEN.check_meeting_time("# Agenda\n", date(2026, 10, 6)))


def _valid(year, month, day):
    try:
        date(year, month, day)
        return True
    except ValueError:
        return False


class SkillGroupTableAgreementTests(unittest.TestCase):
    """
    WEEK_IN_REVIEW_GROUPS and the skill must list the same groups in the same
    order. The skill is the generator's system prompt, so a mismatch sends the
    model one order while the source material arrives in another — and the two
    had already drifted three ways before this test existed: the skill's
    Section 4 template was missing three groups entirely, and its group table
    ordered two pairs differently from the generator.
    """

    SKILL = Path(GEN.SKILL_PATH)

    @classmethod
    def setUpClass(cls):
        root = Path(GEN.repo_root())
        cls.text = (root / GEN.SKILL_PATH).read_text(encoding="utf-8")
        cls.labels = [label for _, label in GEN.WEEK_IN_REVIEW_GROUPS]
        cls.subdirs = [subdir for subdir, _ in GEN.WEEK_IN_REVIEW_GROUPS]

    def test_section_4_template_matches_group_order(self):
        rows = [
            line.split("|")[1].strip()
            for line in self.text.splitlines()
            if line.startswith("| ") and "<YYYY-MM-DD or Did not meet>" in line
        ]
        self.assertEqual(rows, self.labels)

    def test_section_6_update_list_matches_group_order(self):
        listed = re.findall(r"^- \*\*(.+?):\*\*$", self.text, re.MULTILINE)
        # Section 6 lists exactly the Week in Review groups, nothing else.
        self.assertEqual(listed, self.labels)

    def test_group_table_matches_subdir_order(self):
        found = [
            line.split("|")[3].strip().strip("`")
            for line in self.text.splitlines()
            if line.startswith("| ") and "meeting_minutes/" in line
        ]
        found = [
            cell.replace("meeting_minutes/", "").rstrip("/")
            for cell in found
            if cell
        ]
        self.assertEqual(found, self.subdirs)


class CheckWeekInReviewRowsTests(unittest.TestCase):
    """
    Section 4 must carry one row per group, including groups that did not meet.
    The 2026-09-29 draft silently dropped three of twelve: a missing row looks
    identical to a group that does not exist, so the omission is invisible in
    the output. The prompt asks for every row; this verifies it got them.
    """

    WEEK_IN_REVIEW = [
        {"label": "WS1 — Software Supply Chain Security for AI Systems"},
        {"label": "Trust Graph — Agent Trust Graph (WS4)"},
    ]

    def check(self, agenda):
        return GEN.check_week_in_review_rows(agenda, self.WEEK_IN_REVIEW)

    def agenda(self, rows):
        return (
            "## 3. Action Items\n\n| Source | Action Item |\n|---|---|\n\n"
            "## 4. CoSAI Week in Review\n\n"
            "| Group | Last Met | Highlights |\n|---|---|---|\n"
            + rows
            + "\n## 5. Next Steps\n"
        )

    def test_no_missing_rows_when_every_group_is_present(self):
        rows = ("| WS1 — Software Supply Chain Security for AI Systems | "
                "Did not meet | Did not meet |\n"
                "| Trust Graph — Agent Trust Graph (WS4) | 2026-09-24 | "
                "Kick-off held |\n")
        self.assertEqual(self.check(self.agenda(rows)), [])

    def test_reports_a_dropped_row(self):
        rows = ("| WS1 — Software Supply Chain Security for AI Systems | "
                "Did not meet | Did not meet |\n")
        self.assertEqual(
            self.check(self.agenda(rows)),
            ["Trust Graph — Agent Trust Graph (WS4)"],
        )

    def test_mention_outside_a_table_row_does_not_count_as_present(self):
        # A false positive this check was written to avoid: substring-matching
        # the whole section passes on prose that merely names the group.
        rows = ("| WS1 — Software Supply Chain Security for AI Systems | "
                "Did not meet | Did not meet |\n\n"
                "The Trust Graph — Agent Trust Graph (WS4) group also met.\n")
        self.assertEqual(
            self.check(self.agenda(rows)),
            ["Trust Graph — Agent Trust Graph (WS4)"],
        )

    def test_missing_section_reports_every_group(self):
        agenda = "## 3. Action Items\n\nNothing to report.\n"
        self.assertEqual(
            self.check(agenda),
            [row["label"] for row in self.WEEK_IN_REVIEW],
        )


class DedupeActionItemsTests(unittest.TestCase):
    """
    Section 3 must not list a minutes-derived action item that an Issue already
    tracks. The prompt asks the model to merge these, but the 2026-09-08 draft
    carried seven such rows — two for Issues closed the previous day — so the
    merge is enforced deterministically after generation.
    """

    OPEN_ISSUES = [
        {"number": 46,
         "title": "[ACTION] Create workstream review template for next TSC meeting"},
        {"number": 47,
         "title": "[ACTION] Develop regional meetup / community workshop proposal"},
        {"number": 49,
         "title": "[AGENDA] End of Term Review — workstream and SIG standup "
                  "ahead of co-chair transition"},
        {"number": 62,
         "title": "[ACTION] Sync with team on ODIS meeting to prepare future "
                  "agenda item"},
    ]

    CLOSED_ISSUES = [
        {"number": 45, "closedDate": "2026-09-08",
         "title": "[ACTION] Present telemetry documentation to Workstream 4"},
        {"number": 60, "closedDate": "2026-09-08",
         "title": "[ACTION] Notify WS/SIG leads to provide status updates at "
                  "next meeting"},
    ]

    HEADER = ("| Source | Action Item | Owner | Due | Status |\n"
              "|---|---|---|---|---|\n")

    def dedupe(self, rows):
        return GEN.dedupe_action_items(
            self.HEADER + rows, self.OPEN_ISSUES, self.CLOSED_ISSUES
        )

    def test_drops_row_tracked_by_an_open_issue(self):
        row = ("| 2026-09-01 minutes | Comment on regional meetup proposal and "
               "defer to PGB for discussion with OASIS | J.R. Rao | | "
               "🔄 In Progress |\n")
        out, dropped = self.dedupe(row)
        self.assertEqual(len(dropped), 1)
        self.assertIn("#47", dropped[0])
        self.assertNotIn("regional meetup", out)

    def test_drops_row_tracked_by_a_closed_issue(self):
        row = ("| 2026-08-25 minutes | Present telemetry documentation to WS4 "
               "for review and feedback | Sarah Novotny | | "
               "⚠️ Carried Over |\n")
        out, dropped = self.dedupe(row)
        self.assertEqual(len(dropped), 1)
        self.assertIn("#45", dropped[0])
        self.assertIn("closed 2026-09-08", dropped[0])

    def test_matches_across_differing_verbs(self):
        """Minutes name the action, Issue titles name the subject."""
        row = ("| 2026-09-01 minutes | Open GitHub issue to track ODIS meeting "
               "follow-up | J.R. Rao | | 🔄 In Progress |\n")
        _, dropped = self.dedupe(row)
        self.assertEqual(len(dropped), 1)
        self.assertIn("#62", dropped[0])

    def test_keeps_unrelated_minutes_rows(self):
        rows = ("| 2026-09-01 minutes | Draft the multimodal threat taxonomy "
                "outline | Klaudia Krawiecka | | 🔄 In Progress |\n"
                "| 2026-09-01 minutes | Investigate CI runner cost overruns "
                "for the RM SIG | Dalton House | | 🔄 In Progress |\n")
        out, dropped = self.dedupe(rows)
        self.assertEqual(dropped, [])
        self.assertIn("multimodal threat taxonomy", out)
        self.assertIn("CI runner cost overruns", out)

    def test_never_touches_issue_sourced_rows(self):
        """An Issue row is canonical even when its text matches another Issue."""
        row = ("| #45 | Present telemetry documentation to Workstream 4 | "
               "Sarah Novotny | | ✅ Done |\n")
        out, dropped = self.dedupe(row)
        self.assertEqual(dropped, [])
        self.assertIn("#45", out)

    def test_no_issues_leaves_agenda_untouched(self):
        agenda = self.HEADER + ("| 2026-09-01 minutes | Anything at all | A | "
                                "| 🔄 In Progress |\n")
        self.assertEqual(GEN.dedupe_action_items(agenda, [], []), (agenda, []))

    def test_preserves_non_table_content(self):
        agenda = ("## 3. Review of Previous Action Items\n\n" + self.HEADER
                  + "| 2026-09-01 minutes | Create review template for "
                    "end-of-term workstream review | Akila | | ⚠️ Carried Over |\n"
                  + "\n**Status Key:** ✅ Done\n")
        out, dropped = self.dedupe_full(agenda)
        self.assertEqual(len(dropped), 1)
        self.assertIn("## 3. Review of Previous Action Items", out)
        self.assertIn("**Status Key:**", out)
        self.assertIn("|---|---|---|---|---|", out)

    def dedupe_full(self, agenda):
        return GEN.dedupe_action_items(
            agenda, self.OPEN_ISSUES, self.CLOSED_ISSUES
        )


class SimilarityTests(unittest.TestCase):
    def test_weak_verbs_do_not_carry_a_match(self):
        """Two unrelated items sharing only a verb must not match."""
        self.assertFalse(GEN._similar(
            "Create the WS1 supply chain scenario list",
            "Create workstream review template for next TSC meeting",
        ))

    def test_subject_nouns_carry_the_match(self):
        self.assertTrue(GEN._similar(
            "Finalize telemetry documentation for WS4 and close the issue",
            "[ACTION] Present telemetry documentation to Workstream 4",
        ))

    def test_empty_text_never_matches(self):
        self.assertFalse(GEN._similar("", "anything at all"))
        self.assertFalse(GEN._similar("anything at all", ""))


def issue(number, *labels):
    """Minimal issue dict: the number plus whatever labels are named."""
    return {"number": number,
            "labels": [{"name": n} for n in labels]}


class FeaturePresentationPartitionTests(unittest.TestCase):
    """
    `feature-presentation` is an overlay label, never an Issue's only label.
    Left in the base-label lists, such an Issue is offered to the model twice
    and lands in both the Feature Presentations and Issues sections.
    """

    def test_overlay_issues_leave_the_base_lists(self):
        proposed = [issue(79, "proposed", "feature-presentation"),
                    issue(80, "proposed")]
        action_items = [issue(49, "action-item", "feature-presentation"),
                        issue(48, "action-item")]
        features = [issue(79, "proposed", "feature-presentation"),
                    issue(49, "action-item", "feature-presentation")]

        kept_p, kept_a = GEN.partition_feature_presentations(
            proposed, action_items, features)

        self.assertEqual([it["number"] for it in kept_p], [80])
        self.assertEqual([it["number"] for it in kept_a], [48])

    def test_no_features_leaves_both_lists_untouched(self):
        proposed = [issue(80, "proposed")]
        action_items = [issue(48, "action-item")]
        kept_p, kept_a = GEN.partition_feature_presentations(
            proposed, action_items, [])
        self.assertEqual(kept_p, proposed)
        self.assertEqual(kept_a, action_items)

    def test_partition_does_not_mutate_its_inputs(self):
        proposed = [issue(79, "proposed", "feature-presentation")]
        action_items = [issue(49, "action-item", "feature-presentation")]
        GEN.partition_feature_presentations(
            proposed, action_items, list(action_items) + list(proposed))
        self.assertEqual(len(proposed), 1)
        self.assertEqual(len(action_items), 1)


class DropDeferredTests(unittest.TestCase):
    """`deferred-indefinitely` Issues are omitted from the Issues backlog."""

    def test_deferred_issues_are_dropped(self):
        issues = [issue(10, "action-item"),
                  issue(11, "action-item", "deferred-indefinitely"),
                  issue(12, "proposed")]
        self.assertEqual([it["number"] for it in GEN.drop_deferred(issues)],
                         [10, 12])

    def test_in_progress_is_never_dropped(self):
        """`in-progress` means actively worked — hiding it would bury live work."""
        issues = [issue(48, "action-item", "in-progress"),
                  issue(59, "action-item", "in-progress")]
        self.assertEqual(GEN.drop_deferred(issues), issues)

    def test_issue_without_labels_key_survives(self):
        self.assertEqual(GEN.drop_deferred([{"number": 5}]), [{"number": 5}])

    def test_empty_list(self):
        self.assertEqual(GEN.drop_deferred([]), [])


class HasLabelTests(unittest.TestCase):

    def test_present_and_absent(self):
        it = issue(1, "action-item", "feature-presentation")
        self.assertTrue(GEN.has_label(it, "feature-presentation"))
        self.assertFalse(GEN.has_label(it, "deferred-indefinitely"))

    def test_missing_and_null_labels_are_safe(self):
        self.assertFalse(GEN.has_label({"number": 1}, "proposed"))
        self.assertFalse(GEN.has_label({"number": 1, "labels": None},
                                       "proposed"))


if __name__ == "__main__":
    unittest.main()
