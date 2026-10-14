#!/bin/sh
# One paid Codex call that shows what an eval run can see, under the same isolation as codex.sh.
#   sh eval/agents/codex-isolation-probe.sh
# Run it after moving ~/.codex/{AGENTS.md,skills,prompts} aside (docs/prompts/acceptance-dots.md, step 2).
# Pass: Codex lists no skills and no instruction files beyond its built-in behaviour (or says NONE).
# Fail: any named skill, AGENTS.md content or personal path appears. Then stop and report the reply.
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=$(mktemp -d "${TMPDIR:-/tmp}/ds-codex-probe.XXXXXX")
cat > "$WORK/prompt.md" <<'PROMPT'
Use no tools and run no commands. From what is already in your context, list:
1. every skill you can see, by name;
2. every instruction file you were given (AGENTS.md or similar), with its first heading.
If there are none of a kind, write NONE for it.
PROMPT
cd "$WORK" && sh "$HERE/codex.sh" "$WORK/prompt.md"
STATUS=$?
rm -rf "$WORK"
exit $STATUS
