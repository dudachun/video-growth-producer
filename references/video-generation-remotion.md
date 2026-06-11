# Remotion Video Generation

Remotion is the default video engine.

## Build Steps

1. Create or update a Remotion project.
2. Copy assets into `public/`.
3. Generate captions JSON.
4. Create a composition with 1080x1920, 30fps by default.
5. Use timeline beats based on caption/audio timing.
6. Before rendering, transcribe the first 5 seconds of the final voice track and confirm it matches the first script sentence.
7. Render MP4.
8. Validate with `scripts/validate_video.py`.

## Default Commands

```bash
npm run lint
npx remotion still src/index.ts <CompositionId> output/check_05s.png --frame=150 --scale=0.35
npx remotion render src/index.ts <CompositionId> output/final.mp4 --codec=h264 --crf=18
python scripts/validate_video.py output/final.mp4
```

## Visual Sync

Do not make a beautiful unrelated montage. Each beat should match the current script section:

```json
{
  "startSec": 0,
  "endSec": 5,
  "voice": "Most people prompt AI wrong.",
  "visualGoal": "Show wrong prompt vs clear requirement.",
  "layout": "wrong-vs-right"
}
```

## Opening Voice QA

Before rendering the final MP4:

1. Export or locate the final narration audio.
2. Extract the first 5 seconds.
3. Run Whisper or another available ASR.
4. Compare the result with the first script sentence.
5. If the first word, negation word, or core verb is wrong, do not render. Regenerate the voice or rewrite the first sentence, then check again.

This rule is mandatory because a wrong first sentence damages the first 2-second and first 5-second retention window.

## Optional HyperFrames

Use HyperFrames when the user wants richer animated web compositions or HTML-based scenes. Render final video through Remotion unless the local HyperFrames pipeline is already validated.
