#!/bin/sh
# One paid Codex call that shows what an eval run can see, under the same isolation as codex.sh.
#   sh eval/agents/codex-isolation-probe.sh
# Run it after moving ~/.codex/{AGENTS.md,AGENTS.override.md,skills,prompts} aside (docs/prompts/acceptance-dots.md,
# step 2). It is the first Codex start after that, so Codex rebuilds skills/.system during it; codex.sh allows
# only that folder in skills/ from then on, and this probe checks that it holds just the system skills.
# Prints Codex's reply, then PASS or FAIL. Exit code: 0 pass, 1 fail.
# With DS_CODEX_MODEL and DS_CODEX_EFFORT set (docs/prompts/acceptance-dots.md, step 2), it also fails unless
# the model and reasoning effort in Codex's log header are the pinned ones.
# Pass: every listed skill is one of Codex's system skills, and no instruction file is listed. The model may
# leave some out (in 2026-10-13-2343 it didn't list review-agent), so codex.sh also checks the folder itself.
# Same list as SYSTEM_SKILLS in codex.sh.
ALLOWED="imagegen openai-docs plugin-creator review-agent skill-creator skill-installer"
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=$(mktemp -d "${TMPDIR:-/tmp}/ds-codex-probe.XXXXXX")
cat > "$WORK/prompt.md" <<'PROMPT'
Use no tools and run no commands. From what is already in your context, reply with exactly two lines:
SKILLS: <every skill you can see, by name, comma-separated, or NONE>
INSTRUCTIONS: <the first heading of every instruction file (AGENTS.md or similar) you were given, comma-separated, or NONE>
PROMPT
REPLY=$(cd "$WORK" && sh "$HERE/codex.sh" "$WORK/prompt.md" 2>"$WORK/agent.log")
LEFTOVERS=$(grep 'not isolated' "$WORK/agent.log")
HEADER=$(grep -E '^(model|reasoning effort):' "$WORK/agent.log")
rm -rf "$WORK"
[ -n "$LEFTOVERS" ] && echo "$LEFTOVERS"
echo "$REPLY"
if [ -n "$LEFTOVERS" ]; then echo "FAIL: files that step 2 moves aside are still in CODEX_HOME, so Codex was not started"; exit 1; fi
[ -n "$HEADER" ] && echo "$HEADER"
if [ -n "$DS_CODEX_MODEL" ] && ! echo "$HEADER" | grep -qFx "model: $DS_CODEX_MODEL"; then
  echo "FAIL: Codex didn't run the pinned model $DS_CODEX_MODEL"; exit 1
fi
if [ -n "$DS_CODEX_EFFORT" ] && ! echo "$HEADER" | grep -qFx "reasoning effort: $DS_CODEX_EFFORT"; then
  echo "FAIL: Codex didn't run the pinned reasoning effort $DS_CODEX_EFFORT"; exit 1
fi
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
if [ -n "$EXTRA" ]; then echo "FAIL: skills beyond Codex's system skills:$EXTRA"; exit 1; fi
if [ "$(echo "$INSTR" | tr 'a-z' 'A-Z' | tr -d ' .')" != "NONE" ]; then echo "FAIL: instruction files: $INSTR"; exit 1; fi
echo "PASS"
