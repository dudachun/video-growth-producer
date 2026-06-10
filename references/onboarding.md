# Onboarding

Use onboarding when the user has no creator profile, wants to install the workflow, or asks to initialize their account.

## Minimum Questions

Ask only what is needed:

- What niche or topic do you want to make videos about?
- Who should the videos attract?
- What is the goal: followers, leads, consulting, course sales, product sales, community, or brand?
- What style should the videos feel like: aggressive, friendly, expert, cinematic, practical, funny, calm?
- Do you want voiceover, silent preview, or bring your own audio/video?

## Initialize

Run:

```bash
python scripts/init_creator_profile.py --profile default
```

Then edit `profiles/default/creator-profile.yaml` from the user's answers.

## First Workspace

Recommended local folders:

```text
input/
output/
assets/
profiles/default/
remotion-video/
```

The public skill should not require this exact layout if the user's project already has equivalents.

