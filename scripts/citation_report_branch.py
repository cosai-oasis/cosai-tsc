#!/usr/bin/env python3
"""Restore and publish citation data without checking out the publication branch.

Only the five explicit report/data paths can be committed. Git's normal fast-forward
push checks protect concurrent changes; this helper never force-pushes.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent.parent
BRANCH = "automation/citation-impact-report"
DIRECTORY = Path("TSC Deliverables/citation-impact")
REPORT_FILES = ("README.md", "discovered-candidates.json", "discovery-state.json", "sources.json", "excluded-sources.json")
RESUME_FILES = ("discovered-candidates.json", "discovery-state.json")
ABSENT_HEAD = "absent"


def git(repo: Path, *args: str, data: bytes | None = None, env: dict[str, str] | None = None) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args], input=data, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env=env, check=True,
    ).stdout


def remote_head(repo: Path, branch: str) -> str | None:
    ref = f"refs/heads/{branch}"
    result = subprocess.run(
        ["git", "-C", str(repo), "ls-remote", "--exit-code", "--heads", "origin", ref],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode == 2:
        return None
    if result.returncode:
        raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
    git(repo, "fetch", "--no-tags", "--depth=1", "origin", ref)
    return git(repo, "rev-parse", "FETCH_HEAD").decode().strip()


def restore(repo: Path, destination: Path) -> str:
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError("Resume destination must be empty to prevent stale state reuse")
    head = remote_head(repo, BRANCH)
    if head is None:
        print("No published report branch yet; starting from checked-in data.")
        return ABSENT_HEAD
    for name in RESUME_FILES:
        path = (DIRECTORY / name).as_posix()
        entry = git(repo, "ls-tree", "-z", head, "--", path)
        if not entry:
            continue
        if entry.split(b" ", 1)[0] not in {b"100644", b"100755"}:
            raise ValueError(f"Refusing non-regular published data: {path}")
        payload = git(repo, "show", f"{head}:{path}")
        if not isinstance(json.loads(payload), dict):
            raise ValueError(f"Published data must be a JSON object: {path}")
        (destination / name).write_bytes(payload)
    print(f"Restored publication state from {head}; no publication-branch code was checked out.")
    return head


def generated_files(repo: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for name in REPORT_FILES:
        source = repo / DIRECTORY / name
        if not stat.S_ISREG(source.lstat().st_mode):
            raise ValueError(f"Refusing non-regular generated report file: {name}")
        files[name] = source.read_bytes()
    metadata = json.loads(files["discovered-candidates.json"])
    state = json.loads(files["discovery-state.json"])
    if not isinstance(metadata, dict) or not isinstance(state, dict):
        raise ValueError("Generated metadata and state must be JSON objects")
    if metadata.get("discovery_status") not in {"complete", "partial"} or not metadata.get("last_attempted"):
        raise ValueError("Refusing to publish without explicit discovery health and attempt timestamp")
    for name in ("sources.json", "excluded-sources.json"):
        if not isinstance(json.loads(files[name]), list):
            raise ValueError(f"Evidence snapshot must be a JSON list: {name}")
    return files


def publish(repo: Path, expected_head: str) -> str:
    if expected_head != ABSENT_HEAD and not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", expected_head):
        raise ValueError("Publication requires the exact restored head or explicit absent sentinel")
    files = generated_files(repo)
    base = remote_head(repo, BRANCH)
    if (base or ABSENT_HEAD) != expected_head:
        raise ValueError("Publication branch changed since restore; refusing to overwrite newer data. Run a fresh refresh.")
    if base is None:
        base = remote_head(repo, "main")
    if base is None:
        raise ValueError("Cannot initialize publication branch without origin/main")
    # The isolated index preserves other files at the existing publication tip
    # (or main for its first commit), never at the selected execution ref.
    with tempfile.TemporaryDirectory(prefix="citation-publish-") as temporary:
        env = {
            **os.environ,
            "GIT_INDEX_FILE": str(Path(temporary) / "index"),
            "GIT_AUTHOR_NAME": "github-actions[bot]",
            "GIT_AUTHOR_EMAIL": "41898282+github-actions[bot]@users.noreply.github.com",
            "GIT_COMMITTER_NAME": "github-actions[bot]",
            "GIT_COMMITTER_EMAIL": "41898282+github-actions[bot]@users.noreply.github.com",
        }
        git(repo, "read-tree", base, env=env)
        for name, payload in files.items():
            blob = git(repo, "hash-object", "-w", "--stdin", data=payload).decode().strip()
            git(repo, "update-index", "--add", "--cacheinfo", "100644", blob, (DIRECTORY / name).as_posix(), env=env)
        tree = git(repo, "write-tree", env=env).decode().strip()
        if tree == git(repo, "rev-parse", f"{base}^{{tree}}").decode().strip():
            print("Published report already matches generated data.")
            return base
        commit = git(repo, "commit-tree", tree, "-p", base,
                     data=b"docs: publish CoSAI citation discovery snapshot\n", env=env).decode().strip()
        git(repo, "push", "origin", f"{commit}:refs/heads/{BRANCH}")
    print(f"Published only the five report and evidence-snapshot files at {commit}.")
    return commit


def summary(repo: Path, publication: str | None) -> str:
    metadata = json.loads((repo / DIRECTORY / "discovered-candidates.json").read_text(encoding="utf-8"))
    status = metadata.get("discovery_status", "unknown")
    coverage = metadata.get("query_coverage", {})
    lines = [
        "## Citation discovery health",
        f"- Discovery status: **{status}**",
        f"- Last attempted: {metadata.get('last_attempted') or 'not available'}",
        f"- Last completed: {metadata.get('last_completed') or 'no completed discovery yet'}",
        f"- Query coverage: {coverage.get('completed', '?')}/{coverage.get('total', '?')}",
        "- New findings are automatically published as **unverified**, not added to verified citation totals.",
    ]
    if publication:
        lines.append(f"- Published snapshot commit: `{publication}` on `{BRANCH}`")
    else:
        lines.append("- No report was published by this run; inspect the run status and diagnostic artifact.")
    if status == "partial":
        lines.append("- **Partial refresh:** preserved progress can resume on the next run; this run remains unhealthy.")
    for warning in metadata.get("discovery_warnings", []):
        lines.append(f"- Warning: {str(warning).replace(chr(10), ' ')}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    restore_args = commands.add_parser("restore")
    restore_args.add_argument("--destination", type=Path, required=True)
    publish_args = commands.add_parser("publish")
    publish_args.add_argument("--expected-head", required=True)
    summary_args = commands.add_parser("summary")
    summary_args.add_argument("--publication")
    args = parser.parse_args()
    try:
        if args.command == "restore":
            head = restore(args.repo, args.destination)
            if os.environ.get("GITHUB_OUTPUT"):
                with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
                    output.write(f"publication_head={head}\n")
        elif args.command == "publish":
            commit = publish(args.repo, args.expected_head)
            if os.environ.get("GITHUB_OUTPUT"):
                with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
                    output.write(f"commit={commit}\n")
        else:
            report = summary(args.repo, args.publication)
            print(report)
            if os.environ.get("GITHUB_STEP_SUMMARY"):
                with Path(os.environ["GITHUB_STEP_SUMMARY"]).open("a", encoding="utf-8") as output:
                    output.write(report)
    except subprocess.CalledProcessError as error:
        parser.exit(1, error.stderr.decode(errors="replace") if error.stderr else str(error))


if __name__ == "__main__":
    main()
