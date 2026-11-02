#!/bin/sh
# Run the review brief through Cursor's CLI: sh cursor.sh <model or -> <prompt file>
if [ "$1" = "-" ]; then exec cursor-agent -p --force "$(cat "$2")"; fi
exec cursor-agent -p --force --model "$1" "$(cat "$2")"
