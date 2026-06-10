# Content Training

Training means updating profile memory, not fine-tuning a model.

## User Feedback Types

Map feedback into durable files:

- "Do more like this" -> `winning-patterns.md`
- "Never do this again" -> `forbidden-patterns.md`
- "Change my direction/audience/offer/style" -> `creator-profile.yaml`
- "This script format works" -> `content-memory.md`
- "This video data performed well/poorly" -> `performance-ledger.jsonl`

## Update Rules

- Preserve the user's exact preference when possible.
- Add a timestamp and example.
- Prefer specific rules over vague mood notes.
- When a rule conflicts with older memory, mark the older rule as superseded instead of silently deleting it.

## Example

User says:

```text
以后不要先介绍工具名，先讲真实场景。
```

Append:

```markdown
## 2026-06-10

- Do not open with tool names or definitions.
- Start with a real scene, visible result, or before/after contrast.
```

