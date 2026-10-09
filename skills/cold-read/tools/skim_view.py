#!/usr/bin/env python3
"""Print what a skimming reader sees: the first 120 words, then each heading
with the first sentence of its section.

    python3 skim_view.py doc.md [--words 120]
"""

import argparse
import re
import sys


def strip_markup(text):
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*|__([^_]+)__", lambda m: m.group(1) or m.group(2), text)
    return re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", text)


def first_sentence(text):
    match = re.search(r"(.+?[.!?])(?:\s|$)", text)
    return (match.group(1) if match else text).strip()


def skim(text, limit=120):
    lines, fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            lines.append(line)

    opening, count = [], 0
    for line in lines:
        if count >= limit:
            break
        words = strip_markup(line).split()
        if not words:
            continue
        take = words[: limit - count]
        opening.append(" ".join(take))
        count += len(take)

    outline, heading, body = [], None, []

    def flush():
        if heading is not None:
            prose = " ".join(strip_markup(l) for l in body if l.strip() and not l.lstrip().startswith("|")).strip()
            outline.append(f"{heading}\n  {first_sentence(prose) if prose else '(no prose)'}")

    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if match:
            flush()
            heading, body = f"{match.group(1)} {match.group(2).strip()}", []
        else:
            body.append(line)
    flush()
    return "OPENING\n" + "\n".join(opening) + "\n\nOUTLINE\n" + "\n".join(outline) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path")
    parser.add_argument("--words", type=int, default=120)
    args = parser.parse_args(argv)
    try:
        with open(args.path, encoding="utf-8") as handle:
            sys.stdout.write(skim(handle.read(), args.words))
    except OSError as err:
        print(f"skim_view: {err}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
