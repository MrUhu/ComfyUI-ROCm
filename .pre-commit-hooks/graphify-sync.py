#!/usr/bin/env python3
"""Pre-commit hook that syncs graphify outputs when topology changes are detected."""

import subprocess
import sys
import os


def main():
    # Ensure we're running from the repository root
    os.chdir(os.environ.get("PRE_COMMIT_SOURCE_DIR", "."))

    no_changes_msg = "No code-graph topology changes detected; outputs left untouched"

    # Step 1: Run `graphify update .`
    try:
        result = subprocess.run(
            ["graphify", "update", "."],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print(
            "[graphify-sync] ERROR: 'graphify' command not found. "
            "Install it first (e.g., pip install graphify)."
        )
        return 1

    if result.returncode != 0:
        print(
            f"[graphify-sync] ERROR: 'graphify update .' failed with exit code {result.returncode}"
        )
        if result.stderr:
            print(result.stderr)
        return 1

    # Step 2: Check if there are no changes
    if no_changes_msg in result.stdout:
        print(
            "[graphify-sync] No code-graph topology changes detected; outputs left untouched."
        )
        return 0

    # Step 3: Changes were detected — print update output and run `graphify label .`
    print("[graphify-sync] Topology changes detected. Running graphify label...")
    print(result.stdout)

    label_result = subprocess.run(
        ["graphify", "label", "."],
        capture_output=True,
        text=True,
    )

    if label_result.returncode != 0:
        print(
            f"[graphify-sync] ERROR: 'graphify label .' failed with exit code {label_result.returncode}"
        )
        if label_result.stderr:
            print(label_result.stderr)
        return 1

    print("[graphify-sync] Label output:")
    print(label_result.stdout)

    print("[graphify-sync] Files were modified. Please stage the changes.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
