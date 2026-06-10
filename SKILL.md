---
name: video-growth-producer
description: Trainable short-video growth production workflow for Douyin, TikTok, Reels, YouTube Shorts, WeChat Channels, or similar platforms. Use when the user asks to generate short-video topics, hooks, scripts, storyboards, covers, captions, voiceover plans, Remotion videos, imagegen visual assets, HyperFrames enhancements, or to review video performance screenshots/data and improve future content direction. Also use when the user wants to initialize or train a creator-specific content profile.
---

# Video Growth Producer

Use this skill to turn an idea, script, or performance screenshot into a trainable short-video production workflow.

## Core Rule

Separate the public skill from each creator's private profile.

- Public skill files contain workflows, scripts, templates, and sample configs only.
- Creator-specific voice samples, voice models, generated audio, input videos, output videos, account data, and performance ledgers live outside the public skill or under ignored local profile/workspace folders.
- Do not assume a built-in voice profile. Check local config and ask the user how they want voice handled when needed.

## First Decision

Classify the user request:

- **Initialize**: create a creator profile or workspace.
- **Train direction**: update audience, niche, style, forbidden patterns, winning patterns, or performance memory.
- **Script**: generate or revise a topic/hook/script.
- **Video**: generate assets, captions, voice, and a Remotion video from a script.
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

If the user already has a project structure, map these files to the local equivalent instead of duplicating data.

## Production Workflow

For "make a video" requests:

1. Load the creator profile and content memory.
2. If no script is provided, write one in the creator's trained direction.
3. Build a visual plan before rendering.
4. Enforce the opening retention rule: the first 2 seconds need a visible subject demo, result proof, concrete example, or before/after comparison; the first 5 seconds must make the problem and value obvious.
5. Generate or locate cover/background assets. Use imagegen for non-logo visuals when available.
6. Create captions with highlighted keywords.
7. Generate or import voice according to the local creator config. CosyVoice is the recommended local default when configured.
8. Render with Remotion by default. HyperFrames is optional for enhanced animated scenes.
9. Validate the MP4 with ffprobe.
10. Write the episode record and any predictions or assumptions.

## References

Load only the relevant reference:

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
- `scripts/check_workspace.py`: inspect profile, assets, voice config, and output folders.
- `scripts/create_caption_timeline.py`: create Remotion-compatible caption JSON from a script and duration.
- `scripts/create_cover.py`: compose a title cover over a generated/background image.
- `scripts/validate_video.py`: ffprobe validation wrapper.
- `scripts/update_content_memory.py`: append direction changes, wins, and forbidden patterns.
- `scripts/update_performance_ledger.py`: append analytics records.

## Defaults

- Video engine: Remotion.
- Optional visual enhancer: HyperFrames.
- Optional image generator: imagegen.
- Recommended local voice path: CosyVoice, configured per creator profile.
- Default output: 9:16 vertical MP4, 1080x1920, 30fps, H.264 + AAC.
- Default platform logic: optimize for short-video cold-start retention.

## When Publishing Or Sharing

Before committing or uploading, verify that the repository does not contain:

- voice samples, cloned voices, speaker embeddings, or generated voiceover files;
- generated MP4/MOV files;
- private account screenshots or performance data;
- local absolute paths from the creator's machine;
- private creator profiles unless explicitly intended as sanitized samples.
