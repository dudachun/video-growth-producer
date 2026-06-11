#!/usr/bin/env python3
"""Check local workspace readiness for video generation."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    profile_dir = root / "profiles" / args.profile
    checks = {
        "root": str(root),
        "profile_dir": str(profile_dir),
        "creator_profile": (profile_dir / "creator-profile.yaml").exists(),
        "content_memory": (profile_dir / "content-memory.md").exists(),
        "winning_patterns": (profile_dir / "winning-patterns.md").exists(),
        "forbidden_patterns": (profile_dir / "forbidden-patterns.md").exists(),
        "episode_ledger": (profile_dir / "episode-ledger.jsonl").exists(),
        "performance_ledger": (profile_dir / "performance-ledger.jsonl").exists(),
        "input_dir": (root / "input").exists(),
        "output_dir": (root / "output").exists(),
        "voice_samples_dir": (root / "voice_samples").exists(),
        "voice_models_dir": (root / "voice_models").exists(),
        "remotion_project": (root / "package.json").exists() or (root / "remotion-video" / "package.json").exists(),
        "remotion_template": (root / "assets" / "remotion-template" / "package.json").exists(),
        "schemas": (root / "schemas" / "episode_manifest.schema.json").exists()
        and (root / "schemas" / "visual_plan.schema.json").exists(),
        "doctor_script": (root / "scripts" / "doctor.py").exists(),
        "validate_episode_script": (root / "scripts" / "validate_episode.py").exists(),
        "node": shutil.which("node") is not None,
        "npm": shutil.which("npm") is not None,
        "ffmpeg": shutil.which("ffmpeg") is not None,
        "ffprobe": shutil.which("ffprobe") is not None,
    }
    checks["ready_for_script"] = checks["creator_profile"] and checks["content_memory"]
    checks["ready_for_render"] = (
        checks["ready_for_script"]
        and checks["output_dir"]
        and (checks["remotion_project"] or checks["remotion_template"])
        and checks["node"]
        and checks["npm"]
        and checks["ffmpeg"]
        and checks["ffprobe"]
    )
    print(json.dumps(checks, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
