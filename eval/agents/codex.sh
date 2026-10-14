#!/bin/sh
# Run one eval prompt through the Codex CLI. Used by run_arms.py:
#   python3 eval/run_arms.py --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}"
# The final reply goes to stdout (saved as result.md); Codex's own log goes to stderr (saved as agent.log).
#
# Isolation: --ignore-user-config skips config.toml only. Codex also loads instructions and skills from
# $CODEX_HOME (AGENTS.md, skills/, prompts/) and from the home directory (~/.agents/skills, plugins).
# - CODEX_HOME stays the real one, so the single real auth.json is used: no copied login whose refresh
#   token could rotate mid-run. The operator moves AGENTS.md, skills/ and prompts/ out of it for the run
#   (docs/prompts/acceptance-dots.md); this script reports any that are still there.
# - HOME points at an empty temporary directory, so nothing under the real home reaches the agent.
# Check the result once with eval/agents/codex-isolation-probe.sh before a matrix.
CODEX_HOME=${CODEX_HOME:-$HOME/.codex}
export CODEX_HOME
for leftover in AGENTS.md skills prompts; do
  if [ -e "$CODEX_HOME/$leftover" ]; then
    echo "ds-stack: $CODEX_HOME/$leftover is present, so this run is not isolated" >&2
  fi
done
# Codex 0.153 calls the auto-approve flag --approve-for-me; older versions call it --full-auto.
if codex exec --help 2>/dev/null | grep -q -- '--approve-for-me'; then AUTO=--approve-for-me; else AUTO=--full-auto; fi
EMPTY_HOME=$(mktemp -d "${TMPDIR:-/tmp}/ds-codex-home.XXXXXX")
PROMPT=$(cat "$1")
HOME="$EMPTY_HOME" codex exec "$AUTO" --skip-git-repo-check --ignore-user-config --ephemeral "$PROMPT"
STATUS=$?
rm -rf "$EMPTY_HOME"
exit $STATUS
