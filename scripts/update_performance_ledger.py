#!/usr/bin/env python3
"""Append a JSON record to the creator performance ledger."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--root", default=".")
    parser.add_argument("--record-json", required=True)
    args = parser.parse_args()

    record = json.loads(args.record_json)
    record.setdefault("created", date.today().isoformat())
    path = Path(args.root) / "profiles" / args.profile / "performance-ledger.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"updated={path.resolve()}")


if __name__ == "__main__":
    main()

