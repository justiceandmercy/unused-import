#!/usr/bin/env python3
"""CLI: find unused imports in Python files."""

import argparse
import json
import sys
from pathlib import Path

from analyzer import analyze_file, iter_python_files


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="unused-import",
        description="Find unused imports in Python source files.",
    )
    parser.add_argument("paths", nargs="*", default=["."],
                        help="files or directories to scan (default: .)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    files = iter_python_files(args.paths)
    if not files:
        print("no Python files found", file=sys.stderr)
        return 2

    results = []
    total = 0
    for f in files:
        unused, errors = analyze_file(f)
        if errors:
            for e in errors:
                print(f"{f}: {e}", file=sys.stderr)
            continue
        if not unused:
            continue
        total += len(unused)
        if args.json:
            results.append({"file": str(f), "unused": unused})
        else:
            for u in unused:
                print(f"{f}:{u['line']}: unused import '{u['name']}' ({u['module']})")

    if args.json:
        print(json.dumps(results, indent=2))

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())