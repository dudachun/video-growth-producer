#!/usr/bin/env python3
"""Publish-quality validation for a generated short-video episode."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from validate_visual_plan import validate as validate_visual_plan  # noqa: E402


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def ffprobe(path: Path) -> dict:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,size",
        "-show_entries",
        "stream=index,codec_type,codec_name,width,height,avg_frame_rate",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def require_path(root: Path, raw_path: str | None, label: str, errors: list[str]) -> Path | None:
    if not raw_path:
        errors.append(f"missing {label} path")
        return None
    path = Path(raw_path)
    if not path.is_absolute():
        path = root / path
    if not path.exists():
        errors.append(f"{label} does not exist: {path}")
        return None
    return path


def validate_caption_file(path: Path, errors: list[str]) -> None:
    captions = load_json(path)
    if not isinstance(captions, list) or not captions:
        errors.append("caption file must be a non-empty array")
        return
    for index, caption in enumerate(captions):
        text = str(caption.get("text", "")).strip()
        start = caption.get("startMs")
        end = caption.get("endMs")
        if not text:
            errors.append(f"caption {index} has empty text")
        if not isinstance(start, int) or not isinstance(end, int) or end <= start:
            errors.append(f"caption {index} has invalid timing")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", choices=["strict", "remotion-only"])
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise SystemExit("manifest must be a JSON object")

    mode = args.mode or manifest.get("mode", "strict")
    errors: list[str] = []

    video_cfg = manifest.get("video") or {}
    width = int(video_cfg.get("width", 1080))
    height = int(video_cfg.get("height", 1920))
    fps = int(video_cfg.get("fps", 30))
    caption_top = float(video_cfg.get("captionTopPercent", 75))
    if width != 1080 or height != 1920:
        errors.append("publish template must output 1080x1920 vertical video")
    if fps != 30:
        errors.append("publish template must output 30fps")
    if not 73 <= caption_top <= 77:
        errors.append("captionTopPercent must stay near 75 to avoid platform title overlays")

    outputs = manifest.get("outputs") or {}
    video_path = require_path(root, outputs.get("video"), "output video", errors)
    cover_path = require_path(root, outputs.get("cover"), "output cover", errors)
    if cover_path and cover_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        errors.append("cover must be an image file")

    captions_cfg = manifest.get("captions") or {}
    captions_path = require_path(root, captions_cfg.get("path"), "captions", errors)
    highlight_terms = captions_cfg.get("highlightTerms") or []
    if not highlight_terms:
        errors.append("highlightTerms must include key terms for yellow caption emphasis")
    if captions_path:
        validate_caption_file(captions_path, errors)

    visual_plan_cfg = manifest.get("visualPlan") or {}
    visual_plan_path = require_path(root, visual_plan_cfg.get("path"), "visual plan", errors)
    if visual_plan_path:
        visual_plan = load_json(visual_plan_path)
        if isinstance(visual_plan, dict):
            errors.extend(validate_visual_plan(visual_plan, root, mode))
        else:
            errors.append("visual plan must be a JSON object")

    if mode == "strict":
        imagegen_assets = (manifest.get("assets") or {}).get("imagegen") or []
        if len(imagegen_assets) < 2:
            errors.append("strict mode requires at least two imagegen assets in manifest.assets.imagegen")
        for raw in imagegen_assets:
            require_path(root, raw, "imagegen asset", errors)

    voice = manifest.get("voice") or {}
    if voice:
        voice_path = require_path(root, voice.get("path"), "voice audio", errors)
        if voice_path and voice_path.suffix.lower() not in {".wav", ".mp3", ".m4a", ".aac"}:
            errors.append("voice audio has an unsupported extension")
        if voice.get("openingQaPassed") is not True:
            errors.append("voice.openingQaPassed must be true before publish render")

    if video_path:
        try:
            probe = ffprobe(video_path)
            streams = probe.get("streams", [])
            vstream = next((s for s in streams if s.get("codec_type") == "video"), None)
            astream = next((s for s in streams if s.get("codec_type") == "audio"), None)
            if not vstream:
                errors.append("output video has no video stream")
            else:
                if vstream.get("width") != width or vstream.get("height") != height:
                    errors.append(f"output dimensions are {vstream.get('width')}x{vstream.get('height')}, expected {width}x{height}")
                if vstream.get("avg_frame_rate") != f"{fps}/1":
                    errors.append(f"output fps is {vstream.get('avg_frame_rate')}, expected {fps}/1")
            if not astream:
                errors.append("output video has no audio stream")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"ffprobe failed: {exc}")

    result = {"ok": not errors, "manifest": str(manifest_path), "mode": mode, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
