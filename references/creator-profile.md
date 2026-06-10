# Creator Profile

Each creator trains the skill through local profile files.

## Files

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

## creator-profile.yaml

Example:

```yaml
profile_name: default
series_name: ""
niche: ""
audience: ""
content_goal: ""
offer_or_conversion: ""
tone: ""
platforms:
  - douyin
  - video_channels
default_duration_sec: 45
video_engine: remotion
optional_enhancers:
  imagegen: true
  hyperframes: false
voice:
  provider: cosyvoice
  profile_id: ""
  fallback: ask
style:
  visual_mode: light-tech
  caption_position: 75%
  keyword_highlight: yellow
```

## Use

Before writing or rendering, read:

1. `creator-profile.yaml`
2. `content-memory.md`
3. `winning-patterns.md`
4. `forbidden-patterns.md`
5. recent `episode-ledger.jsonl` and `performance-ledger.jsonl`

