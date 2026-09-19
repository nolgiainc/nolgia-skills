# Install for Agents

You are an AI coding agent. The user asked you to install the NOLGIA skills. Follow these steps exactly.

## Step 1: Install the NOLGIA CLI

Skip this step if `nolgia --version` already prints a version.

```bash
curl -fsSL https://raw.githubusercontent.com/nolgiainc/nolgia-cli/main/install.sh | bash
```

The installer needs no sudo: it writes to `~/.local/bin` (or `~/bin`) and adds that directory to the shell profile. If `nolgia` is not found afterwards, run the `export PATH=...` line the installer printed.

Other routes if the script cannot run: `brew install nolgiainc/nolgia/nolgia`, `npm install -g @nolgia/cli`, or `cargo install nolgia-cli`.

Verify: `nolgia --version` prints `nolgia X.Y.Z`.

## Step 2: Authenticate

If `NOLGIA_TOKEN` is already set in the environment, skip to the check below. Otherwise ask the user to run:

```bash
nolgia auth login
```

It opens a browser approval page. Wait for the user to confirm they approved it.

Verify: `nolgia auth status` prints `<email> (<tier>)`.

## Step 3: Install the skills

The CLI ships the skills, so install them from it. Pick the target for your platform:

| Agent | Command |
|---|---|
| Claude Code | `nolgia skills install` |
| Cursor | `nolgia skills install --target dir --dir ~/.cursor/skills` |
| Codex | `nolgia skills install --target dir --dir ~/.codex/skills` |
| Hermes | `nolgia skills install --target hermes` |
| Other | `nolgia skills install --target dir --dir ~/.<agent>/skills` |

If the CLI is older than the skills in this repo, clone the repo instead and copy `skills/*` into the same directory:

```bash
git clone --depth 1 https://github.com/nolgiainc/nolgia-skills.git /tmp/nolgia-skills
cp -R /tmp/nolgia-skills/skills/* <skills directory>/
```

## Step 4: Verify without spending credits

Run:

```bash
nolgia models list --modality image
```

It is free and read-only. A list of image models means the CLI, auth, and network all work.

If anything fails:
- `401` or `not authenticated`: repeat Step 2.
- `402 Payment Required` on a later generation: the token's API credit pool is empty; the user tops up at nolgia.ai.
- Network error: the user's connectivity, not the install.

## Step 5: Done

Tell the user: "NOLGIA skills installed. Try: generate an image, make a short video, extend a photo to 9:16, or plan a vertical UGC ad."

Do not run a paid generation as part of the install, and do not explain the file layout unless asked.
