"""Regression tests for --skip handling in process_transcript.py.

The plan is re-derived from the model on every invocation, so proposed
new-item indices are not stable between a --dry-run and the real run. Reusing
a dry-run index once skipped an approved item and created one a co-chair had
asked to drop, so the text form exists and is covered here.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "process_transcript.py"
SPEC = importlib.util.spec_from_file_location("process_transcript", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to import {SCRIPT}")
PT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PT)


class ParseSkipsTests(unittest.TestCase):
    def test_bare_number_skips_the_issue(self):
        spec = PT.parse_skips(["48"])
        self.assertEqual(spec["issues"], {48})
        self.assertEqual(spec["closes"], set())
        self.assertEqual(spec["new"], set())

    def test_hash_prefix_is_accepted(self):
        self.assertEqual(PT.parse_skips(["#48"])["issues"], {48})

    def test_close_prefix_targets_closes_only(self):
        spec = PT.parse_skips(["close:48"])
        self.assertEqual(spec["closes"], {48})
        self.assertEqual(spec["issues"], set())

    def test_numeric_new_is_an_index(self):
        spec = PT.parse_skips(["new:3"])
        self.assertEqual(spec["new"], {3})
        self.assertEqual(spec["new_text"], set())

    def test_non_numeric_new_is_a_title_match(self):
        spec = PT.parse_skips(["new:rsac"])
        self.assertEqual(spec["new_text"], {"rsac"})
        self.assertEqual(spec["new"], set())

    def test_comma_and_repeat_forms_combine(self):
        spec = PT.parse_skips(["48,close:70", "new:2", "new:ontology"])
        self.assertEqual(spec["issues"], {48})
        self.assertEqual(spec["closes"], {70})
        self.assertEqual(spec["new"], {2})
        self.assertEqual(spec["new_text"], {"ontology"})

    def test_multi_word_title_match_is_kept_whole(self):
        spec = PT.parse_skips(["new:submit rsac 2027"])
        self.assertEqual(spec["new_text"], {"submit rsac 2027"})

    def test_unparseable_numeric_like_token_exits(self):
        # A typo'd skip that quietly does nothing is how an unwanted close
        # slips through, so a bad *issue* token must abort.
        with self.assertRaises(SystemExit):
            PT.parse_skips(["close:not-a-number"])

    def test_zero_and_negative_indices_exit(self):
        for bad in ("0", "new:0", "-1"):
            with self.subTest(token=bad):
                with self.assertRaises(SystemExit):
                    PT.parse_skips([bad])


class BuildPlanSkipTests(unittest.TestCase):
    """build_plan must honour both skip forms when filing new items."""

    NEW_ITEMS = [
        {"title": "Submit RSAC 2027 proposals via tracking spreadsheet",
         "owner": "Leads", "due_date": "2026-10-09", "body": "b1"},
        {"title": "Coordinate with Dustin on Duke project review",
         "owner": "Claudia Rauch", "due_date": "", "body": "b2"},
        {"title": "Revise Duke University ADRs for readability",
         "owner": "Josiah Hagen", "due_date": "", "body": "b3"},
    ]

    def plan(self, skips):
        return PT.build_plan(
            "2026-09-29",
            {"new_action_items": list(self.NEW_ITEMS), "issue_updates": []},
            {},
            skips=skips,
        )

    def titles(self, plan):
        return [item["title"] for item in plan["create"]]

    def test_no_skips_creates_everything(self):
        plan = self.plan(PT.parse_skips([]))
        self.assertEqual(len(self.titles(plan)), 3)

    def test_text_skip_drops_the_matching_item_only(self):
        plan = self.plan(PT.parse_skips(["new:rsac"]))
        self.assertEqual(
            self.titles(plan),
            ["Coordinate with Dustin on Duke project review",
             "Revise Duke University ADRs for readability"],
        )
        self.assertTrue(any("rsac" in note.lower() for note in plan["skipped"]))

    def test_text_skip_is_case_insensitive(self):
        plan = self.plan(PT.parse_skips(["new:RSAC 2027"]))
        self.assertEqual(len(self.titles(plan)), 2)

    def test_text_skip_matching_nothing_leaves_plan_intact(self):
        plan = self.plan(PT.parse_skips(["new:nonexistent topic"]))
        self.assertEqual(len(self.titles(plan)), 3)

    def test_index_skip_is_positional(self):
        # Documents the hazard the text form exists to avoid: the same index
        # means "whatever is third this run", not a particular title.
        plan = self.plan(PT.parse_skips(["new:3"]))
        self.assertNotIn("Revise Duke University ADRs for readability",
                         self.titles(plan))
        reordered = list(reversed(self.NEW_ITEMS))
        other = PT.build_plan(
            "2026-09-29",
            {"new_action_items": reordered, "issue_updates": []},
            {},
            skips=PT.parse_skips(["new:3"]),
        )
        # Same index, different title dropped — purely because order changed.
        self.assertNotIn("Submit RSAC 2027 proposals via tracking spreadsheet",
                         [i["title"] for i in other["create"]])


if __name__ == "__main__":
    unittest.main()
