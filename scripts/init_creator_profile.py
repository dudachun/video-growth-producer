#!/usr/bin/env python3
"""Initialize a local trainable creator profile."""

from __future__ import annotations

import argparse
from pathlib import Path


CREATOR_PROFILE = """profile_name: {profile}
series_name: ""
niche: ""
audience: ""
content_goal: ""
offer_or_conversion: ""
tone: ""
platforms:
  - douyin
  - tiktok
default_duration_sec: 45
video_engine: remotion
optional_enhancers:
  imagegen: true
  hyperframes: false
voice:
  provider: cosyvoice
  profile_id: ""
  fallback: ask
style:
  visual_mode: light-tech
  caption_position: 75%
  keyword_highlight: yellow
"""


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    profile_dir = root / "profiles" / args.profile
    profile_dir.mkdir(parents=True, exist_ok=True)

    write_if_missing(profile_dir / "creator-profile.yaml", CREATOR_PROFILE.format(profile=args.profile))
    write_if_missing(
        profile_dir / "content-memory.md",
        "# Content Memory\n\nAdd durable script, audience, offer, and style preferences here.\n",
    )
    write_if_missing(
        profile_dir / "winning-patterns.md",
        "# Winning Patterns\n\nRecord hooks, visual structures, and topics that performed well.\n",
    )
    write_if_missing(
        profile_dir / "forbidden-patterns.md",
        "# Forbidden Patterns\n\nRecord patterns the creator does not want repeated.\n",
    )
    write_if_missing(
        profile_dir / "visual-style.md",
        "# Visual Style\n\nRecord preferred palettes, layouts, caption rules, and reference creators.\n",
    )
    write_if_missing(profile_dir / "episode-ledger.jsonl", "")
    write_if_missing(profile_dir / "performance-ledger.jsonl", "")

    for folder in ["input", "output", "assets", ".generated/audio", ".generated/covers"]:
        (root / folder).mkdir(parents=True, exist_ok=True)

    print(f"profile_dir={profile_dir}")


if __name__ == "__main__":
    main()

