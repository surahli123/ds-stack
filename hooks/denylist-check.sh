#!/usr/bin/env bash
# Block commits and pushes that contain terms from the private overlay's denylist.
#
#   hooks/denylist-check.sh staged          # pre-commit: added lines in the index
#   hooks/denylist-check.sh push            # pre-push: reads git's pre-push stdin
#
# The denylist lives OUTSIDE this repo, in the private overlay. Point at it with
# DS_DENYLIST=/path/to/denylist.txt or DS_OVERLAY_DIR=/path/to/overlay.
# Fail-closed: with no denylist configured, the hook blocks. A machine that
# never holds work material can opt out explicitly with DS_DENYLIST=none.
set -euo pipefail

mode="${1:-staged}"
list="${DS_DENYLIST:-}"
if [ -z "$list" ] && [ -n "${DS_OVERLAY_DIR:-}" ]; then
  list="$DS_OVERLAY_DIR/denylist.txt"
fi

if [ "$list" = "none" ]; then
  exit 0
fi
if [ -z "$list" ] || [ ! -r "$list" ]; then
  echo "denylist-check: no readable denylist (set DS_DENYLIST or DS_OVERLAY_DIR; DS_DENYLIST=none to opt out)." >&2
  exit 1
fi

patterns="$(mktemp)"
trap 'rm -f "$patterns"' EXIT
grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$list" > "$patterns" || true
if [ ! -s "$patterns" ]; then
  exit 0
fi

added_lines() {
  if [ "$mode" = "push" ]; then
    local zero=0000000000000000000000000000000000000000
    while read -r _ local_sha _ remote_sha; do
      [ "$local_sha" = "$zero" ] && continue
      if [ "$remote_sha" = "$zero" ]; then
        git log -p --format= "$local_sha" --not --remotes
      else
        git diff "$remote_sha" "$local_sha"
      fi
    done
  else
    git diff --cached -U0 --no-color
  fi
}

hits="$(added_lines | grep -E '^\+' | grep -v -E '^\+\+\+ ' | grep -n -i -F -f "$patterns" || true)"
if [ -n "$hits" ]; then
  count="$(printf '%s\n' "$hits" | wc -l | tr -d ' ')"
  echo "denylist-check: blocked. $count added line(s) contain a denylisted term:" >&2
  printf '%s\n' "$hits" | cut -c1-160 >&2
  exit 1
fi
