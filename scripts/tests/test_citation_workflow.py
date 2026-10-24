"""Execute the workflow's recovery shell against offline process substitutes."""

from pathlib import Path
import os
import shlex
import subprocess
import tempfile
import textwrap
import unittest


WORKFLOW = Path(__file__).resolve().parents[2] / ".github/workflows/refresh-citation-impact.yml"


class WorkflowRecoveryTests(unittest.TestCase):
    def run_workflow_step(self, statuses, elapsed=()):
        # Exercise the actual shell used by Actions, including exit-code capture
        # under bash -e. No GitHub requests, discovery, publication, or waits.
        workflow = WORKFLOW.read_text()
        step = workflow.split("id: refresh\n", 1)[1].split("\n      - name:", 1)[0]
        command = textwrap.dedent(step.split("run: |\n", 1)[1])
        substitutes = """
        python() {
          count=0
          if [ -f "$RUNNER_TEMP/attempts" ]; then
            read -r count < "$RUNNER_TEMP/attempts"
          fi
          count=$((count + 1))
          echo "$count" > "$RUNNER_TEMP/attempts"
          printf '%s\\n' "$*" >> "$RUNNER_TEMP/commands"
          duration=$(sed -n "${count}p" "$RUNNER_TEMP/elapsed")
          SECONDS=$((SECONDS + ${duration:-0}))
          code=$(sed -n "${count}p" "$RUNNER_TEMP/statuses")
          return "${code:-99}"
        }
        sleep() {
          printf '%s\\n' "$1" >> "$RUNNER_TEMP/pauses"
          SECONDS=$((SECONDS + $1))
        }
        """
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "statuses").write_text("".join(f"{value}\n" for value in statuses))
            (root / "elapsed").write_text("".join(f"{value}\n" for value in elapsed))
            output = root / "output"
            result = subprocess.run(
                ["bash", "-e", "-c", textwrap.dedent(substitutes) + command],
                env={**os.environ, "RUNNER_TEMP": temporary, "GITHUB_OUTPUT": str(output)},
                capture_output=True, text=True, timeout=5,
            )
            return {
                "result": result,
                "attempts": int((root / "attempts").read_text()),
                "output": output.read_text() if output.exists() else "",
                "pauses": (root / "pauses").read_text().splitlines() if (root / "pauses").exists() else [],
                "commands": (root / "commands").read_text().splitlines(),
            }

    def test_complete_refresh_stops_without_starting_another_round(self):
        run = self.run_workflow_step([0])
        self.assertEqual(run["result"].returncode, 0, run["result"].stderr)
        self.assertEqual(run["attempts"], 1)
        self.assertEqual(run["output"], "exit_code=0\n")
        self.assertEqual(run["pauses"], [])

    def test_partial_refresh_resumes_and_publishes_final_complete_status(self):
        run = self.run_workflow_step([2, 2, 0])
        self.assertEqual(run["result"].returncode, 0, run["result"].stderr)
        self.assertEqual(run["attempts"], 3)
        self.assertEqual(run["output"], "exit_code=0\n")
        self.assertEqual(run["pauses"], ["60", "60"])
        budgets = []
        for command in run["commands"]:
            args = shlex.split(command)
            budgets.append(int(args[args.index("--discovery-budget-seconds") + 1]))
        self.assertEqual(budgets, [1200, 1140, 1080])
        self.assertIn("--resume-from", run["commands"][0])
        self.assertIn("--fail-on-discovery-error", run["commands"][0])

    def test_exhausted_retries_preserve_partial_status_for_publication_and_failure(self):
        run = self.run_workflow_step([2, 2, 2])
        self.assertEqual(run["result"].returncode, 0, run["result"].stderr)
        self.assertEqual(run["attempts"], 3)
        self.assertEqual(run["output"], "exit_code=2\n")
        self.assertEqual(run["pauses"], ["60", "60"])

    def test_attempt_time_and_pauses_share_one_budget(self):
        run = self.run_workflow_step([2, 0], elapsed=[730, 30])
        self.assertEqual(run["output"], "exit_code=0\n")
        self.assertIn("--discovery-budget-seconds 410", run["commands"][1])

    def test_exhausted_time_does_not_restart_budget_or_sleep(self):
        run = self.run_workflow_step([2], elapsed=[1200])
        self.assertEqual(run["result"].returncode, 0, run["result"].stderr)
        self.assertEqual(run["attempts"], 1)
        self.assertEqual(run["output"], "exit_code=2\n")
        self.assertEqual(run["pauses"], [])

    def test_fatal_errors_never_set_publication_output_or_retry(self):
        for statuses in ([1], [2, 1], [2, 124]):
            with self.subTest(statuses=statuses):
                run = self.run_workflow_step(statuses)
                self.assertEqual(run["result"].returncode, statuses[-1])
                self.assertEqual(run["attempts"], len(statuses))
                self.assertEqual(run["output"], "")


if __name__ == "__main__":
    unittest.main()
