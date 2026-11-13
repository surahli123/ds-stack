#!/usr/bin/env python3
"""Check that every number in a ds-mode readout traces to a logged query or check.

    python3 tools/verify_readout.py readout.md [--queries .ds-queries.log] [--checks .ds-checks.log] [--stamp]

In the Answer, "What it means" and "Why we believe it" sections:
- every line that states a number carries a tag: [q<n>] for a logged query,
  [check:<name>#<n>] for a logged check, or [given] for a number stated in the
  request (a threshold, a date range). One bracket may hold several: [q3, q4].
- every [q<n>] is a query that ran (through the runner, or pasted with --pasted);
- every [check:<name>#<n>] is a logged check whose "from" names queries that ran.
The Provenance section must have a "Reconciled:" line.

It also looks for each tagged number in what its tags hold: the query's rows
and row count, or the check's details and summary, as is or times 100, to the
decimals shown. A number it can't find is listed for the reviewer to confirm,
not failed: a difference or an interval worked out by hand is in no log until
it is logged with query.py --pasted. Counts up to 10 are not looked up.
ds-verify's `sources` check is the one that refuses a Headline it can't find.

A heading that is not one of the readout's own (a sub-heading over a table)
does not end a checked section: the lines under it are still checked.

Dates, a "95%" in front of "interval" or "CI", and digits inside names (v2,
q3) don't count as numbers. Logs default to $DS_QUERIES_LOG / $DS_CHECKS_LOG,
else the files in the current directory.

Prints "verify_readout: pass (...)" or "verify_readout: fail" with one line per
problem, then the [given] lines for the reviewer to confirm against the request,
then the numbers not found in their source, then any metric that two cited
queries (same --metric, --slice and as-of) report with no rate value in common.
With --stamp, a pass also writes "- Verified: <the pass line>" as the last line
of Provenance, replacing an earlier one, so the readout needs no second run.
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
CI_LEVEL = re.compile(r"\b(?:80|90|95|99)\s*[%％]\s*(?=(?:confidence\s+)?(?:interval|CI)\b|置信)", re.I)
LIST_MARKER = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
NUMBER = re.compile(r"(?<![A-Za-z_#\d.])[-+−]?\d+(?:[.,]\d+)*")
VERIFIED = re.compile(r"^\s*[-*]\s*Verified\s*:.*\n?", re.I | re.M)
CHECKED_SECTIONS = ("answer", "what it means", "why we believe")
READOUT_SECTIONS = CHECKED_SECTIONS + ("caveats", "provenance")


def _clean(text):
    text = re.sub(r"^```[a-z]*\s*$", "", text, flags=re.M)
    return text.replace("**", "").replace("__", "").replace("`", "")


def sections(text):
    parts = HEADING.split(_clean(text))
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def readout_sections(text):
    """(name, body) for each section, as verify() reads them. Inside a checked section, a
    heading that is not one of the readout's own (a sub-heading over a table, say) stays in
    the body, so its lines are still checked. sections() splits on every heading."""
    text = _clean(text)
    starts = []
    for head in HEADING.finditer(text):
        name = head.group(1).strip()
        in_checked = starts and starts[-1][0].lower().startswith(CHECKED_SECTIONS)
        if in_checked and not name.lower().startswith(READOUT_SECTIONS):
            continue
        starts.append((name, head.start(), head.end()))
    ends = [start for _, start, _ in starts[1:]] + [len(text)]
    return [(name, text[body:end]) for (name, _, body), end in zip(starts, ends)]


def numbers_in(line):
    body = LIST_MARKER.sub("", TAGS.sub(" ", LABELS.sub(" ", line)))
    body = CI_LEVEL.sub(" ", DATE.sub(" ", body))
    return NUMBER.findall(body)


def values_in(obj):
    """Every number in a logged result: rows, details or summary text."""
    if isinstance(obj, bool) or obj is None:
        return []
    if isinstance(obj, (int, float)):
        return [float(obj)]
    if isinstance(obj, str):
        return [float(n.replace("−", "-").replace(",", "")) for n in NUMBER.findall(obj)]
    if isinstance(obj, dict):
        obj = list(obj.values())
    return [v for item in obj for v in values_in(item)] if isinstance(obj, list) else []


def in_source(number, values):
    """True when the number, as written, rounds from a logged value or from 100 times one."""
    x = abs(float(number.replace("−", "-").replace(",", "")))
    tolerance = 0.5 * 10 ** -(len(number.split(".")[1]) if "." in number else 0) + 1e-9
    return any(abs(x - abs(v)) <= tolerance or abs(x - abs(v) * 100) <= tolerance for v in values)


def conflicts(cited, results):
    """Cited queries that name the same metric, slice and period but share no rate value."""
    groups = {}
    for qid in sorted(cited):
        entry = results.get(qid)
        if entry and entry.get("metric"):
            key = (entry["metric"].lower(), (entry.get("slice") or "all").lower(), entry.get("as_of"))
            groups.setdefault(key, []).append(entry)
    found = []
    for (metric, part, as_of), entries in groups.items():
        rates = {}
        for entry in entries:
            values = values_in(entry.get("rows"))
            rates[entry["id"]] = [v for v in values if v != int(v)] or values
        for i, a in enumerate(entries):
            for b in entries[i + 1:]:
                if not any(abs(x - y) <= 0.002 * max(abs(x), abs(y), 1e-9) for x in rates[a["id"]] for y in rates[b["id"]]):
                    found.append((metric, part, as_of, a, b, rates))
    return found


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
    results = {e["id"].lower(): e for e in queries if e.get("id") and e.get("status") == "ok"}
    problems, given = [], []
    stats = {"lines": 0, "numbers": 0, "queries": set(), "checks": set(), "unsourced": []}
    found = readout_sections(text)
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
            if numbers and tags and "given" not in tags:
                values = []
                for tag in tags:
                    if tag in results:
                        values += values_in(results[tag].get("rows")) + values_in(results[tag].get("row_count"))
                    elif tag.startswith("check:") and tag.split(":", 1)[1] in logged_checks:
                        entry = logged_checks[tag.split(":", 1)[1]]
                        values += values_in(entry.get("details")) + values_in(entry.get("summary"))
                missing = [n for n in numbers if not (n.isdigit() and int(n) <= 10) and not in_source(n, values)]
                if missing:
                    stats["unsourced"].append((missing, line.strip()))
    stats["conflicts"] = conflicts(stats["queries"], results)
    return list(dict.fromkeys(problems)), stats, given


def stamp(text, result):
    """Return text with '- Verified: <result>' as the last line of Provenance."""
    entry = f"- Verified: {result}\n"
    heads = list(HEADING.finditer(text))
    for i, head in enumerate(heads):
        if head.group(1).strip().lower().startswith("provenance"):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            block = VERIFIED.sub("", text[head.end():end]).rstrip("\n")
            rest = text[end:]
            return text[:head.end()] + block + "\n" + entry + ("\n" + rest if rest else "")
    return text.rstrip("\n") + "\n\n## Provenance\n" + entry


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("readout", help="the readout file (use - for stdin)")
    parser.add_argument("--queries", default=os.environ.get("DS_QUERIES_LOG") or ".ds-queries.log")
    parser.add_argument("--checks", default=os.environ.get("DS_CHECKS_LOG") or ".ds-checks.log")
    parser.add_argument("--stamp", action="store_true", help="on a pass, write the Verified line into the readout")
    args = parser.parse_args(argv)
    if args.stamp and args.readout == "-":
        print("verify_readout: --stamp needs a readout file, not stdin", file=sys.stderr)
        return 3
    try:
        text = sys.stdin.read() if args.readout == "-" else open(args.readout).read()
    except OSError as err:
        print(f"verify_readout: can't read the readout ({err})", file=sys.stderr)
        return 3
    problems, stats, given = verify(text, read_jsonl(args.queries), read_jsonl(args.checks))
    counts = (f"{stats['numbers']} numbers on {stats['lines']} lines; {len(stats['queries'])} queries, "
              f"{len(stats['checks'])} checks, {len(given)} given, "
              f"{sum(len(m) for m, _ in stats['unsourced'])} not found in their source"
              + (f", {len(stats['conflicts'])} metric reported with two values" if stats["conflicts"] else ""))
    if problems:
        print(f"verify_readout: fail ({counts})")
        for problem in problems:
            print(f"  - {problem}")
    else:
        result = f"verify_readout: pass ({counts})"
        print(result)
        if args.stamp:
            with open(args.readout, "w") as handle:
                handle.write(stamp(text, result))
            print("  stamped: the Verified line is in Provenance; no need to run this again")
    for line in given:
        print(f"  given (confirm against the request): {line}")
    for missing, line in stats["unsourced"]:
        print(f"  not in its source (confirm, or log how it was computed): {', '.join(missing)} in: {line}")
    for metric, part, as_of, a, b, rates in stats["conflicts"]:
        shown = "; ".join(f"{e['id']} gives {', '.join(f'{v:g}' for v in rates[e['id']][:4])}" for e in (a, b))
        print(f"  one metric, two values (confirm the definitions match): {metric} ({part}, through {as_of}): {shown}")
        for e in (a, b):
            print(f"    {e['id']}: {' '.join(e.get('sql', '').split())[:300]}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
