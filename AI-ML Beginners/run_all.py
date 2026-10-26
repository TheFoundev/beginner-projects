"""Run all 20 projects and report which ones succeeded.

Usage:
    python run_all.py
    python run_all.py --only 06 13 16
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
PROJECTS = BASE / "projects"


def find_projects(only: list[str] | None = None) -> list[Path]:
    mains = sorted(PROJECTS.glob("*/main.py"))
    if only:
        selected = []
        for main in mains:
            if any(main.parent.name.startswith(prefix) for prefix in only):
                selected.append(main)
        return selected
    return mains


def main() -> int:
    parser = argparse.ArgumentParser(description="Run every project in the pack.")
    parser.add_argument(
        "--only",
        nargs="+",
        help="Run only projects whose folder name starts with these prefixes, e.g. 06 13",
    )
    args = parser.parse_args()

    mains = find_projects(args.only)
    if not mains:
        print("No projects found.")
        return 1

    failures = []
    started = time.time()

    for index, main_file in enumerate(mains, start=1):
        project_dir = main_file.parent
        print("\n" + "=" * 72)
        print(f"[{index}/{len(mains)}] {project_dir.name}")
        print("=" * 72)
        result = subprocess.run(
            [sys.executable, str(main_file)],
            cwd=project_dir,
            text=True,
            capture_output=True,
        )
        if result.stdout:
            print(result.stdout.rstrip())
        if result.returncode != 0:
            failures.append(project_dir.name)
            print("FAILED")
            if result.stderr:
                print(result.stderr.rstrip())
        else:
            print("OK")

    elapsed = time.time() - started
    print("\n" + "=" * 72)
    print(f"Finished {len(mains)} project(s) in {elapsed:.1f}s")
    if failures:
        print(f"Failures: {', '.join(failures)}")
        return 1
    print("All projects ran successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
