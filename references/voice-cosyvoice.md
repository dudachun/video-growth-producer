# Voice With CosyVoice

CosyVoice is the recommended local voice option when configured.

## Config Pattern

Store voice settings in the creator profile:

```yaml
voice:
  provider: cosyvoice
  profile_id: my_voice
  model_dir: ""
  sample_dir: voice_samples/
  output_dir: .generated/audio/
  speed: 1.2
  fallback: ask
```

## Workflow

1. Check the local profile for `voice.provider`.
2. If CosyVoice is configured, use the local generator script/project available in that user's workspace.
3. If not configured, ask whether to configure voice, use another TTS path, use imported audio, or make a silent preview.
4. After voice generation, use `ffprobe` to get exact duration.
5. Extract the first 5 seconds and transcribe it with Whisper or another available ASR.
6. Compare the ASR result with the first script sentence. The first word, negation word, and core verb must be correct before rendering.
7. If the opening is mispronounced or mis-synthesized, regenerate the audio or rewrite the first sentence into a more stable sentence order.
8. Generate captions from script lines using actual or estimated audio timing.

## Opening QA Rule

The opening sentence needs separate quality control because short-video retention is decided in the first seconds and TTS can mis-synthesize short negation openings.

Examples of fragile openings:

- `Don't stop...`
- `Don't rush...`
- `Do not...`
- Chinese equivalents such as `别再...`, `不要再...`, `别先...`

When this happens, prefer a more stable rewrite:

```text
Original: Don't rush to study the installation tutorial when someone shares a Codex Skill.
Safer: When someone shares a Codex Skill, don't rush to study the installation tutorial first.
```

## Public Skill Packaging

Do not package local voice samples, cloned voices, speaker embeddings, or generated audio in the public skill repository.
