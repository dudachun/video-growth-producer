#!/usr/bin/env python3
"""Export episode_manifest.json + visual_plan.json + captions.json into Remotion TS data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(root: Path, raw_path: str) -> dict | list:
    path = Path(raw_path)
    if not path.is_absolute():
        path = root / path
    return json.loads(path.read_text(encoding="utf-8-sig"))


def public_path(raw_path: str | None) -> str | None:
    if not raw_path:
        return None
    return raw_path.replace("\\", "/")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="assets/remotion-template/src/episode_manifest.ts")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))

    visual_plan_ref = manifest.get("visualPlan", {}).get("path")
    captions_ref = manifest.get("captions", {}).get("path")
    if not visual_plan_ref:
        raise SystemExit("manifest.visualPlan.path is required")
    if not captions_ref:
        raise SystemExit("manifest.captions.path is required")

    visual_plan = load_json(root, visual_plan_ref)
    captions = load_json(root, captions_ref)
    if not isinstance(visual_plan, dict):
        raise SystemExit("visual plan must be a JSON object")
    if not isinstance(captions, list):
        raise SystemExit("captions must be a JSON array")

    remotion_manifest = {
        "mode": manifest.get("mode", "strict"),
        "episodeId": manifest.get("episodeId", "episode"),
        "title": manifest.get("title", "Untitled"),
        "seriesName": manifest.get("seriesName", "Video Growth Producer"),
        "video": {
            "width": manifest.get("video", {}).get("width", 1080),
            "height": manifest.get("video", {}).get("height", 1920),
            "fps": manifest.get("video", {}).get("fps", 30),
            "durationSec": manifest.get("video", {}).get("durationSec", 45),
            "captionTopPercent": manifest.get("video", {}).get("captionTopPercent", 75),
            "captionFont": manifest.get("video", {}).get("captionFont", "Noto Serif SC"),
            "captionHighlightColor": manifest.get("video", {}).get("captionHighlightColor", "#ffd84d"),
        },
        "voice": {
            "path": public_path(manifest.get("voice", {}).get("path")),
            "speed": manifest.get("voice", {}).get("speed", 1.2),
            "openingQaPassed": manifest.get("voice", {}).get("openingQaPassed", False),
        },
        "bgm": {
            "path": public_path(manifest.get("bgm", {}).get("path")),
            "volume": manifest.get("bgm", {}).get("volume", 0.18),
        },
        "captions": {
            "highlightTerms": manifest.get("captions", {}).get("highlightTerms", []),
            "data": captions,
        },
        "visualPlan": {
            "beats": visual_plan.get("beats", []),
        },
    }

    if not remotion_manifest["voice"]["path"]:
        remotion_manifest.pop("voice")
    if not remotion_manifest["bgm"]["path"]:
        remotion_manifest.pop("bgm")

    out = Path(args.out)
    if not out.is_absolute():
        out = root / out
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(remotion_manifest, ensure_ascii=False, indent=2)
    out.write_text(
        'import type { EpisodeManifest } from "./types";\n\n'
        f"export const episodeManifest = {payload} satisfies EpisodeManifest;\n",
        encoding="utf-8",
    )
    print(f"remotion_manifest={out.resolve()}")


if __name__ == "__main__":
    main()
