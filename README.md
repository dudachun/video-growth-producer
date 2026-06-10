# Video Growth Producer

`video-growth-producer` is a trainable Codex Skill for short-video production.

It helps a creator go from idea or script to:

- short-video topic and hook
- script and storyboard
- cover concept and cover image workflow
- captions and keyword highlights
- Remotion-based vertical video plan/render workflow
- optional imagegen visuals
- optional HyperFrames-enhanced scenes
- local voice workflow recommendation with CosyVoice
- performance review and future-content memory

The Skill is designed for Douyin, TikTok, Reels, YouTube Shorts, WeChat Channels, and similar vertical short-video platforms.

## What Makes It Different

This Skill is not locked to one niche.

Each user can train their own content direction through local profile files:

```text
profiles/default/
  creator-profile.yaml
  content-memory.md
  winning-patterns.md
  forbidden-patterns.md
  visual-style.md
  episode-ledger.jsonl
  performance-ledger.jsonl
```

For example, one creator can use it for AI tools, another for fitness, another for workplace skills, another for education, consulting, product promotion, or local services.

## Core Rule

The public repository contains only reusable workflow files, scripts, templates, and sample configuration.

It does **not** include:

- private voice samples
- cloned voice models
- generated voiceovers
- private creator profiles
- account screenshots
- performance data
- generated videos

Every creator should create their own local profile and configure their own voice workflow if they want AI voiceover.

## Install As A Codex Skill

Clone this repository into your Codex skills folder:

```bash
git clone https://github.com/<your-name>/video-growth-producer.git ~/.codex/skills/video-growth-producer
```

On Windows, the skills folder is usually:

```powershell
git clone https://github.com/<your-name>/video-growth-producer.git $env:USERPROFILE\.codex\skills\video-growth-producer
```

Then start a new Codex session and invoke:

```text
Use $video-growth-producer to initialize my short-video creator profile.
```

## Quick Start

Initialize a creator profile:

```bash
python scripts/init_creator_profile.py --profile default
```

Check workspace readiness:

```bash
python scripts/check_workspace.py --profile default
```

Then tell Codex:

```text
Use $video-growth-producer to help me create a short video for my niche.
```

Or provide a script directly:

```text
Use $video-growth-producer to turn this script into a vertical short-video plan, cover, captions, and Remotion render workflow:

<paste script here>
```

## Training Your Content Direction

You can change the content direction at any time.

Examples:

```text
以后我的内容方向改成老板 AI 落地，不做 Codex 工具推荐。
```

```text
以后开头不要先讲概念，要先给真实场景和结果。
```

```text
这个账号目标是吸引健身小白，最终转化私教课。
```

The Skill should update local memory files such as:

- `creator-profile.yaml`
- `content-memory.md`
- `winning-patterns.md`
- `forbidden-patterns.md`

## Video Generation Workflow

Default workflow:

1. Load creator profile and memory.
2. Generate or clean the script.
3. Build a visual plan.
4. Enforce the first 2s/5s retention rule.
5. Generate or prepare cover and scene assets.
6. Generate captions JSON.
7. Generate or import voiceover.
8. Render with Remotion.
9. Validate MP4 with `ffprobe`.
10. Record the episode and performance assumptions.

## First 2s / First 5s Rule

Short-video openings must show useful subject content immediately.

Do not waste the first seconds with only:

- atmosphere
- generic background
- title text
- logo animation

Good openings show:

- wrong way vs right way
- before and after
- real result proof
- product/interface preview
- concrete example
- data change
- finished output

For course or opinion videos, default to:

```text
wrong method vs correct method
```

For tool videos, default to:

```text
result proof first, tool name later
```

## Voice Workflow

The recommended local voice path is CosyVoice, configured by each creator in their own workspace.

This public repository does not ship any voice model or voice sample.

A creator can choose:

- local CosyVoice
- another TTS provider
- imported human-recorded audio
- silent preview
- a custom workflow

See:

```text
references/voice-cosyvoice.md
```

## Remotion

Remotion is the default video engine.

A minimal template is included:

```text
assets/remotion-template/
```

Use it as a starting point, or copy the Skill workflow into an existing Remotion project.

See:

```text
references/video-generation-remotion.md
```

## Useful Scripts

```text
scripts/init_creator_profile.py
scripts/check_workspace.py
scripts/create_caption_timeline.py
scripts/create_cover.py
scripts/validate_video.py
scripts/update_content_memory.py
scripts/update_performance_ledger.py
```

## Repository Structure

```text
video-growth-producer/
  SKILL.md
  README.md
  LICENSE
  agents/
  references/
  scripts/
  assets/
```

## Privacy Checklist Before Publishing

Before pushing your own fork or project workspace, make sure you do not commit:

- `profiles/`
- `voice_samples/`
- `voice_models/`
- `.generated/`
- `input/`
- `output/`
- `*.wav`
- `*.mp3`
- `*.mp4`
- account screenshots
- private performance ledgers

The included `.gitignore` already excludes common private/generated files.

## License

MIT
