#!/bin/sh
# Run the review brief through the Codex CLI: sh codex.sh <model or -> <prompt file>
# Writes stay in the reviewer's directory (workspace-write sandbox) and nothing escalates (approval never).
# Otherwise the reviewer keeps the owner's Codex config: login, effort, and the model when "-" is given.
MODEL=$1
PROMPT=$(cat "$2")
set -- exec --sandbox workspace-write -c 'approval_policy="never"' --skip-git-repo-check
if [ "$MODEL" != "-" ]; then set -- "$@" --model "$MODEL"; fi
exec codex "$@" "$PROMPT"
