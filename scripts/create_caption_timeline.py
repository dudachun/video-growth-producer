#!/usr/bin/env python3
"""Create Remotion-compatible captions from script lines and a total duration."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def weight(text: str) -> int:
    stripped = re.sub(r"[\s，。！？、“”《》：；,.!?;:\"'()（）-]", "", text)
    return max(2, len(stripped))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", required=True)
    parser.add_argument("--duration-sec", type=float, required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--overlap-ms", type=int, default=140)
    args = parser.parse_args()

    lines = [
        line.strip().lstrip("\ufeff")
        for line in Path(args.script).read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if not lines:
        raise SystemExit("script has no non-empty lines")

    weights = [weight(line) for line in lines]
    total = sum(weights)
    cursor = 0.0
    captions = []
    for index, (line, item_weight) in enumerate(zip(lines, weights)):
        duration = args.duration_sec * item_weight / total
        start_ms = round(cursor * 1000)
        if index:
            start_ms = max(0, start_ms - args.overlap_ms)
        end_ms = round((cursor + duration) * 1000)
        captions.append(
            {
                "text": line,
                "startMs": int(start_ms),
                "endMs": int(max(end_ms, start_ms + 360)),
                "timestampMs": None,
                "confidence": None,
            }
        )
        cursor += duration

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(captions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"captions={Path(args.out).resolve()}")


if __name__ == "__main__":
    main()
