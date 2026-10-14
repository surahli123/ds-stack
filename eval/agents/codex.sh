#!/bin/sh
# Run one eval prompt through the Codex CLI. Used by run_arms.py:
#   python3 eval/run_arms.py --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}"
# The final reply goes to stdout (saved as result.md); Codex's own log goes to stderr (saved as agent.log).
#
# Isolation: --ignore-user-config skips config.toml only. Codex also loads instructions and skills from
# $CODEX_HOME (AGENTS.md, skills/, prompts/) and from the home directory (~/.agents/skills, plugins).
# - CODEX_HOME stays the real one, so the single real auth.json is used: no copied login whose refresh
#   token could rotate mid-run. The operator moves AGENTS.md, AGENTS.override.md, skills/ and prompts/ out of
#   it for the run (docs/prompts/acceptance-dots.md). If any is still there, this script says so and exits 4
#   without starting Codex, so a leaky run is never made.
# - Codex writes its embedded system skills to $CODEX_HOME/skills/.system on every start (codex-rs/skills,
#   install_system_skills), so skills/ exists again after the first run. Only .system is allowed in it (and
#   Finder's .DS_Store), and .system may hold only the skills below and Codex's marker file. They are the
#   six in codex-rs/skills/src/assets/samples at tag rust-v0.153.4. A Codex release that adds one stops
#   every run here until the list is updated; the probe uses the same list.
# - HOME points at an empty temporary directory, so nothing under the real home reaches the agent.
# - Plugins, remote plugins, apps and memories are disabled per run (Codex 0.153 feature flags).
# - DS_CODEX_MODEL and DS_CODEX_EFFORT, when set, pin the model and the reasoning effort. Otherwise
#   --ignore-user-config leaves Codex's defaults. agent.log's header names the ones used either way.
# Check the result once with eval/agents/codex-isolation-probe.sh before a matrix.
CODEX_HOME=${CODEX_HOME:-$HOME/.codex}
export CODEX_HOME
SYSTEM_SKILLS="imagegen openai-docs plugin-creator review-agent skill-creator skill-installer"
LEAKED=0
leak() { echo "ds-stack: $1 is present, so this run is not isolated; Codex was not started" >&2; LEAKED=1; }
for leftover in AGENTS.md AGENTS.override.md prompts; do
  if [ -e "$CODEX_HOME/$leftover" ]; then leak "$CODEX_HOME/$leftover"; fi
done
for entry in "$CODEX_HOME"/skills/* "$CODEX_HOME"/skills/.[!.]* "$CODEX_HOME"/skills/..?*; do
  if [ ! -e "$entry" ] && [ ! -L "$entry" ]; then continue; fi
  if [ "$entry" = "$CODEX_HOME/skills/.system" ] && [ ! -L "$entry" ]; then continue; fi
  if [ "$entry" = "$CODEX_HOME/skills/.DS_Store" ] && [ -f "$entry" ] && [ ! -L "$entry" ]; then continue; fi
  leak "$entry"
done
for entry in "$CODEX_HOME"/skills/.system/* "$CODEX_HOME"/skills/.system/.[!.]* "$CODEX_HOME"/skills/.system/..?*; do
  if [ ! -e "$entry" ] && [ ! -L "$entry" ]; then continue; fi
  case " $SYSTEM_SKILLS .codex-system-skills.marker .DS_Store " in *" ${entry##*/} "*) continue ;; esac
  leak "$entry"
done
if [ "$LEAKED" = 1 ]; then exit 4; fi
# Codex 0.153 calls the auto-approve flag --approve-for-me; older versions call it --full-auto.
if codex exec --help 2>/dev/null | grep -q -- '--approve-for-me'; then AUTO=--approve-for-me; else AUTO=--full-auto; fi
EMPTY_HOME=$(mktemp -d "${TMPDIR:-/tmp}/ds-codex-home.XXXXXX")
PROMPT=$(cat "$1")
set --
if [ -n "$DS_CODEX_MODEL" ]; then set -- "$@" --model "$DS_CODEX_MODEL"; fi
if [ -n "$DS_CODEX_EFFORT" ]; then set -- "$@" -c "model_reasoning_effort=\"$DS_CODEX_EFFORT\""; fi
# Account-synced plugins (and their skills), apps and memories load regardless of config.toml; switch them off.
HOME="$EMPTY_HOME" codex exec "$AUTO" --skip-git-repo-check --ignore-user-config --ephemeral \
  --disable plugins --disable remote_plugin --disable apps --disable memories "$@" "$PROMPT"
STATUS=$?
rm -rf "$EMPTY_HOME"
exit $STATUS
