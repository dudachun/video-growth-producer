# Remotion Video Generation

Remotion is the default renderer. The publish workflow is manifest-driven.

## Modes

Use `strict` mode by default.

- `strict`: publish-quality output. Requires imagegen or an equivalent image generation capability.
- `remotion-only`: preview fallback only. Use it only after the user explicitly confirms the fallback. It may use Remotion UI, screenshots, official logos, and generated vector/layout elements, but it must not claim imagegen assets.

If the current agent cannot call imagegen, strict mode must stop before rendering.

## Required Order

1. Run `python scripts/doctor.py --mode strict --imagegen available`.
2. If imagegen is missing, stop and ask whether the user wants `remotion-only` preview mode.
3. Write or import the script.
4. Generate `visual_plan.json` before rendering.
5. In strict mode, generate required imagegen assets and copy them into the project assets/public folder.
6. Generate voice and run the opening ASR quality check.
7. Generate captions from real or approved timing.
8. Create `episode_manifest.json`.
9. Run `python scripts/export_manifest_to_remotion.py episode_manifest.json`.
10. Render with the Remotion template.
11. Generate a separate cover image.
12. Run `python scripts/validate_episode.py episode_manifest.json --mode strict`.

## Remotion Template

The template is in:

```text
assets/remotion-template/
```

It is driven by:

```text
assets/remotion-template/src/episode_manifest.ts
```

For a real episode, generate or update this file from the approved `episode_manifest.json` and `visual_plan.json`.

Hard-coded quality defaults:

- 1080x1920 vertical video.
- 30fps.
- Caption top position near 75%.
- White caption text, black shadow, no outline.
- Yellow keyword highlights.
- Main visual structure changes every 3-5 seconds.
- Opening 0-2 seconds must contain a subject-bearing layout.

## Default Commands

```bash
cd assets/remotion-template
npm install
npm run lint
npm run still
npm run render
cd ../..
python scripts/validate_episode.py episode_manifest.json --mode strict
```

## Visual Sync

Do not make a beautiful unrelated montage. Each visual beat must match the current script section:

```json
{
  "startSec": 0,
  "endSec": 4,
  "voice": "Most people prompt AI wrong.",
  "visualGoal": "Show wrong prompt vs clear requirement.",
  "layout": "wrong-right",
  "assetSource": "imagegen",
  "imagegenAsset": "assets/episode/opening-wrong-right.png",
  "motion": ["split reveal", "keyword pop"]
}
```

## Opening Voice QA

Before rendering the final MP4:

1. Export or locate the final narration audio.
2. Extract the first 5 seconds.
3. Run Whisper or another available ASR.
4. Compare it with the first script sentence.
5. If the first word, negation word, or core verb is wrong, do not render. Regenerate the voice or rewrite the first sentence, then check again.

## Optional HyperFrames

Use HyperFrames only when available and useful for richer animated web scenes. Remotion remains the final publish renderer unless the user explicitly chooses a validated HyperFrames-only pipeline.
