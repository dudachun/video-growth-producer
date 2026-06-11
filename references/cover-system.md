# Cover System

Use generated or captured visuals as backgrounds. Add final title text locally to avoid malformed Chinese or brand text.

Every publish-ready video must include a separate cover image unless the user explicitly asks to skip it.

In strict mode, the cover background should be generated with imagegen or an equivalent image generation tool. Add final Chinese title text locally to avoid malformed text.

## Workflow

1. Decide cover promise from the hook.
2. In strict mode, generate a 3:4 background image with imagegen. In remotion-only preview mode, use a clearly labeled generated-ui or screenshot fallback.
3. Keep background text-free when using imagegen.
4. Use `scripts/create_cover.py` for title layout.
5. Export a cover image separately from the video.
6. Add the cover path to `episode_manifest.json`.
7. Validate that the cover file exists, the title is readable, and the visual promise matches the first 5 seconds of the video.

## Cover Prompt Pattern

```text
Create a high-retention short-video cover background.
No readable text. Leave clean space for a large title.
Use the creator's style: <style>.
Subject: <visual metaphor/result/proof>.
Avoid: logos, watermarks, malformed text.
```

## Title Rules

- Large promise title.
- One short subheading or badge.
- Strong contrast.
- Do not place important text under platform UI areas.
- Default filename: `output/<date>_<slug>_cover.png`.
