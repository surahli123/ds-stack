#!/usr/bin/env python3
"""Check that every number in a ds-mode readout traces to a logged query or check.

    python3 tools/verify_readout.py readout.md [--queries .ds-queries.log] [--checks .ds-checks.log]

In the Answer, "What it means" and "Why we believe it" sections:
- every line that states a number carries a tag: [q<n>] for a logged query,
  [check:<name>#<n>] for a logged check, or [given] for a number stated in the
  request (a threshold, a date range). One bracket may hold several: [q3, q4].
- every [q<n>] is a query that ran (through the runner, or pasted with --pasted);
- every [check:<name>#<n>] is a logged check whose "from" names queries that ran.
The Provenance section must have a "Reconciled:" line.

Dates, a "95%" in front of "interval" or "CI", and digits inside names (v2,
q3) don't count as numbers. Logs default to $DS_QUERIES_LOG / $DS_CHECKS_LOG,
else the files in the current directory.

Prints "verify_readout: pass (...)" or "verify_readout: fail" with one line per
problem, then the [given] lines for the reviewer to confirm against the request.
Exit code: 0 pass, 1 fail, 3 usage error.
"""

import argparse
import json
import os
import re
import sys

ONE_TAG = r"(?:q\d+|check:[a-z_]+#\d+|given)"
TAGS = re.compile(r"\[\s*(" + ONE_TAG + r"(?:\s*[,;|]\s*" + ONE_TAG + r")*)\s*\]", re.I)
LABELS = re.compile(r"\[(?:measured|inferred|guess)\]", re.I)
HEADING = re.compile(r"^#{1,4}\s+(.+?)\s*#*\s*$", re.M)
DATE = re.compile(r"\b\d{4}-\d{2}(?:-\d{2})?\b|\b\d{4}-W\d{2}\b", re.I)
CI_LEVEL = re.compile(r"\b(?:80|90|95|99)\s*%\s*(?=(?:confidence\s+)?(?:interval|CI)\b)", re.I)
LIST_MARKER = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
NUMBER = re.compile(r"(?<![A-Za-z_#\d.])[-+−]?\d+(?:[.,]\d+)*")
CHECKED_SECTIONS = ("answer", "what it means", "why we believe")


def _clean(text):
    text = re.sub(r"^```[a-z]*\s*$", "", text, flags=re.M)
    return text.replace("**", "").replace("__", "").replace("`", "")


def sections(text):
    parts = HEADING.split(_clean(text))
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def numbers_in(line):
    body = LIST_MARKER.sub("", TAGS.sub(" ", LABELS.sub(" ", line)))
    body = CI_LEVEL.sub(" ", DATE.sub(" ", body))
    return NUMBER.findall(body)


def tags_in(line):
    found = []
    for group in TAGS.findall(line):
        found += [tag.strip().lower() for tag in re.split(r"[,;|]", group) if tag.strip()]
    return found


def read_jsonl(path):
    entries = []
    try:
        with open(path) as handle:
            for line in handle:
                try:
                    entries.append(json.loads(line))
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return entries


def verify(text, queries, checks):
    """Return (problems, stats, given_lines)."""
    ran = {e["id"].lower() for e in queries if e.get("id") and e.get("status") == "ok"}
    tried = {e["id"].lower(): e.get("status") for e in queries if e.get("id")}
    logged_checks = {e["id"].lower(): e for e in checks if e.get("id")}
    problems, given, stats = [], [], {"lines": 0, "numbers": 0, "queries": set(), "checks": set()}
    found = sections(text)
    if not any(name.lower().startswith("answer") for name, _ in found):
        problems.append("no Answer section")
    for name, body in found:
        lowered = name.lower()
        if lowered.startswith("provenance") and not re.search(r"^\s*[-*]?\s*reconciled\s*:", body, re.I | re.M):
            problems.append("Provenance has no 'Reconciled:' line (write 'Reconciled: not done (<reason>)' if none was possible)")
        if not lowered.startswith(CHECKED_SECTIONS):
            continue
        for line in body.splitlines():
            numbers, tags = numbers_in(line), tags_in(line)
            if numbers:
                stats["lines"] += 1
                stats["numbers"] += len(numbers)
                if not tags:
                    problems.append(f"untagged number in '{name}': {line.strip()}")
            for tag in tags:
                if tag == "given":
                    given.append(line.strip())
                elif tag.startswith("q"):
                    stats["queries"].add(tag)
                    if tag not in ran:
                        why = f"it was {tried[tag]}" if tag in tried else "it is not in the query log"
                        problems.append(f"[{tag}] doesn't resolve: {why}")
                else:
                    check_id = tag.split(":", 1)[1]
                    stats["checks"].add(check_id)
                    entry = logged_checks.get(check_id)
                    if entry is None:
                        problems.append(f"[{tag}] doesn't resolve: it is not in the check log")
                    elif not entry.get("from"):
                        problems.append(f"[{tag}] has no source query: rerun it with \"from\": \"q<n>\" in the spec")
                    else:
                        missing = [q for q in entry["from"] if q.lower() not in ran]
                        if missing:
                            problems.append(f"[{tag}] names queries that didn't run: {', '.join(missing)}")
    return list(dict.fromkeys(problems)), stats, given


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("readout", help="the readout file (use - for stdin)")
    parser.add_argument("--queries", default=os.environ.get("DS_QUERIES_LOG") or ".ds-queries.log")
    parser.add_argument("--checks", default=os.environ.get("DS_CHECKS_LOG") or ".ds-checks.log")
    args = parser.parse_args(argv)
    try:
        text = sys.stdin.read() if args.readout == "-" else open(args.readout).read()
    except OSError as err:
        print(f"verify_readout: can't read the readout ({err})", file=sys.stderr)
        return 3
    problems, stats, given = verify(text, read_jsonl(args.queries), read_jsonl(args.checks))
    counts = (f"{stats['numbers']} numbers on {stats['lines']} lines; {len(stats['queries'])} queries, "
              f"{len(stats['checks'])} checks, {len(given)} given")
    if problems:
        print(f"verify_readout: fail ({counts})")
        for problem in problems:
            print(f"  - {problem}")
    else:
        print(f"verify_readout: pass ({counts})")
    for line in given:
        print(f"  given (confirm against the request): {line}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
