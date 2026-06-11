#!/usr/bin/env python3
"""Validate visual-plan quality gates before rendering."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STRICT_MIN_IMAGEGEN = {
    "single-topic": 2,
    "single-tool": 2,
    "three-tool": 3,
    "big-project": 5,
    "custom": 2,
}

SUBJECT_LAYOUTS = {"impact-open", "wrong-right", "compare", "proof", "screen-demo", "asset-focus"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate(plan: dict, root: Path, mode: str | None = None) -> list[str]:
    errors: list[str] = []
    actual_mode = mode or plan.get("mode", "strict")
    scope = plan.get("scope", "custom")
    beats = plan.get("beats") or []
    imagegen_assets = plan.get("imagegenAssets") or []

    if actual_mode not in {"strict", "remotion-only"}:
        fail("mode must be strict or remotion-only", errors)

    if not beats:
        fail("visual plan has no beats", errors)
        return errors

    first = beats[0]
    if abs(float(first.get("startSec", -1))) > 0.01:
        fail("first beat must start at 0s", errors)

    first2 = [b for b in beats if float(b.get("startSec", 999)) < 2 and float(b.get("endSec", 0)) > 0]
    first5 = [b for b in beats if float(b.get("startSec", 999)) < 5 and float(b.get("endSec", 0)) > 0]
    if not any(b.get("layout") in SUBJECT_LAYOUTS for b in first2):
        fail("0-2s must use a subject-bearing layout, not an empty title/background", errors)
    if not any(b.get("visualGoal") and (b.get("bullets") or b.get("asset") or b.get("imagegenAsset")) for b in first5):
        fail("0-5s must include concrete value: visualGoal plus bullets/asset/imagegenAsset", errors)

    opening = plan.get("openingContract") or {}
    if opening.get("first2SecHasSubject") is not True:
        fail("openingContract.first2SecHasSubject must be true", errors)
    if opening.get("first5SecHasConcreteValue") is not True:
        fail("openingContract.first5SecHasConcreteValue must be true", errors)

    previous_layout = None
    for index, beat in enumerate(beats):
        start = float(beat.get("startSec", -1))
        end = float(beat.get("endSec", -1))
        if end <= start:
            fail(f"beat {index} endSec must be greater than startSec", errors)
        if not beat.get("motion"):
            fail(f"beat {index} must declare at least one motion cue", errors)
        if previous_layout and previous_layout == beat.get("layout"):
            fail(f"beat {index} repeats the previous layout; vary adjacent layouts", errors)
        previous_layout = beat.get("layout")

    if actual_mode == "strict":
        required_count = STRICT_MIN_IMAGEGEN.get(scope, 2)
        required_assets = [a for a in imagegen_assets if a.get("required", True)]
        if len(required_assets) < required_count:
            fail(f"strict mode requires at least {required_count} required imagegen assets for scope={scope}", errors)
        for asset in required_assets:
            asset_path = asset.get("path")
            if asset_path and not (root / asset_path).exists():
                fail(f"required imagegen asset is missing: {asset_path}", errors)
        if not any(b.get("assetSource") == "imagegen" or b.get("imagegenAsset") for b in beats):
            fail("strict mode visual beats must use imagegen assets", errors)
    else:
        if imagegen_assets:
            fail("remotion-only mode should not claim imagegen assets; use generated-ui, official, or screenshot assets", errors)

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("visual_plan")
    parser.add_argument("--root", default=".")
    parser.add_argument("--mode", choices=["strict", "remotion-only"])
    args = parser.parse_args()

    root = Path(args.root).resolve()
    plan_path = Path(args.visual_plan)
    plan = load_json(plan_path)
    errors = validate(plan, root, args.mode)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    print(json.dumps({"ok": True, "visual_plan": str(plan_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
