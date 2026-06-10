#!/usr/bin/env python3
"""Validate an MP4 with ffprobe."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--expect-width", type=int, default=1080)
    parser.add_argument("--expect-height", type=int, default=1920)
    parser.add_argument("--expect-fps", default="30/1")
    args = parser.parse_args()

    video = Path(args.video)
    if not video.exists():
        raise SystemExit(f"missing video: {video}")

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
        str(video),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not video_stream:
        raise SystemExit("no video stream")
    if not audio_stream:
        raise SystemExit("no audio stream")
    if video_stream.get("width") != args.expect_width or video_stream.get("height") != args.expect_height:
        raise SystemExit(f"unexpected dimensions: {video_stream.get('width')}x{video_stream.get('height')}")
    if video_stream.get("avg_frame_rate") != args.expect_fps:
        raise SystemExit(f"unexpected fps: {video_stream.get('avg_frame_rate')}")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()

