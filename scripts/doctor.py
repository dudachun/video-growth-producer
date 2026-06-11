#!/usr/bin/env python3
"""Check whether the workspace can run publish-quality video generation."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path


def command_available(name: str) -> bool:
    return shutil.which(name) is not None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--profile", default="default")
    parser.add_argument(
        "--mode",
        choices=["strict", "remotion-only"],
        default="strict",
        help="strict requires imagegen; remotion-only is a user-confirmed preview fallback.",
    )
    parser.add_argument(
        "--imagegen",
        choices=["available", "missing", "unknown"],
        default=os.environ.get("VGP_IMAGEGEN", "unknown"),
        help="Agent-level image generation capability. Set available only when the current agent can call imagegen.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    profile_dir = root / "profiles" / args.profile
    remotion_template = root / "assets" / "remotion-template"

    checks = {
        "root": str(root),
        "mode": args.mode,
        "profile": str(profile_dir),
        "python": True,
        "node": command_available("node"),
        "npm": command_available("npm"),
        "ffmpeg": command_available("ffmpeg"),
        "ffprobe": command_available("ffprobe"),
        "remotion_template": remotion_template.exists(),
        "creator_profile": (profile_dir / "creator-profile.yaml").exists(),
        "output_dir": (root / "output").exists(),
        "imagegen": args.imagegen,
    }

    blockers: list[str] = []
    for key in ["node", "npm", "ffmpeg", "ffprobe", "remotion_template"]:
        if not checks[key]:
            blockers.append(f"missing {key}")

    if args.mode == "strict" and args.imagegen != "available":
        blockers.append("strict publish mode requires imagegen or an equivalent image generation tool")

    if args.mode == "remotion-only" and args.imagegen == "available":
        blockers.append("imagegen is available; use strict mode unless the user explicitly requested a preview fallback")

    result = {
        "ok": not blockers,
        "checks": checks,
        "blockers": blockers,
        "next_step": "continue" if not blockers else "fix blockers or explicitly switch to remotion-only preview mode",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if blockers:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
