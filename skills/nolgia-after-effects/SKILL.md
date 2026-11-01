---
name: nolgia-after-effects
description: "Finish NOLGIA work in Adobe After Effects on the user's own computer through NOLGIA for Adobe, the NOLGIA plugin in After Effects: open a NOLGIA Studio composition in After Effects through its build.jsx export, read and change comps with ExtendScript, render check frames, bring NOLGIA library media into a project and send the finished render back to the NOLGIA library. Use when: the user has After Effects with NOLGIA for Adobe and asks to 'open my Studio edit in After Effects', 'finish this in AE', 'add motion graphics to my NOLGIA video', or 'get my AE render into NOLGIA'. NOT for: generating media (use nolgia-platform), Premiere Pro, Illustrator, Photoshop, Blender or DaVinci Resolve (each has its own NOLGIA plugin), or scripting After Effects from outside the plugin."
version: 1.10.0
author: NOLGIA
license: MIT
metadata:
  tags: [nolgia, after-effects, motion-graphics, mcp, desktop, plugin, studio-export, jsx]
  related_skills: [nolgia-platform]
---

# NOLGIA + After Effects (desktop)

Three pieces:

- **After Effects** (2024 to 2026, macOS or Windows), licensed and installed
  by the user.
- **NOLGIA for Adobe**, the NOLGIA plugin in After Effects (one install also
  covers Premiere Pro and Illustrator): it runs every command in After
  Effects and shows each one in its Activity list.
- **Your agent connected to NOLGIA**: the NOLGIA MCP server
  (`https://mcp.nolgia.ai/mcp`) gives it the `nolgia_app_*` tools, or the
  `nolgia` CLI (see nolgia-platform) sends the same commands with
  `nolgia api` (the Desktop apps guide, below).

NOLGIA Agent at nolgia.ai/agent works in After Effects through the same
plugin, so the person never needs to leave NOLGIA; this skill is for an
agent the person runs themselves.

NOLGIA Studio's **Export for editing > After Effects** writes a `build.jsx`
script that rebuilds a Studio edit as a native After Effects comp.

## Setup (once)

1. Install NOLGIA for Adobe from https://nolgia.ai/plugins/after-effects.
2. In After Effects open **Window > Extensions > NOLGIA**, click **Sign in**,
   check that the code matches on the page that opens and click **Connect**.
   Keep **Connected** on.
3. Connect your agent to NOLGIA (https://nolgia.ai/mcp), or sign in the CLI
   with `nolgia auth login`.
4. Check: `nolgia_app_status` (or `nolgia api GET /bridge/sessions`) lists
   After Effects on this computer.

## Only through the plugin

Drive After Effects only through the NOLGIA plugin. Never script it from
outside: no AppleScript or `osascript`, no `DoScript`, no COM, no Windows UI
automation, no simulated keystrokes or clicks, and no other local After
Effects MCP server that scripts the app from outside. Those skip the
person's Activity list, **Ask before running code** and the plugin's error
handling, and a bad call that way can crash After Effects and lose unsaved
work: one malformed AppleScript command crashed it in testing.

## Open a Studio composition in After Effects

1. Find the composition: `nolgia compositions list` (or ask for its name in
   Studio).
2. Get the export. Easiest: in Studio, **Export for editing > After
   Effects**. The browser downloads a ZIP holding `build.jsx`, the media under
   `media/`, LUTs under `luts/`, `manifest.json` and `README.txt`. Media over
   256 MiB in total is left out and listed in `manifest.json`.

   Without the browser (the CLI has no export command yet), first create a
   personal access token at [API tokens](https://nolgia.ai/settings/api-tokens)
   and export it as `NOLGIA_TOKEN` in your local shell. `nolgia auth login`
   stores credentials internally and does not set this variable. Never paste
   the token into chat or logs.

   ```bash
   curl -fsSL -H "Authorization: Bearer $NOLGIA_TOKEN" \
     "${NOLGIA_API_URL:-https://api.nolgia.ai}/v1/compositions/<composition_id>/export?format=aejsx" \
     -o export.zip
   unzip export.zip -d studio-export && cd studio-export
   python3 - <<'PY'
   import json, pathlib, urllib.request
   for m in json.load(open("manifest.json"))["media"]:
       dest = pathlib.Path(m["path"])
       dest.parent.mkdir(parents=True, exist_ok=True)
       if not dest.exists():
           urllib.request.urlretrieve(m["url"], dest)
   PY
   ```

   The media URLs in `manifest.json` expire after about an hour: download
   them right away, and never paste them into chat or logs.
3. The user runs it: **File > Scripts > Run Script File > build.jsx**, with
   `build.jsx` still next to `media/`. Ask for this one click; it is their
   project.
4. Check the result through the plugin: `nolgia_app_info` (the new comp's
   size, frame rate, frames and layers), then `nolgia_app_preview` with
   `comp` and `frame` at a few frames (start, a cut, a keyframed move, the
   end) and look at them.
5. Fix what the export cannot carry, per `README.txt`:
   - **Fonts**: text layers use PostScript names; a missing font shows as a
     substitute. Tell the user which to install.
   - **Color**: grades arrive as `.cube` files. Put `luts/canvas.cube` on an
     adjustment layer over everything (Apply Color LUT), and per-clip LUTs on
     their layers.
   - Authored HTML, CSS or GSAP animation in the composition never maps; only
     timed media, plain text and the Studio edits do. Keyframes arrive as
     sampled linear keys.

## Drive After Effects through the plugin

- Start with `nolgia_app_info`: the project, whether it has unsaved changes,
  the active comp (size, frame rate, frames, layers) and the other comps.
- Read the rules every NOLGIA workflow in After Effects follows before you
  change anything: `nolgia api GET /desktop-apps/after_effects/rules` (safety
  copies, keeping work editable, previews, the ES3 traps).
- Change things with `nolgia_app_run`: ExtendScript, ES3 (no `let`, `const`,
  arrow functions or `JSON`). Set `result` to a short summary. Each run is
  one undo step in After Effects, and a failure comes back with the line
  that failed.
- Look with `nolgia_app_preview` (`comp`, `frame`) after each visible change.
- Make a safety copy first with `nolgia_app_export` `aep`, and save with
  `nolgia_app_save` only when the person agrees.
- Some commands wait for the person in the plugin (code, when **Ask before
  running code** is on). Tell them to look at the NOLGIA panel, and never
  resend after a **Deny**.

Every command kind, its arguments and the approval flow:
https://docs.nolgia.ai/guides/desktop-apps.html

## Bring NOLGIA media into a project

Generate with nolgia-platform (images, clips, voiceover), then bring the
library asset in with `nolgia_app_import` and its `asset_id` (`as`:
`footage` or `layer`). A NOLGIA color preset installs as a LUT with
`color_preset`. Generation costs credits; work in After Effects adds no
generation cost.

## Send the finished render back to NOLGIA

`nolgia_app_export` with `format: "mp4"` renders the comp through the Render
Queue on the person's computer and puts the file in their NOLGIA library
(`png` for a still). A render the user made themselves uploads with:

```bash
nolgia assets upload final.mp4 --project-id <project_id> --json
```

The result is an ordinary NOLGIA asset: share it, cut shorts from it, or
place it in another Studio composition.

## Limits

- After Effects runs on the person's computer; NOLGIA reaches it only while
  the plugin is signed in with **Connected** on, and NOLGIA Agent only while
  **Allow NOLGIA Agent** is on too.
- Adobe licensing and OS permissions belong to the user.
- The export cannot carry authored HTML, CSS or GSAP animation (see
  `README.txt` in the export).
