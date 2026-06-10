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
5. Generate captions from script lines using actual or estimated audio timing.

## Public Skill Packaging

Do not package local voice samples, cloned voices, speaker embeddings, or generated audio in the public skill repository.

