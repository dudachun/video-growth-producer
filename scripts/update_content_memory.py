#!/usr/bin/env python3
"""Append creator training notes to memory files."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


TARGETS = {
    "memory": "content-memory.md",
    "winning": "winning-patterns.md",
    "forbidden": "forbidden-patterns.md",
    "visual": "visual-style.md",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--root", default=".")
    parser.add_argument("--target", choices=TARGETS, default="memory")
    parser.add_argument("--note", required=True)
    args = parser.parse_args()

    path = Path(args.root) / "profiles" / args.profile / TARGETS[args.target]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# {TARGETS[args.target]}\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {date.today().isoformat()}\n\n- {args.note.strip()}\n")
    print(f"updated={path.resolve()}")


if __name__ == "__main__":
    main()

