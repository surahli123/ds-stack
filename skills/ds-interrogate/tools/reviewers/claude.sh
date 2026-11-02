#!/bin/sh
# Run the review brief through Claude Code: sh claude.sh <model or -> <prompt file>
# The shell is limited to ds-mode's query runner ($DS_QUERY_PY, set by interrogate.py); files go through
# the file tools, in the reviewer's own directory.
MODEL=$1
PROMPT=$(cat "$2")
set -- -p "$PROMPT" --allowedTools "Bash(python3 $DS_QUERY_PY:*)" Read Write Glob Grep --max-turns 60
if [ "$MODEL" != "-" ]; then set -- "$@" --model "$MODEL"; fi
exec claude "$@"
