---
name: video-growth-producer
description: Trainable strict short-video production workflow for Douyin, TikTok, Reels, YouTube Shorts, WeChat Channels, or similar platforms. Use when the user asks to generate short-video topics, hooks, scripts, storyboards, covers, captions, voiceover plans, Remotion videos, required imagegen visual assets, HyperFrames enhancements, or to review video performance screenshots/data and improve future content direction. Also use when the user wants to initialize or train a creator-specific content profile.
---

# Video Growth Producer

Turn an idea, script, or performance screenshot into a trainable short-video production workflow.

## Core Rule

Separate the public skill from each creator's private profile.

- Public skill files contain workflows, scripts, schemas, templates, and sample configs only.
- Creator-specific voice samples, voice models, generated audio, input videos, output videos, account data, and performance ledgers live outside the public skill or under ignored local profile/workspace folders.
- Do not assume a built-in voice profile. Check local config and ask the user how they want voice handled when needed.

## Mode Rule

Default to `strict` mode for publish-ready videos.

- `strict`: publish-quality mode. It requires imagegen or an equivalent image generation capability.
- `remotion-only`: preview fallback. Use it only after the user explicitly confirms the fallback.

If the current agent cannot generate images, do not render a publish-ready video. Tell the user the skill cannot run in strict mode without imagegen, and ask whether they want to install/enable imagegen or continue with `remotion-only` preview.

Do not silently downgrade strict mode.

## First Decision

Classify the user request:

- **Initialize**: create a creator profile or workspace.
- **Train direction**: update audience, niche, style, forbidden patterns, winning patterns, or performance memory.
- **Script**: generate or revise a topic/hook/script.
- **Video**: generate image assets, captions, voice, cover, manifest, and a Remotion video from a script.
- **Review**: analyze metrics/screenshots and update the next-video strategy.

## Required Workspace Checks

Before generating a video, inspect or create:

```text
profiles/default/creator-profile.yaml
profiles/default/content-memory.md
profiles/default/winning-patterns.md
profiles/default/forbidden-patterns.md
profiles/default/visual-style.md
profiles/default/episode-ledger.jsonl
profiles/default/performance-ledger.jsonl
```

Run or adapt:

```bash
python scripts/init_creator_profile.py --profile default
python scripts/check_workspace.py --profile default
```

Before a publish render, run:

```bash
python scripts/doctor.py --mode strict --imagegen available
```

Only pass `--imagegen available` when the current agent can actually call imagegen or an equivalent image generation tool. If this is not true, strict mode is blocked.

## Production Workflow

For "make a video" requests:

1. Load the creator profile and content memory.
2. Decide mode. Default to `strict`; use `remotion-only` only after explicit user confirmation.
3. Run `doctor.py`.
4. If no script is provided, write one in the creator's trained direction.
5. Build `visual_plan.json` before rendering.
6. Enforce the opening retention rule: the first 2 seconds need a visible subject demo, result proof, concrete example, or before/after comparison; the first 5 seconds must make the problem and value obvious.
7. In strict mode, generate required imagegen assets for the opening, key scenes, and cover background. Copy generated assets into the project. Do not leave them only in a global generated-images folder.
8. Generate or import voice according to local creator config. CosyVoice is the recommended local default when configured.
9. Before rendering, quality-check the opening voiceover: extract the first 5 seconds, transcribe it with Whisper or another available ASR, and compare it with the first script sentence. If the first word, negation word, or core verb is wrong, rewrite or regenerate the opening voice before continuing.
10. Create captions from approved timing. Captions must be near 75% from the top, white with black shadow, no outline, and important terms in yellow.
11. Create `episode_manifest.json`.
12. Render with the Remotion template.
13. Export the cover separately. Add title text locally instead of asking imagegen to draw Chinese or brand text.
14. Run `validate_episode.py`. Do not deliver the video as complete unless validation passes.
15. Write the episode record and any predictions or assumptions.

## Quality Gates

Strict publish mode must pass all gates:

- 1080x1920 vertical MP4, 30fps, H.264 + AAC.
- Separate cover image exists.
- `visual_plan.json` exists and passes `validate_visual_plan.py`.
- `episode_manifest.json` exists and passes `validate_episode.py`.
- At least the required number of imagegen assets exists in strict mode.
- 0-2 seconds has a subject-bearing layout.
- 0-5 seconds has concrete value, proof, comparison, or example.
- Captions are synchronized, near 75% vertical position, and include yellow key terms.
- Opening voice QA passed.

## References

Load only the relevant reference:

- `references/strict-production.md`: strict mode, imagegen requirement, and remotion-only fallback.
- `references/onboarding.md`: first-run setup and profile initialization.
- `references/creator-profile.md`: profile schema and trainable memory files.
- `references/content-training.md`: how to update direction from user feedback.
- `references/script-system.md`: hooks, scripts, structure, and niche adaptation.
- `references/retention-rules.md`: first 2s/5s rules and visual proof standards.
- `references/cover-system.md`: imagegen cover workflow and local title layout.
- `references/video-generation-remotion.md`: Remotion rendering workflow and template use.
- `references/voice-cosyvoice.md`: local CosyVoice recommendation and config pattern.
- `references/performance-review.md`: reviewing analytics and updating memory.

## Scripts

- `scripts/init_creator_profile.py`: create a local trainable creator profile.
- `scripts/check_workspace.py`: inspect profile, assets, tools, and output folders.
- `scripts/doctor.py`: enforce strict/remotion-only capability checks.
- `scripts/create_caption_timeline.py`: create Remotion-compatible caption JSON from a script and duration.
- `scripts/create_cover.py`: compose a title cover over a generated/background image.
- `scripts/export_manifest_to_remotion.py`: export JSON manifest, captions, and visual plan into the Remotion template.
- `scripts/validate_visual_plan.py`: check opening, motion, layout, and imagegen requirements.
- `scripts/validate_video.py`: low-level ffprobe validation wrapper.
- `scripts/validate_episode.py`: publish-quality manifest, asset, caption, cover, voice, and ffprobe validation.
- `scripts/update_content_memory.py`: append direction changes, wins, and forbidden patterns.
- `scripts/update_performance_ledger.py`: append analytics records.

## Bundled Assets

- `assets/remotion-template/`: manifest-driven Remotion production template.
- `assets/cover-template/`: cover prompt pattern.
- `assets/sample-config.yaml`: strict production defaults.
- `assets/sample-creator-profile.yaml`: profile defaults.
- `schemas/episode_manifest.schema.json`: episode manifest contract.
- `schemas/visual_plan.schema.json`: visual plan contract.

## Defaults

- Video engine: Remotion.
- Required image generator for publish mode: imagegen or equivalent.
- Optional visual enhancer: HyperFrames.
- Recommended local voice path: CosyVoice, configured per creator profile.
- Default output: 9:16 vertical MP4, 1080x1920, 30fps, H.264 + AAC, plus a separate 3:4 cover image.
- Default platform logic: optimize for short-video cold-start retention.

## When Publishing Or Sharing

Before committing or uploading, verify that the repository does not contain:

- voice samples, cloned voices, speaker embeddings, or generated voiceover files;
- generated MP4/MOV files;
- private account screenshots or performance data;
- local absolute paths from the creator's machine;
- private creator profiles unless explicitly intended as sanitized samples.
