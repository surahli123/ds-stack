#!/bin/sh
# Run the review brief through the Codex CLI: sh codex.sh <model or -> <prompt file>
# The reviewer keeps the owner's own Codex config (model, effort, login); "-" means its default model.
if codex exec --help 2>/dev/null | grep -q -- '--approve-for-me'; then AUTO=--approve-for-me; else AUTO=--full-auto; fi
if [ "$1" = "-" ]; then set -- "$2"; else set -- "$2" --model "$1"; fi
PROMPT=$(cat "$1"); shift
exec codex exec "$AUTO" --skip-git-repo-check "$@" "$PROMPT"
