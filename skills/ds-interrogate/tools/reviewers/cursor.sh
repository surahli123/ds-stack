#!/bin/sh
# Run the review brief through Cursor's CLI: sh cursor.sh <model or -> <prompt file>
# --force runs commands without asking, and Cursor's CLI has no sandbox flag: use it only where that's acceptable.
MODEL=$1
PROMPT=$(cat "$2")
set -- -p --force
if [ "$MODEL" != "-" ]; then set -- "$@" --model "$MODEL"; fi
exec cursor-agent "$@" "$PROMPT"
