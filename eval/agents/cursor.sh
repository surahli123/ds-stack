#!/bin/sh
# Run one eval prompt through the Cursor CLI. Used by run_arms.py:
#   python3 eval/run_arms.py --agent-cmd "sh $PWD/eval/agents/cursor.sh {prompt_file}"
# Check `cursor-agent --help` if a flag is rejected: the run must be allowed to execute commands and write files.
exec cursor-agent -p --force "$(cat "$1")"
