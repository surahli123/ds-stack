#!/bin/sh
# Run one eval prompt through the Codex CLI. Used by run_arms.py:
#   python3 eval/run_arms.py --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}"
# The final reply goes to stdout (saved as result.md); Codex's own log goes to stderr (saved as agent.log).
# Codex 0.153 calls the auto-approve flag --approve-for-me; older versions call it --full-auto.
# --ignore-user-config skips config.toml only. Global instructions in $CODEX_HOME (AGENTS.md, skills, prompts) would
# still reach every arm, baseline included, so the operator moves them aside for the run (docs/prompts/acceptance-dots.md).
# A temporary CODEX_HOME would avoid that, but a copied ChatGPT login can rotate its refresh token mid-run.
for leftover in AGENTS.md skills prompts; do
  if [ -e "${CODEX_HOME:-$HOME/.codex}/$leftover" ]; then
    echo "ds-stack: ${CODEX_HOME:-$HOME/.codex}/$leftover is present, so this run is not isolated" >&2
  fi
done
if codex exec --help 2>/dev/null | grep -q -- '--approve-for-me'; then AUTO=--approve-for-me; else AUTO=--full-auto; fi
exec codex exec "$AUTO" --skip-git-repo-check --ignore-user-config --ephemeral "$(cat "$1")"
