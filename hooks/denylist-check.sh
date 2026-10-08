#!/usr/bin/env bash
# Block commits and pushes that contain terms from the private overlay's denylist.
#
#   hooks/denylist-check.sh staged          # pre-commit: what is staged
#   hooks/denylist-check.sh push            # pre-push: reads git's pre-push stdin
#
# Scans added lines (binary files as text, so a term inside a .db is found) and
# file paths. Pre-push scans every commit being pushed, not the net diff, so a
# term added in one commit and removed in the next is still caught.
#
# The denylist lives OUTSIDE this repo, in the private overlay. Point at it with
# DS_DENYLIST=/path/to/denylist.txt or DS_OVERLAY_DIR=/path/to/overlay.
# Fail-closed: no denylist configured, or any git error, blocks. A machine that
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

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$list" > "$work/patterns" || true
if [ ! -s "$work/patterns" ]; then
  exit 0
fi

fail() { echo "denylist-check: $1; blocking." >&2; exit 1; }
: > "$work/diff"
: > "$work/names"

if [ "$mode" = "push" ]; then
  zero=0000000000000000000000000000000000000000
  while read -r _ local_sha _ remote_sha; do
    [ "$local_sha" = "$zero" ] && continue
    if [ "$remote_sha" = "$zero" ]; then
      range=("$local_sha" --not --remotes)
    else
      range=("$remote_sha..$local_sha")
    fi
    git log -p --format= -U0 --no-color --text "${range[@]}" >> "$work/diff" || fail "git log failed for ${range[*]}"
    git log --format= --name-only "${range[@]}" >> "$work/names" || fail "git log failed for ${range[*]}"
  done
else
  git diff --cached -U0 --no-color --text > "$work/diff" || fail "git diff failed"
  git diff --cached --name-only > "$work/names" || fail "git diff failed"
fi

{ grep -a -E '^\+' "$work/diff" | grep -a -v -E '^\+\+\+ ' || true; sed 's/^/path: /' "$work/names"; } > "$work/added"
hits="$(grep -n -i -a -F -f "$work/patterns" "$work/added" || true)"
if [ -n "$hits" ]; then
  count="$(printf '%s\n' "$hits" | wc -l | tr -d ' ')"
  echo "denylist-check: blocked. $count added line(s) or path(s) contain a denylisted term:" >&2
  printf '%s\n' "$hits" | LC_ALL=C tr -c '[:print:]\n' '?' | cut -c1-160 >&2
  exit 1
fi
