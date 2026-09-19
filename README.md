# NOLGIA Skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.2.0-green.svg)](./VERSION)
[![Skills](https://img.shields.io/badge/skills-4-blueviolet.svg)](#skills)

Agent skills for generating images, video, and audio on [NOLGIA](https://nolgia.ai). They teach Claude Code, Cursor, Codex, and any agent that loads Markdown skills how to drive the [`nolgia` CLI](https://github.com/nolgiainc/nolgia-cli): pick a model from the live catalog, submit and follow jobs, keep characters consistent, direct multi-shot video, produce vertical UGC ads, and assemble clips into one finished video.

## Install

Pick one. Every method installs the same skills.

### `npx skills` (cross-agent)

```bash
npx skills add nolgiainc/nolgia-skills
```

### `gh skill install`

GitHub CLI 2.90 or newer:

```bash
gh skill install nolgiainc/nolgia-skills --all
```

### Claude Code plugin marketplace

Inside Claude Code:

```
/plugin marketplace add nolgiainc/nolgia-skills
/plugin install nolgia@nolgia
```

### The `nolgia` CLI

The CLI ships the same skills and installs them itself:

```bash
nolgia skills install                 # ~/.claude/skills (Claude Code, user-wide)
nolgia skills install --target dir --dir ~/.cursor/skills
```

More options, including Cursor and Codex, in [INSTALL.md](./INSTALL.md). To let your agent do the install, paste [INSTALL_FOR_AGENTS.md](./INSTALL_FOR_AGENTS.md) into it.

For the NOLGIA MCP server and a `/nolgia` command in Cursor, see [nolgiainc/cursor-plugin](https://github.com/nolgiainc/cursor-plugin).

## Skills

| Skill | Claude Code | What it covers |
|---|---|---|
| [`nolgia-platform`](./skills/nolgia-platform) | `/nolgia:nolgia-platform` | Auth, the live model catalog, image/video/audio generation, outpainting (`--expand-to`), voices, async jobs (`nolgia jobs list`), characters, projects, credits, assembling clips into a rendered video, and failure recovery. |
| [`nolgia-video-prompting`](./skills/nolgia-video-prompting) | `/nolgia:nolgia-video-prompting` | Directing craft: shot grammar, the breathing pattern, multi-shot sequencing, reference-image consistency, per-shot sound, and the keep/fix/cut iteration loop. |
| [`nolgia-ugc-ads`](./skills/nolgia-ugc-ads) | `/nolgia:nolgia-ugc-ads` | Vertical UGC ads: persona, portraits, screenshot B-roll, a lip-synced talking head from a voiceover, the interleaved timeline, and face-safe text zones. |
| [`nolgia-after-effects`](./skills/nolgia-after-effects) | `/nolgia:nolgia-after-effects` | Desktop only: open a NOLGIA Studio composition in After Effects through its `build.jsx` export, drive After Effects with the local `fnf-after-effects-mcp` server, and upload the finished render back to NOLGIA. |

They chain: `nolgia-platform` owns the mechanics; `nolgia-video-prompting` and `nolgia-ugc-ads` own the craft and hand every command back to it; `nolgia-after-effects` takes finished NOLGIA work into a local After Effects.

## Quick reference

| What you want | Skill | Command shape |
|---|---|---|
| An image from a prompt | `nolgia-platform` | `nolgia gen image --prompt ... --out img.png` |
| A video clip | `nolgia-platform` | `nolgia gen video --prompt ... --aspect-ratio 9:16 --out clip.mp4` |
| A 16:9 still as a 9:16 story | `nolgia-platform` | `nolgia gen image --expand-to 9:16 --input still.png` |
| A voiceover | `nolgia-platform` | `nolgia voices list --model <tts>` then `nolgia gen audio --model <tts> --voice <id>` |
| Jobs in flight or failed | `nolgia-platform` | `nolgia jobs list --status running` |
| A multi-shot sequence | `nolgia-video-prompting` | `nolgia gen video --shot "4:WIDE..." --shot "3:CU..."` |
| A TikTok/Reels ad | `nolgia-ugc-ads` | persona, assets, `heygen-avatar-iv` talking head, composition render |
| A Studio edit finished in After Effects | `nolgia-after-effects` | Studio Export for editing > After Effects, run `build.jsx`, then `nolgia assets upload final.mp4` |

## Requirements

- The `nolgia` CLI: `brew install nolgiainc/nolgia/nolgia`, `npm install -g @nolgia/cli`, or `curl -fsSL https://raw.githubusercontent.com/nolgiainc/nolgia-cli/main/install.sh | bash`.
- A NOLGIA account: `nolgia auth login`, or a personal access token in `NOLGIA_TOKEN` (API credits).

## Maintaining

The three generation skills are the same files the CLI bundles in [`crates/cli/skills`](https://github.com/nolgiainc/nolgia-cli/tree/main/crates/cli/skills); change them there and copy them here in the same release. `nolgia-after-effects` is a desktop skill and lives only here. `python3 scripts/check-skills.py` (run in CI) enforces the conventions: `name` equals the folder, `version` equals [VERSION](./VERSION) and every plugin manifest, the description carries a "Use when" trigger and a "NOT for" boundary within 1,024 characters, `related_skills` resolve, and no skill reaches outside its folder.

## License

MIT, see [LICENSE](./LICENSE).
