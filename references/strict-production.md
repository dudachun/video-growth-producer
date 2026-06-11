# Strict Production Mode

Strict mode is the default mode for publish-ready videos.

## Non-Negotiable Rule

Strict mode requires imagegen or an equivalent image generation tool. If the current agent cannot generate images, stop before rendering and tell the user:

```text
当前 Agent 没有图片生成能力，不能使用 video-growth-producer 的发布级视频流程。
你可以安装/启用 imagegen，或者明确选择 remotion-only 预览模式。
```

Do not silently downgrade to a lower-quality video.

## Remotion-Only Preview

Only use this fallback when the user explicitly confirms it.

Allowed:

- Remotion UI panels.
- Text cards.
- Official logos.
- Screenshots supplied by the user or captured by the agent.
- Generated vector-like UI inside Remotion.

Not allowed:

- Claiming that imagegen assets were generated.
- Calling the output publish-quality when imagegen is missing.
- Skipping captions, cover, first-2-second subject, or visual-plan validation.

Use an output name with `_preview` or `_remotion_only` when possible.

## Publish Gates

Before final delivery, run:

```bash
python scripts/validate_visual_plan.py visual_plan.json --mode strict
python scripts/validate_episode.py episode_manifest.json --mode strict
```

The episode is not complete until both pass.
