---
name: nolgia-after-effects
description: "Finish NOLGIA work in Adobe After Effects on the user's own computer: open a NOLGIA Studio composition in After Effects through its build.jsx export, drive After Effects with the local fnf-after-effects-mcp server (inspect comps, layers, keyframes, render check frames), bring NOLGIA-generated media into a project, and upload the finished render back to the NOLGIA library with the nolgia CLI. Use when: the user has After Effects installed and asks to 'open my Studio edit in After Effects', 'finish this in AE', 'add motion graphics to my NOLGIA video', or 'get my AE render into NOLGIA'. NOT for: generating media (use nolgia-platform), Premiere Pro or DaVinci Resolve (use the sequence.xml export in the web app), Blender, or the hosted NOLGIA Agent, which runs in the cloud and cannot reach a desktop app."
version: 1.2.0
author: NOLGIA
license: MIT
metadata:
  tags: [nolgia, after-effects, motion-graphics, mcp, desktop, studio-export, jsx]
  related_skills: [nolgia-platform]
---

# NOLGIA + After Effects (desktop)

Three pieces on the user's own machine:

- **After Effects** (2024 to 2026, macOS or Windows), licensed and installed
  by the user.
- **`fnf-after-effects-mcp`**: a local stdio MCP server that drives After
  Effects through its scripting interface (12 tools, `ae_*`). It runs only on
  the same computer as After Effects.
- **The `nolgia` CLI** (see nolgia-platform for install and auth): generates
  media, lists compositions, uploads the finished render.

NOLGIA Studio's **Export for editing > After Effects** writes the bridge
between them: a `build.jsx` script that rebuilds the Studio edit as a native
After Effects comp.

## Setup (once)

```bash
node --version                      # 24 or newer
npm install --global --ignore-scripts fnf-after-effects-mcp@0.1.1
fnf-after-effects doctor            # node, platform, server, After Effects path, bundled skills
fnf-after-effects config            # prints the MCP entry with absolute paths
```

Register the server with the agent you are running in, using the printed
`command` and `args`:

- **Codex**: `fnf-after-effects install-codex`.
- **Claude Code**: `claude mcp add after-effects -- <command> <args>` with the
  two values from `config`.
- **Cursor or another client**: merge the printed JSON into its MCP config.

Then refresh the client's MCP connection and, in After Effects, turn on
**Allow Scripts to Write Files and Access Network** (Preferences, or
Settings on macOS, > Scripting & Expressions). On macOS, allow the Automation prompt the first time. Verify
with `ae_project_info`: it answers with the open project, or says what
permission is missing. For a nonstandard install path, set `AE_MCP_EXE` in the
server's environment.

## Open a Studio composition in After Effects

1. Find the composition: `nolgia compositions list` (or ask for its name in
   Studio).
2. Get the export. Easiest: in Studio, **Export for editing > After
   Effects**. The browser downloads a ZIP holding `build.jsx`, the media under
   `media/`, LUTs under `luts/`, `manifest.json` and `README.txt`. Media over
   256 MiB in total is left out and listed in `manifest.json`.

   Without the browser (the CLI has no export command yet):

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
   `build.jsx` still next to `media/`. The MCP server does not run scripts
   (its arbitrary-eval switch, `AE_MCP_ENABLE_EVAL`, stays off), so ask the
   user to do this one click.
4. Check the result through the MCP: `ae_project_info`, then `ae_comp_info`
   on the new comp (size, fps, duration, layer list) and `ae_layer_info` on
   text and masked layers. `ae_render_frame` a few frames (start, a cut, a
   keyframed move, the end) and look at them.
5. Fix what the export cannot carry, per `README.txt`:
   - **Fonts**: text layers use PostScript names; a missing font shows as a
     substitute. Tell the user which to install.
   - **Color**: grades arrive as `.cube` files. Put `luts/canvas.cube` on an
     adjustment layer over everything (Apply Color LUT), and per-clip LUTs on
     their layers.
   - Authored HTML, CSS or GSAP animation in the composition never maps; only
     timed media, plain text and the Studio edits do. Keyframes arrive as
     sampled linear keys.

## Drive After Effects with the MCP

- Start with `ae_get_skill({})` and `ae_context`: the bundled workflows and
  the ES3 and undo rules. `ae_catalog({})` then `ae_catalog({category})`
  lists the exact operations `ae_do` accepts; discover them rather than
  guessing names.
- Every `ae_*` call is one undo group; `batch.run` groups several but does
  not roll back on failure. A call that timed out may still have run:
  inspect before retrying a change.
- Preserve the user's unsaved work. Save with `ae_save_project` only when
  they ask. For a look-only session, set `AE_MCP_READONLY=1` on the server.

## Bring NOLGIA media into a project

Generate with nolgia-platform (`nolgia gen image ... --out plate.png`,
`nolgia gen video ... --out shot.mp4`), keep the files in the project's
folder, then import them with the import operation `ae_catalog` lists, or
ask the user to drag them in. The generation costs credits; After Effects
work costs none.

## Send the finished render back to NOLGIA

The user renders from the Render Queue (H.264 MP4 or ProRes MOV). Then:

```bash
nolgia assets upload final.mp4 --project-id <project_id> --json
```

The uploaded video is an ordinary NOLGIA asset: share it, cut shorts from it,
or place it in another Studio composition.

## Limits

- Desktop only: After Effects and this server must be on the same machine.
  The hosted NOLGIA Agent cannot reach them; it can prepare the export and the
  media, and the user finishes here.
- Adobe licensing, OS permissions and the scripting preference belong to the
  user; the server cannot grant them.
- Premiere Pro and DaVinci Resolve use the other export format, `sequence.xml`
  (Export for editing > Premiere Pro or DaVinci Resolve), with no MCP.
