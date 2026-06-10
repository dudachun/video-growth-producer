# Cover System

Use generated or captured visuals as backgrounds. Add final title text locally to avoid malformed Chinese or brand text.

## Workflow

1. Decide cover promise from the hook.
2. Generate or choose a 3:4 or 9:16 background image.
3. Keep background text-free when using imagegen.
4. Use `scripts/create_cover.py` for title layout.
5. Export a cover image separately from the video.

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

