#!/bin/sh
# Run the review brief through Claude Code: sh claude.sh <model or -> <prompt file>
if [ "$1" = "-" ]; then MODEL=""; else MODEL="--model $1"; fi
# shellcheck disable=SC2086
exec claude -p "$(cat "$2")" $MODEL --allowedTools "Bash,Read,Write,Glob,Grep" --max-turns 60
