#!/usr/bin/env python3
"""
Fetch CoSAI meeting minutes from Google Drive and GitHub, save as markdown.

Drive sources: Reads Gemini-generated meeting notes from shared Drive
folders, exports them as markdown. Each Drive source is scanned three ways:
per-meeting subfolders, loose notes documents sitting directly in the parent
folder, and a shared-with-me fallback. Drive access goes through the Google
Workspace CLI (`gws`, https://github.com/googleworkspace/cli). See the
"TSC Meeting Planner and Tracker" README for one-time gws + OAuth setup;
an expired token surfaces as `token_valid: false` in `gws auth status` and
makes every Drive source silently stale — re-run `gws auth login`.
Currently covers
WS1, WS2, WS3, WS4, the ADLC SIG (under WS4), the Code-Development SIG
(under WS3), the Risk Management SIG (under WS3), and the Agent Credentials
group.

GitHub sources: Reads markdown meeting minutes committed to public GitHub
repo directories. Covers TSC minutes and PGB minutes. Uses the unauthenticated
GitHub Contents API; honors GITHUB_TOKEN env var if set to raise the rate
limit.

Output goes under meeting_minutes/<subdir>/ in this repo. All minutes are
downloaded as-is — filtering for TSC-relevant content happens in
generate_tsc_agenda.py, not here.

Usage:
    # Fetch all meeting minutes
    python scripts/fetch_meeting_minutes.py

    # Fetch only new minutes (skip existing files)
    python scripts/fetch_meeting_minutes.py --skip-existing

    # Fetch only GitHub sources (TSC + PGB); skip Drive sources
    python scripts/fetch_meeting_minutes.py --github-only

    # Fetch only TSC minutes
    python scripts/fetch_meeting_minutes.py --tsc-only
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# ── Configuration ─────────────────────────────────────────────────────────────
# Meeting sources. Each source has:
#   type:    "drive" or "github"
#   subdir:  output subdirectory under meeting_minutes/
#   For drive sources:
#     folder_id: Google Drive parent folder containing per-meeting subfolders
#     shared_name_contains: substring to match in shared-with-me fallback
#     shared_title_pattern: regex to extract date from shared-with-me filename
#     shared_folder_name_template: output folder name template using {y}{m}{d}
#   For github sources:
#     repo: GitHub repo in owner/name format
#     path: directory path inside the repo containing markdown files

SOURCES = [
    # ── GitHub sources ────────────────────────────────────────────────────────
    {
        "name": "TSC",
        "type": "github",
        "repo": "cosai-oasis/cosai-tsc",
        "path": "tsc-meeting-minutes",
        "subdir": "tsc",
    },
    {
        "name": "PGB",
        "type": "github",
        "repo": "cosai-oasis/oasis-open-project",
        "path": "pgb-meeting-minutes",
        "subdir": "pgb",
        # Note: PGB minutes are filtered for TSC-relevant items in
        # generate_tsc_agenda.py — all files are downloaded here as-is.
    },

    # ── Google Drive sources ──────────────────────────────────────────────────
    {
        "name": "WS1",
        "type": "drive",
        "folder_id": "1L7A46unF12D3Tk68_QVP53M9cGjJUMA3",
        "subdir": "ws1",
        # Prefix match — works whether or not "Notes by Gemini" is appended.
        # The meeting was renamed from "CoSAI WS1 Weekly Meeting" to
        # "CoSAI WS1 Meeting (updated)"; match both so older titles keep working.
        # Narrowest substring common to both old and new titles.
        "shared_name_contains": "CoSAI WS1",
        "shared_title_pattern": (
            r"^CoSAI WS1 (?:Weekly )?Meeting(?: \(updated\))?\s+- "
            r"(?P<y>\d{4})/(?P<m>\d{2})/(?P<d>\d{2})"
        ),
        "shared_folder_name_template": "WS1-{y}{m}{d}",
    },
    {
        "name": "WS2",
        "type": "drive",
        "folder_id": "1zmeLjxAp8UJdu99LM3qAhHf-CH9JGR32",
        "subdir": "ws2",
        # Prefix match — WS2 files end after the date with no "Notes by Gemini".
        # Titles are now "CoSAI WS2 Defenders Bi-Weekly Meeting". Some older
        # entries separate the date with "/" in the day position (2026/05-19),
        # so accept "/" or "-" between date parts.
        "shared_name_contains": "CoSAI WS2 Defenders",
        "shared_title_pattern": (
            r"^CoSAI WS2 Defenders (?:Bi-Weekly )?[Mm]eeting\s+- "
            r"(?P<y>\d{4})[/-](?P<m>\d{2})[/-](?P<d>\d{2})"
        ),
        "shared_folder_name_template": "WS2-{y}{m}{d}",
    },
    {
        "name": "WS3",
        "type": "drive",
        "folder_id": "1NFk_-2Plyi3qYr2qtrvt42AQhzJZB0Wf",
        "subdir": "ws3",
        # Titles are "WS3 bi-weekly meeting  - <date>" — note the double space
        # before the dash, hence \s+ rather than a literal " ".
        "shared_name_contains": "WS3 bi-weekly meeting",
        "shared_title_pattern": (
            r"^WS3 bi-weekly meeting\s+- "
            r"(?P<y>\d{4})/(?P<m>\d{2})/(?P<d>\d{2})"
        ),
        "shared_folder_name_template": "WS3-{y}{m}{d}",
    },
    {
        "name": "WS4",
        "type": "drive",
        "folder_id": "1TJl4yqWIdfPc8fKWiTO0CsmsmuecGxWa",
        "subdir": "ws4",
        "shared_name_contains": "CoSAI WS4 recurring meeting",
        "shared_title_pattern": (
            r"^CoSAI WS4 recurring meeting - "
            r"(?P<y>\d{4})/(?P<m>\d{2})/(?P<d>\d{2})"
        ),
        "shared_folder_name_template": "WS4-{y}{m}{d}",
    },
    {
        "name": "ADLC",
        "type": "drive",
        "folder_id": "1EkoOpMCtYahLu-sEhYrgNDmvPyTtgpit",
        "subdir": "adlc",
        "shared_name_contains": "WS4 SIG Security of Agent Development Lifecycle",
        "shared_title_pattern": (
            r"^WS4 SIG Security of Agent Development Lifecycle - "
            r"(?P<y>\d{4})/(?P<m>\d{2})/(?P<d>\d{2})"
        ),
        "shared_folder_name_template": "{y}-{m}-{d}",
    },
    {
        "name": "Code-SIG",
        "type": "drive",
        "folder_id": "1yKk-Mbbpowsk3gfRwGIT7UpMOJ-fDzdo",
        "subdir": "code-sig",
        "shared_name_contains": "CoSAI WS3 SIG: Security of AI-Assisted Code Development",
        "shared_title_pattern": (
            r"^CoSAI WS3 SIG: Security of AI-Assisted Code Development - "
            r"(?P<y>\d{4})/(?P<m>\d{2})/(?P<d>\d{2})"
        ),
        "shared_folder_name_template": "{y}-{m}-{d}",
    },
    {
        "name": "RM-SIG",
        "type": "drive",
        "folder_id": "1tboOFAyYHnJRlXqMO3Kdh6KrcAVVIpiB",
        "subdir": "rm-sig",
        "shared_name_contains": "CoSAI WS3 CoSAI-RM SIG weekly meeting",
        "shared_title_pattern": (
            r"^CoSAI WS3 CoSAI-RM SIG weekly meeting - "
            r"(?P<y>\d{4})/(?P<m>\d{2})/(?P<d>\d{2})"
        ),
        "shared_folder_name_template": "WS3-CoSAI-RM-SIG-{y}{m}{d}",
    },
    {
        "name": "Agent-Credentials",
        "type": "drive",
        "folder_id": "1Telz7CDwCgPNUyHlMwu9cBGl-keqP9z3",
        "subdir": "agent-credentials",
        "shared_name_contains": "CoSAI WS4: Agent Credentials",
        "shared_title_pattern": (
            r"^CoSAI WS4: Agent Credentials - "
            r"(?P<y>\d{4})/(?P<m>\d{2})/(?P<d>\d{2})"
        ),
        "shared_folder_name_template": "{y}-{m}-{d}",
    },
]

# Output directory — derived from this script's location so it always writes
# into the repo it is run from, regardless of where the user cloned it.
REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "meeting_minutes"


# ── Drive helpers ─────────────────────────────────────────────────────────────

class GwsError(Exception):
    """A gws invocation failed; message carries the API error if parseable."""


def run_gws(args, cwd=None):
    """Run a gws command and return parsed JSON from stdout."""
    result = subprocess.run(
        ["gws", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        message = result.stderr.strip().splitlines()[-1:] or ["unknown error"]
        try:
            err = json.loads(result.stdout).get("error", {})
            message = [f"{err.get('code', '?')} {err.get('message', 'unknown error')}"]
        except (json.JSONDecodeError, AttributeError):
            pass
        raise GwsError(message[0])
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise GwsError(f"unparseable gws output: {e}")


def drive_list(params):
    """Call `gws drive files list`, following pagination. Returns files[]."""
    files = []
    params = dict(params)
    while True:
        response = run_gws(["drive", "files", "list", "--params",
                            json.dumps(params)])
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            return files
        params["pageToken"] = page_token


def check_gws():
    """Verify the gws CLI is available before doing any Drive work."""
    if shutil.which("gws"):
        return
    print("Error: the Google Workspace CLI (`gws`) is not on PATH.",
          file=sys.stderr)
    print("Install it from https://github.com/googleworkspace/cli/releases",
          file=sys.stderr)
    print("Then authenticate with: gws auth login", file=sys.stderr)
    sys.exit(1)


def list_meeting_folders(parent_folder_id):
    """List all meeting subfolders in a parent Drive folder."""
    folders = drive_list({
        "q": (
            f"'{parent_folder_id}' in parents and "
            "mimeType='application/vnd.google-apps.folder' and trashed=false"
        ),
        "fields": "nextPageToken, files(id, name)",
        "pageSize": 100,
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True,
    })
    return sorted(folders, key=lambda f: f["name"])


def find_notes_doc(folder_id):
    """Find the Gemini notes document in a meeting folder.

    Prefers files with 'Notes by Gemini' in the name; falls back to any
    resolvable Google Doc or shortcut pointing to one.
    """
    files = drive_list({
        "q": (
            f"'{folder_id}' in parents and trashed=false and "
            "(mimeType='application/vnd.google-apps.document' "
            "or mimeType='application/vnd.google-apps.shortcut')"
        ),
        "fields": "nextPageToken, files(id, name, mimeType, shortcutDetails)",
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True,
    })

    def resolve(f):
        if f["mimeType"] == "application/vnd.google-apps.shortcut":
            sd = f.get("shortcutDetails") or {}
            if sd.get("targetMimeType") != "application/vnd.google-apps.document":
                return None
            return {
                "id": sd["targetId"],
                "name": f["name"],
                "mimeType": sd["targetMimeType"],
            }
        return f

    # Prefer "Notes by Gemini" matches first
    for f in files:
        if "Notes by Gemini" in f["name"]:
            resolved = resolve(f)
            if resolved:
                return resolved
    # Fall back to any resolvable doc
    for f in files:
        resolved = resolve(f)
        if resolved:
            return resolved
    return None


def export_doc_as_markdown(file_id, workdir):
    """Export a Google Doc as markdown text via gws."""
    tmp_name = f".gws-export-{os.getpid()}.tmp"
    tmp_path = workdir / tmp_name
    try:
        run_gws(
            [
                "drive", "files", "export",
                "--params", json.dumps({
                    "fileId": file_id,
                    "mimeType": "text/markdown",
                }),
                "-o", tmp_name,
            ],
            cwd=workdir,
        )
        return tmp_path.read_text(encoding="utf-8")
    finally:
        tmp_path.unlink(missing_ok=True)


def folder_name_to_filename(folder_name):
    """Convert a folder name to a safe markdown filename.

    e.g. 'WS4-20260402' → 'WS4-20260402.md'
         'WS1 20260402' → 'WS1-20260402.md'

    Path separators and other characters that are unsafe in filenames are
    replaced with '-', so a raw Gemini document title can be passed in safely.
    """
    name = re.sub(r"\s+", "-", folder_name.strip())
    name = re.sub(r'[/\\:*?"<>|]', "-", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    return f"{name}.md"


def fetch_drive_source(source, output_dir, skip_existing):
    """Fetch all meeting notes from a Drive source by walking its folder tree.

    Returns (fetched, skipped, no_notes, errors).
    """
    fetched = skipped = no_notes = errors = 0

    print(f"\n[{source['name']}] Listing meeting folders...")
    folders = list_meeting_folders(source["folder_id"])
    print(f"[{source['name']}] Found {len(folders)} meeting folders")

    for folder in folders:
        filename = folder_name_to_filename(folder["name"])
        output_path = output_dir / filename

        if skip_existing and output_path.exists():
            skipped += 1
            continue

        notes_doc = find_notes_doc(folder["id"])
        if not notes_doc:
            print(f"  {folder['name']}: no notes document found")
            no_notes += 1
            continue

        print(f"  {folder['name']}: fetching '{notes_doc['name']}'...")
        try:
            content = export_doc_as_markdown(notes_doc["id"], output_dir)
        except GwsError as e:
            print(f"  {folder['name']}: export failed ({e}); skipping",
                  file=sys.stderr)
            errors += 1
            continue

        header = (
            f"# {folder['name']}\n\n"
            f"**Source:** {notes_doc['name']}\n\n---\n\n"
        )
        with open(output_path, "w") as f:
            f.write(header + content)

        fetched += 1

    return fetched, skipped, no_notes, errors


def fetch_drive_loose_docs(source, output_dir, skip_existing):
    """Catch notes that sit directly in the source's parent folder rather than
    inside a per-meeting subfolder.

    Gemini now drops "<meeting title> - YYYY/MM/DD HH:MM TZ - Notes by Gemini"
    documents straight into the workstream folder. `fetch_drive_source` only
    walks subfolders, and `fetch_drive_shared_fallback` only queries
    `sharedWithMe`, which does not match files in a folder we can list
    directly — so without this pass those notes are never fetched.

    The output filename is derived from the date in the title via the same
    `shared_folder_name_template` used by the shared-with-me fallback, so a
    meeting filed into a subfolder later resolves to the same filename and is
    skipped rather than duplicated.

    Returns (fetched, skipped, errors).
    """
    pattern = source.get("shared_title_pattern")
    template = source.get("shared_folder_name_template")
    if not (pattern and template):
        return 0, 0, 0

    fetched = skipped = errors = 0
    pat = re.compile(pattern)

    print(f"\n[{source['name']}] Scanning parent folder for loose notes...")
    try:
        candidates = drive_list({
            "q": (
                f"'{source['folder_id']}' in parents and trashed=false and "
                "mimeType='application/vnd.google-apps.document'"
            ),
            "fields": "nextPageToken, files(id, name, mimeType)",
            "pageSize": 100,
            "supportsAllDrives": True,
            "includeItemsFromAllDrives": True,
        })
    except GwsError as e:
        print(f"[{source['name']}] parent-folder listing failed ({e})",
              file=sys.stderr)
        return 0, 0, 1

    for f in candidates:
        m = pat.search(f["name"])
        if not m:
            continue
        synthetic = template.format(**m.groupdict())
        output_path = output_dir / folder_name_to_filename(synthetic)

        if skip_existing and output_path.exists():
            skipped += 1
            continue

        print(f"  [loose] {synthetic}: fetching '{f['name']}'...")
        try:
            content = export_doc_as_markdown(f["id"], output_dir)
        except GwsError as e:
            print(f"  [loose] {synthetic}: export failed ({e}); skipping",
                  file=sys.stderr)
            errors += 1
            continue

        header = (
            f"# {synthetic}\n\n"
            f"**Source:** {f['name']} (via parent-folder scan)\n\n"
            f"---\n\n"
        )
        with open(output_path, "w") as out:
            out.write(header + content)
        fetched += 1

    return fetched, skipped, errors


def fetch_drive_shared_fallback(source, output_dir, skip_existing):
    """Catch notes shared directly with the user but not yet filed into a
    per-meeting subfolder in Drive.

    Uses a prefix regex match so it works whether or not 'Notes by Gemini'
    is appended to the filename — making it robust to Gemini title variations.

    Returns (fetched, skipped, errors).
    """
    name_contains = source.get("shared_name_contains")
    pattern = source.get("shared_title_pattern")
    template = source.get("shared_folder_name_template")
    if not (name_contains and pattern and template):
        return 0, 0, 0

    fetched = skipped = errors = 0
    # re.search rather than re.match — handles any prefix in the title
    pat = re.compile(pattern)

    safe_contains = name_contains.replace("'", "\\'")
    q = (
        "sharedWithMe = true and trashed = false and "
        "mimeType = 'application/vnd.google-apps.document' and "
        f"name contains '{safe_contains}'"
    )

    print(f"\n[{source['name']}] Scanning shared-with-me for unfiled notes...")
    candidates = drive_list({
        "q": q,
        "fields": "nextPageToken, files(id, name, mimeType)",
        "pageSize": 100,
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True,
    })

    for f in candidates:
        m = pat.search(f["name"])
        if not m:
            continue
        synthetic = template.format(**m.groupdict())
        output_path = output_dir / folder_name_to_filename(synthetic)

        if skip_existing and output_path.exists():
            skipped += 1
            continue

        print(f"  [shared] {synthetic}: fetching '{f['name']}'...")
        try:
            content = export_doc_as_markdown(f["id"], output_dir)
        except GwsError as e:
            print(f"  [shared] {synthetic}: export failed ({e}); skipping",
                  file=sys.stderr)
            errors += 1
            continue

        header = (
            f"# {synthetic}\n\n"
            f"**Source:** {f['name']} (via shared-with-me fallback)\n\n"
            f"---\n\n"
        )
        with open(output_path, "w") as out:
            out.write(header + content)
        fetched += 1

    return fetched, skipped, errors


# ── GitHub helpers ────────────────────────────────────────────────────────────

def _github_request(url):
    """Open a GitHub API or raw content URL with optional bearer auth."""
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "fetch_meeting_minutes",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    return urllib.request.urlopen(req, timeout=30)


def fetch_github_source(source, output_dir, skip_existing):
    """Fetch markdown meeting minutes from a GitHub repo directory.

    Downloads all .md files found in the specified path. Content filtering
    (e.g. extracting only TSC-relevant items from PGB minutes) is done
    downstream in generate_tsc_agenda.py, not here.

    Returns (fetched, skipped, errors).
    """
    fetched = skipped = errors = 0
    api_url = (
        f"https://api.github.com/repos/{source['repo']}"
        f"/contents/{source['path']}"
    )

    print(f"\n[{source['name']}] Listing GitHub directory "
          f"{source['repo']}/{source['path']}...")
    try:
        with _github_request(api_url) as resp:
            listing = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"[{source['name']}] GitHub API error: {e.code} {e.reason}",
              file=sys.stderr)
        return fetched, skipped, errors + 1

    md_files = [
        f for f in listing
        if f.get("type") == "file" and f["name"].endswith(".md")
    ]
    print(f"[{source['name']}] Found {len(md_files)} markdown files")

    for f in md_files:
        output_path = output_dir / f["name"]
        if skip_existing and output_path.exists():
            skipped += 1
            continue

        print(f"  {f['name']}: fetching...")
        try:
            with _github_request(f["download_url"]) as resp:
                content = resp.read().decode("utf-8")
        except (urllib.error.URLError, OSError) as e:
            print(f"  {f['name']}: download failed ({e}); skipping",
                  file=sys.stderr)
            errors += 1
            continue

        output_path.write_text(content, encoding="utf-8")
        fetched += 1

    return fetched, skipped, errors


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fetch CoSAI meeting minutes from Drive and GitHub"
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip meetings that already have a local file",
    )
    parser.add_argument(
        "--github-only",
        action="store_true",
        help="Fetch only GitHub sources (TSC + PGB); skip all Drive sources",
    )
    parser.add_argument(
        "--tsc-only",
        action="store_true",
        help="Fetch only TSC minutes from GitHub; skip everything else",
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Only check for gws if we are fetching Drive sources
    needs_drive = (
        any(s["type"] == "drive" for s in SOURCES)
        and not args.github_only
        and not args.tsc_only
    )
    if needs_drive:
        check_gws()

    total_fetched = 0
    total_skipped = 0
    total_no_notes = 0
    total_errors = 0

    for source in SOURCES:
        # Apply source filters
        if args.tsc_only and source["name"] != "TSC":
            continue
        if args.github_only and source["type"] == "drive":
            continue

        output_dir = (
            OUTPUT_DIR / source["subdir"]
            if source.get("subdir")
            else OUTPUT_DIR
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        if source["type"] == "drive":
            fetched, skipped, no_notes, errors = fetch_drive_source(
                source, output_dir, args.skip_existing
            )
            total_no_notes += no_notes
            total_errors += errors
            f2, s2, e2 = fetch_drive_loose_docs(
                source, output_dir, args.skip_existing
            )
            fetched += f2
            skipped += s2
            total_errors += e2
            f3, s3, e3 = fetch_drive_shared_fallback(
                source, output_dir, args.skip_existing
            )
            fetched += f3
            skipped += s3
            total_errors += e3

        elif source["type"] == "github":
            fetched, skipped, errors = fetch_github_source(
                source, output_dir, args.skip_existing
            )
            total_errors += errors

        else:
            print(
                f"[{source['name']}] Unknown source type: {source['type']}",
                file=sys.stderr,
            )
            continue

        total_fetched += fetched
        total_skipped += skipped

    print(
        f"\nDone: {total_fetched} fetched, {total_skipped} skipped, "
        f"{total_no_notes} without notes, {total_errors} errors"
    )


if __name__ == "__main__":
    main()
