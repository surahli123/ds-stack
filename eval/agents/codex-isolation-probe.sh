#!/bin/sh
# One paid Codex call that shows what an eval run can see, under the same isolation as codex.sh.
#   sh eval/agents/codex-isolation-probe.sh
# Run it after moving ~/.codex/{AGENTS.md,skills,prompts} aside (docs/prompts/acceptance-dots.md, step 2).
# Prints Codex's reply, then PASS or FAIL. Exit code: 0 pass, 1 fail.
# Pass: every listed skill is one of Codex's five rebuilt system skills, and no instruction file is listed.
ALLOWED="imagegen openai-docs plugin-creator skill-creator skill-installer"
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=$(mktemp -d "${TMPDIR:-/tmp}/ds-codex-probe.XXXXXX")
cat > "$WORK/prompt.md" <<'PROMPT'
Use no tools and run no commands. From what is already in your context, reply with exactly two lines:
SKILLS: <every skill you can see, by name, comma-separated, or NONE>
INSTRUCTIONS: <the first heading of every instruction file (AGENTS.md or similar) you were given, comma-separated, or NONE>
PROMPT
REPLY=$(cd "$WORK" && sh "$HERE/codex.sh" "$WORK/prompt.md" 2>"$WORK/agent.log")
rm -rf "$WORK"
echo "$REPLY"
SKILLS=$(echo "$REPLY" | grep -i '^ *SKILLS:' | tail -1 | sed 's/^ *[Ss][Kk][Ii][Ll][Ll][Ss]: *//')
INSTR=$(echo "$REPLY" | grep -i '^ *INSTRUCTIONS:' | tail -1 | sed 's/^ *[Ii][Nn][Ss][Tt][Rr][Uu][Cc][Tt][Ii][Oo][Nn][Ss]: *//')
if [ -z "$SKILLS" ] || [ -z "$INSTR" ]; then echo "FAIL: the reply lacks a SKILLS: or INSTRUCTIONS: line"; exit 1; fi
EXTRA=""
if [ "$(echo "$SKILLS" | tr 'a-z' 'A-Z' | tr -d ' .')" != "NONE" ]; then
  for name in $(echo "$SKILLS" | tr ',' ' '); do
    name=$(echo "$name" | tr -d ' .`')
    case " $ALLOWED " in *" $name "*) ;; *) EXTRA="$EXTRA $name" ;; esac
  done
fi
if [ -n "$EXTRA" ]; then echo "FAIL: skills beyond the five system skills:$EXTRA"; exit 1; fi
if [ "$(echo "$INSTR" | tr 'a-z' 'A-Z' | tr -d ' .')" != "NONE" ]; then echo "FAIL: instruction files: $INSTR"; exit 1; fi
echo "PASS"
