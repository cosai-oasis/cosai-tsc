"""Offline integration tests for isolated, allowlisted report-branch publication."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "citation_report_branch.py"
SPEC = importlib.util.spec_from_file_location("citation_report_branch", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
REPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORT)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.repo = root / "checkout"
        self.remote = root / "remote.git"
        self.resume = root / "resume"
        # A wholly local fixture: no user configuration, credentials, or network.
        environment = {
            "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.invalid",
        }
        self.environment = mock.patch.dict(os.environ, environment)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, capture_output=True)
        subprocess.run(["git", "init", "-b", "main", str(self.repo)], check=True, capture_output=True)
        (self.repo / "script.py").write_text("main code\n")
        directory = self.repo / REPORT.DIRECTORY
        directory.mkdir(parents=True)
        (directory / "README.md").write_text("old snapshot\n")
        (directory / "sources.json").write_text("[]\n")
        (directory / "excluded-sources.json").write_text("[]\n")
        self.git("add", ".")
        self.git("commit", "-m", "main baseline")
        self.main = self.git("rev-parse", "HEAD").strip()
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "origin", "main")
        self.git("checkout", "-b", "fix/test")
        (self.repo / "script.py").write_text("unmerged code change\n")
        self.git("add", "script.py")
        self.git("commit", "-m", "unmerged execution code")
        self.execution_head = self.git("rev-parse", "HEAD").strip()
        self.expected_head = REPORT.ABSENT_HEAD
        self.write_generated()

    def git(self, *args, repo=None):
        return REPORT.git(repo or self.repo, *args).decode()

    def publish(self):
        commit = REPORT.publish(self.repo, self.expected_head)
        self.expected_head = commit
        return commit

    def write_generated(self, status="partial"):
        directory = self.repo / REPORT.DIRECTORY
        (directory / "README.md").write_text(f"New {status} report; findings unverified\n")
        (directory / "discovered-candidates.json").write_text(json.dumps({
            "discovery_status": status, "last_attempted": "2026-10-05T16:00:00Z",
            "last_completed": None, "query_coverage": {"completed": 1, "total": 14},
            "discovery_warnings": ["Provider rate limited"], "candidates": [],
        }))
        (directory / "discovery-state.json").write_text(json.dumps({"schema_version": 1, "completed_queries": ["one"]}))
        (directory / "sources.json").write_text('[{"id":"new-source-snapshot"}]\n')
        (directory / "excluded-sources.json").write_text('[{"source_url":"https://example.invalid/excluded"}]\n')

    def test_first_publication_changes_only_five_data_paths_based_on_main(self):
        before = self.git("status", "--porcelain")
        commit = self.publish()
        changed = set(self.git("diff", "--name-only", self.main, commit).splitlines())
        self.assertEqual(changed, {(REPORT.DIRECTORY / name).as_posix() for name in REPORT.REPORT_FILES})
        self.assertEqual(self.git("show", f"{commit}:script.py"), "main code\n")
        self.assertEqual(self.git("rev-parse", f"{commit}^" ).strip(), self.main)
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.execution_head)
        self.assertEqual(self.git("status", "--porcelain"), before)
        self.assertEqual(self.git("rev-parse", "refs/heads/main", repo=self.remote).strip(), self.main)
        self.assertEqual(self.git("show", "-s", "--format=%an", commit).strip(), "github-actions[bot]")

    def test_restore_reads_only_two_json_files_without_checking_out_bot_code(self):
        commit = self.publish()
        self.assertEqual(REPORT.restore(self.repo, self.resume), commit)
        self.assertEqual({path.name for path in self.resume.iterdir()}, set(REPORT.RESUME_FILES))
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.execution_head)
        self.assertEqual((self.repo / "script.py").read_text(), "unmerged code change\n")
        self.assertEqual(json.loads((self.resume / "discovery-state.json").read_text())["completed_queries"], ["one"])

    def test_second_publication_extends_existing_branch_and_preserves_main(self):
        first = self.publish()
        self.write_generated("complete")
        second = self.publish()
        self.assertEqual(self.git("rev-parse", f"{second}^").strip(), first)
        self.assertEqual(self.git("show", f"{second}:script.py"), "main code\n")
        self.assertEqual(self.git("rev-parse", "refs/heads/main", repo=self.remote).strip(), self.main)

    def test_identical_snapshot_does_not_create_extra_commit(self):
        first = self.publish()
        self.assertEqual(self.publish(), first)

    def test_missing_branch_starts_with_empty_resume_directory(self):
        self.assertEqual(REPORT.restore(self.repo, self.resume), REPORT.ABSENT_HEAD)
        self.assertEqual(list(self.resume.iterdir()), [])

    def test_restore_refuses_nonempty_directory(self):
        self.resume.mkdir()
        (self.resume / "old-state").write_text("stale")
        with self.assertRaisesRegex(ValueError, "must be empty"):
            REPORT.restore(self.repo, self.resume)

    def test_publish_rejects_missing_health_metadata(self):
        (self.repo / REPORT.DIRECTORY / "discovered-candidates.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "explicit discovery health"):
            self.publish()

    def test_publish_rejects_symlinked_data(self):
        path = self.repo / REPORT.DIRECTORY / "README.md"
        path.unlink()
        path.symlink_to(self.repo / "script.py")
        with self.assertRaisesRegex(ValueError, "non-regular"):
            self.publish()

    def test_publish_rejects_invalid_evidence_snapshot(self):
        (self.repo / REPORT.DIRECTORY / "sources.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Evidence snapshot"):
            self.publish()

    def test_concurrent_remote_change_is_not_overwritten(self):
        first = self.publish()
        self.write_generated("complete")
        original_git = REPORT.git
        competing = []

        def racing_git(repo, *args, **kwargs):
            if args[0] == "push":
                tree = original_git(self.repo, "rev-parse", f"{first}^{{tree}}").decode().strip()
                other = original_git(self.repo, "commit-tree", tree, "-p", first, data=b"concurrent update\n").decode().strip()
                # Transfer the competing object before advancing only our local
                # bare fixture's publication ref. No external remote is touched.
                original_git(self.repo, "push", "origin", f"{other}:refs/heads/{REPORT.BRANCH}")
                competing.append(other)
            return original_git(repo, *args, **kwargs)

        with mock.patch.object(REPORT, "git", side_effect=racing_git):
            with self.assertRaises(subprocess.CalledProcessError):
                self.publish()
        self.assertEqual(self.git("rev-parse", f"refs/heads/{REPORT.BRANCH}", repo=self.remote).strip(), competing[0])

    def test_remote_update_after_restore_before_publish_is_not_overwritten(self):
        first = self.publish()
        restored = REPORT.restore(self.repo, self.resume)
        self.assertEqual(restored, first)
        self.write_generated("complete")
        competing = self.publish()
        self.write_generated("partial")
        with self.assertRaisesRegex(ValueError, "changed since restore"):
            REPORT.publish(self.repo, restored)
        self.assertEqual(self.git("rev-parse", f"refs/heads/{REPORT.BRANCH}", repo=self.remote).strip(), competing)

    def test_remote_creation_after_absent_restore_is_not_overwritten(self):
        restored = REPORT.restore(self.repo, self.resume)
        self.assertEqual(restored, REPORT.ABSENT_HEAD)
        competing = self.publish()
        self.write_generated("complete")
        with self.assertRaisesRegex(ValueError, "changed since restore"):
            REPORT.publish(self.repo, restored)
        self.assertEqual(self.git("rev-parse", f"refs/heads/{REPORT.BRANCH}", repo=self.remote).strip(), competing)

    def test_missing_expected_head_cannot_publish(self):
        with self.assertRaisesRegex(ValueError, "exact restored head"):
            REPORT.publish(self.repo, "")

    def test_partial_summary_is_explicit_and_not_claimed_complete(self):
        report = REPORT.summary(self.repo, "abc123")
        self.assertIn("**partial**", report)
        self.assertIn("no completed discovery yet", report)
        self.assertIn("Query coverage: 1/14", report)
        self.assertIn("remains unhealthy", report)
        self.assertIn("**unverified**", report)

    def test_workflow_publication_gate_requires_refresh_and_authorization_not_artifact_success(self):
        workflow = (SCRIPT.parent.parent / ".github/workflows/refresh-citation-impact.yml").read_text()
        publication = workflow.split("id: publish", 1)[1].split("run:", 1)[0]
        self.assertIn("!cancelled()", publication)
        self.assertIn("steps.refresh.outcome == 'success'", publication)
        self.assertIn("steps.refresh.outputs.exit_code != ''", publication)
        self.assertIn("github.event_name == 'schedule' && github.ref == 'refs/heads/main'", publication)
        self.assertIn("github.event_name == 'workflow_dispatch' && inputs.publish_report", publication)
        self.assertNotIn("success()", publication)
        self.assertIn("steps.restore.outputs.publication_head", publication)
        self.assertIn('--expected-head "$EXPECTED_PUBLICATION_HEAD"', workflow)


if __name__ == "__main__":
    unittest.main()
