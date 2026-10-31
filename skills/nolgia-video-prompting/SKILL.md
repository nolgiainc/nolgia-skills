---
name: nolgia-video-prompting
description: "Directing craft for NOLGIA video generation: shot grammar, the breathing pattern, multi-shot sequencing, character and location consistency with reference images, per-shot sound design, and the iteration process (keep approved shots, regenerate only what failed). Use when: writing or fixing video prompts, planning a multi-clip production, a short film, a trailer or a music video on NOLGIA, or deciding which shots to regenerate. NOT for: platform mechanics such as auth, flags, jobs and credits (use nolgia-platform), vertical UGC ad pipelines (use nolgia-ugc-ads), or still-image prompting."
version: 1.4.0
author: NOLGIA
license: MIT
metadata:
  tags: [nolgia, video-prompting, directing, seedance, minimax-h3, multi-shot, filmmaking]
  related_skills: [nolgia-platform, nolgia-ugc-ads]
---

# NOLGIA Video Prompting

Distilled from producing complete short films on the platform. Two layers:
what to put in a prompt, and how to run a multi-clip production without
burning credits.

## Prompt anatomy (one shot)

```
<SHOT SIZE>. <subject + one action>. <environment, time, weather>.
<camera: lens/movement>. <film stock / grade>. AUDIO: <sound design>.
```

Example: *WIDE SHOT. A rust-flecked hatchback moves south on an empty
two-lane highway through flat farmland. Late afternoon, overcast gray sky.
Static camera, 35mm feel, fine film grain and a print stock look. AUDIO: car
engine, wind, distant birds, natural ambient.*

Grade in post, not in the prompt: on Seedance 2.5 never paste film stock or
camera brand names, and on any model never describe lens artifacts as things
in the frame ("streak flares", "barrel distortion" and "vignette corners"
render as overlays). Pick the stock as a Studio color preset
(`nolgia color-presets list`: 500T for night interiors, 250D for day, the 2383
print finish over either).

Rules that survived production:
- **One action per shot.** Two actions = the model picks one or morphs.
- **Repeat exact wording** for wardrobe/props/locations in every prompt
  that shows them ("olive field jacket with tear at left elbow" —
  verbatim, every time). Paraphrasing = drift.
- **Describe action only in image-to-video** — the reference image already
  carries character and environment; re-describing them fights it.
- **No text in generated frames.** Models garble it; burn text in post.
- **≤3 characters per shot**, close-up references beat distant ones.

## Scripted films: the workflow, not shot-by-shot prompts

A short film, skit, trailer or narrative ad where people act or speak is never
made by sending each line of a shot list to `nolgia gen video`. That is how an
in-house short came out looking like AI (2026-10-31). The order that works:

1. **Story first**: logline, scene list, the script with every spoken line.
2. **Cast and world as locked assets**: one photoreal portrait per character
   (each view its own image, never an expression grid as the identity
   reference), saved with `nolgia characters create`; empty location plates
   from a three-quarter angle, never frontal, one plate per lighting state.
3. **Storyboard**: one keyframe still per shot built from those references
   (`gpt-image-2`, up to four references), watched as an animatic before any
   video. A look on one element only (a black-and-white character in a color
   room) is built into these stills.
4. **Image to video from the approved keyframe.** Speaking or scene-carrying
   people on `minimax-h3` (native lip-synced speech); its start frame cannot be
   combined with `--element` or `--character-id`, so the keyframe carries
   identity and the description is restated in words. Action, vehicles and
   creatures on Seedance 2.5; never Seedance for lifelike humans.
5. **Natural takes, cut in the edit**: calm scenes 3–4s a shot, tense 1.5–2s,
   continuous takes cut in a Studio composition, never 1-second slices of
   separate generations. Short prompts: who, one action, timed beats, the
   exact line, the sound.
6. **Post**: grade with a Studio color preset, one mix with the dialogue on
   top, and titles only: no burned dialogue captions on a film.

## The breathing pattern (multi-shot sequencing)

Every cut changes shot size: WIDE (establish) → MEDIUM (observe) →
CLOSE-UP (feel) → WIDE (release). Never two adjacent shots at the same
distance. Vary pacing: calm scenes 3–4s/shot, tense 1.5–2s, danger <1s.
After every discovery, a half-second reaction beat on the protagonist —
reaction shots ARE the story. Never cut directly into a key moment: show
approach → threshold → reaction → event.

```bash
nolgia gen video --model fal-ai/bytedance/seedance/v2/pro/text-to-video \
  --prompt "Cinematic 35mm horror, muted palette." --generate-audio true \
  --shot "5:WIDE SHOT. Abandoned radio station at dusk, one lit window.|wind, a loose sign creaks" \
  --shot "4:MEDIUM. Maya at the threshold, hand on the door, listening.|her breath, faint static inside" \
  --shot "3:CU. Her face as the static resolves into a voice.|static becomes a whispered name"
```

## Consistency: reference images first

Generate character portraits and location plates ONCE (`nolgia gen image`),
then anchor every clip with `--input maya.png` on a model that takes a start
image (`minimax-h3`, or the Seedance 2.0 Pro image-to-video id; `nolgia
models get <model>` says which do). Save a recurring subject as a character
(`nolgia characters create`) and pass `--character-id` so every still and
clip carries the same reference and description. For multi-angle
characters, stitch a reference sheet into a single image. Consistency
drift is the #1 defect in multi-clip work — lock refs before writing a
single shot.

## Sound is written into the shot

Every shot carries an AUDIO direction (the `|audio` part of `--shot`, or
an `AUDIO:` sentence). Silence is a direction too ("total silence" is the
strongest cut in the toolbox). Audio-as-afterthought produces cuts that
feel aggressive and unmotivated.

## The iteration loop (protects credits and quality)

1. Draft cheap: `veo-3.1-lite` or `veo-3.1-fast`, lowest tier (compare
   prices with `nolgia models list --modality video` or `--cost-only`).
2. Review each clip: **KEEP / FIX / CUT** — write it down.
3. **Never regenerate a KEEP.** Regenerate only FIX shots, changing one
   variable at a time (prompt sentence, seed, or ref — not all three).
4. Reuse a fixed `--seed` when re-rolling composition so only your change
   moves.
5. Final pass on the premium model only for shots that earned it.

The classic failure: regenerating everything each round because feedback
touched some shots. Approved clips are assets — edit around them.

## Assemble the finished cut

Individual clips are not a film. Once the shots are approved, sequence them
into one rendered video with a Studio composition (see the `nolgia-platform`
skill): `nolgia compositions create --name <n> --clip <shot1> --clip <shot2>
… --render --wait`. Clips play in the order given, each clip's audio is kept
(`--mute` to drop it). Do not report the production done until that render
succeeds and you can name the finished asset — a project folder full of
clips is not the deliverable.
