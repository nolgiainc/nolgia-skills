# Install NOLGIA Skills

Three skills ship in this repo:

- **`nolgia-platform`**: generate images, video, and audio with the `nolgia` CLI; the live model catalog, outpainting, voices, jobs, characters, projects, credits, rendering a finished cut, and failure recovery
- **`nolgia-video-prompting`**: directing craft for video prompts and multi-clip productions
- **`nolgia-ugc-ads`**: vertical UGC ad production end to end

`nolgia-platform` owns the commands; the other two own the craft and call back into it.

## Prerequisites

Install the NOLGIA CLI (no sudo; installs to `~/.local/bin`):

```bash
curl -fsSL https://raw.githubusercontent.com/nolgiainc/nolgia-cli/main/install.sh | bash
nolgia auth login
```

Alternatives: `brew install nolgiainc/nolgia/nolgia`, `npm install -g @nolgia/cli`, or `cargo install nolgia-cli`. Prebuilt binaries cover macOS (universal), Linux x86_64 and Windows x86_64; Linux arm64 and Windows arm64 builds ship from the first CLI release after v0.2.26.

For CI or headless agents, skip the browser login and export a personal access token from [nolgia.ai/settings/api-tokens](https://nolgia.ai/settings/api-tokens) as `NOLGIA_TOKEN`. Token requests spend API credits.

## Option 1: `npx skills` (cross-agent)

Works with Claude Code, Cursor, Codex, and the other agents the [`skills`](https://www.npmjs.com/package/skills) CLI supports. Requires Node.js.

```bash
npx skills add nolgiainc/nolgia-skills
```

The CLI detects the host agent and writes each skill to that agent's skills directory.

## Option 2: `gh skill install`

GitHub CLI 2.90 or newer (the command is in preview).

```bash
gh skill install nolgiainc/nolgia-skills --all                    # this project
gh skill install nolgiainc/nolgia-skills --all --scope user       # every project
gh skill install nolgiainc/nolgia-skills nolgia-platform --agent cursor
```

## Option 3: Claude Code plugin marketplace

Inside Claude Code:

```
/plugin marketplace add nolgiainc/nolgia-skills
/plugin install nolgia@nolgia
```

This reads `.claude-plugin/marketplace.json` and registers the skills as `/nolgia:nolgia-platform`, `/nolgia:nolgia-video-prompting`, `/nolgia:nolgia-ugc-ads`, and `/nolgia:nolgia-after-effects`.

## Option 4: Cursor

Cursor reads `.cursor-plugin/plugin.json` and the `skills/` folder when the repo is added as a plugin. Without the plugin flow, use Option 1 or 2 with `--agent cursor`. For the hosted NOLGIA MCP server and a `/nolgia` command, install [nolgiainc/cursor-plugin](https://github.com/nolgiainc/cursor-plugin) as well.

## Option 5: Codex

Codex reads `.codex-plugin/plugin.json`, which points at `./skills/`, when the repo is installed as a plugin. To install the skills directly instead:

```bash
gh skill install nolgiainc/nolgia-skills --all --agent codex --scope user
```

## Option 6: the `nolgia` CLI

The CLI bundles the three generation skills (`nolgia-platform`, `nolgia-video-prompting`, `nolgia-ugc-ads`), so an installed CLI needs nothing else for those. The desktop `nolgia-after-effects` skill ships from this repo only:

```bash
nolgia skills list
nolgia skills install                                   # ~/.claude/skills
nolgia skills install --target claude-project           # ./.claude/skills
nolgia skills install --target dir --dir ~/.codex/skills
```

`--force` overwrites existing copies.

## Verify

In your agent, ask:

> "Which NOLGIA image models support 9:16?"

The agent should load `nolgia-platform` and run `nolgia models list --modality image`, which is free and read-only. Ask for a generation only when you are ready to spend credits.

## Updating

| Method | Update command |
|---|---|
| `npx skills` | re-run `npx skills add nolgiainc/nolgia-skills` |
| `gh skill install` | `gh skill update` |
| Claude Code marketplace | `/plugin marketplace update nolgia` then `/plugin update nolgia@nolgia` |
| `nolgia` CLI | upgrade the CLI, then `nolgia skills install --force` |
