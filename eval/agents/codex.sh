#!/bin/sh
# Run one eval prompt through the Codex CLI. Used by run_arms.py:
#   python3 eval/run_arms.py --agent-cmd "sh $PWD/eval/agents/codex.sh {prompt_file}"
# The final reply goes to stdout (saved as result.md); Codex's own log goes to stderr (saved as agent.log).
# Codex 0.153 calls the auto-approve flag --approve-for-me; older versions call it --full-auto.
if codex exec --help 2>/dev/null | grep -q -- '--approve-for-me'; then AUTO=--approve-for-me; else AUTO=--full-auto; fi
exec codex exec "$AUTO" --skip-git-repo-check --ignore-user-config --ephemeral "$(cat "$1")"
