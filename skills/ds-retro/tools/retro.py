#!/usr/bin/env python3
"""Find the mistakes that repeat across finished analyses and propose where a fix belongs. Never applies one.

    python3 tools/retro.py --analyses <analysis dir> [...] [--min-runs 2] [--out ds-retro] [--json report.json]
    python3 tools/retro.py --results eval/results/<dir> [...] [--arms full]     # eval runs, graded by grade.py

An analysis directory holds a readout (readout.md or result.md), its logs (.ds-queries.log or queries.log,
.ds-checks.log or checks.log), and when available the request (request.md) and the database (warehouse.db);
the overlay comes from $DS_OVERLAY_DIR. An eval results directory is read run by run, with each fixture's
database, overlay and task from eval/fixtures, and the grader's reasons from its summary.json.

Signals: every ds-verify failure and could_not_verify on each run, and for eval runs the grader's reason for
each miss. Each signal is reduced to a pattern (numbers, quotes and ids taken out) and counted once per run. A
pattern seen in --min-runs runs or more becomes a proposal:
  - where the fix belongs (the ds-mode skill, the overlay, the project's setup, or a person's call);
  - the proposed rule, and whether ds-mode's SKILL.md already has a rule for it, in which case the problem
    is compliance and the proposal is a gate (a check), not more text;
  - a fixture sketch for the eval gate: plain prompting misses it, ds-mode with the rule gets it right,
    and it fails again without the rule.
A person approves each proposal; metric definitions are always a person's to write.

Exit code: 0 no proposal, 1 at least one, 3 usage error.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(HERE))
REPO = os.path.dirname(SKILLS)
sys.path.insert(0, os.path.join(SKILLS, "ds-verify", "tools"))

import ds_verify as dv  # noqa: E402

DS_MODE_SKILL = os.path.join(SKILLS, "ds-mode", "SKILL.md")
FIXTURES = os.path.join(REPO, "eval", "fixtures")

# (pattern regex on the normalized signal, where the fix belongs, the proposal, a fixture sketch,
#  a phrase that shows ds-mode already has a rule for it)
LESSONS = [
    (r"^overlay: the overlay defines <metric>; the metric line lacks", "ds-mode skill",
     "Run ds-verify before replying, so a readout that ignores metrics.json fails before anyone reads it.",
     "A metric whose team definition differs from the obvious one (as f6), with metrics.json in the overlay.",
     "metrics.json"),
    (r"^overlay: the overlay marks <metric> unavailable", "ds-mode skill",
     "When metrics.json marks the metric unavailable, answer can't tell and give any proxy only on a "
     "'not computed' line.",
     "A request for a metric the warehouse can't compute, with a tempting proxy column (as f7).",
     "available"),
    (r"^estimand: the request asks for .* headline is in|^grade: headline has no number in", "ds-mode skill",
     "Write the Headline in the unit the request asks for: percent for a level, pp for a change.",
     "A level question asked 'in percent', where the readout's natural comparison is a change in pp.",
     "unit the request"),
    (r"^estimand: the causal effect gives a number", "ds-mode skill",
     "Give a Causal effect number only 'from <design>' for a randomized test or another identifying design.",
     "A before/after drop with a launch on the boundary and no holdout (as f1).",
     "Causal effect is a number only"),
    (r"^alternatives: 'ruled in' is hedged without a flagged check", "ds-mode skill",
     "Add a third verdict, 'not ruled out', for an alternative the data can't decide; 'ruled in' only for "
     "what the evidence shows.",
     "A cause the data can neither confirm nor exclude, next to one the data does confirm.",
     "not ruled out"),
    (r"^alternatives: none of the|^grade: unparseable: none of the .* alternative lines", "ds-mode skill",
     "End every alternative with 'ruled in' or 'ruled out', in English, whatever the readout's language.",
     "Any fixture run with a Chinese prompt suffix; the parser needs the fixed words.",
     "ruled in"),
    (r"^estimand: (the headline gives a number, but no estimate line does|no headline number is one of)", "ds-mode skill",
     "Keep the three estimate lines (Observed, Adjusted, Causal effect) in every readout, and make the Headline one "
     "of them.",
     "A drop with a mix shift, where the observed and adjusted changes differ (as f1).",
     "Observed:"),
    (r"^flags: .* the readout doesn't report it", "ds-mode skill",
     "List every check that ran under 'Checks run', by its tag, including a failed call you then reran.",
     "A fixture where a first check call fails on a wrong argument and a rerun passes (as f1's completeness).",
     "Checks run"),
    (r"^sources: headline: .* (isn't in|cites output with no numbers)", "ds-mode skill",
     "Compute the Headline number in the query or check it cites, so the number appears in that output.",
     "A rate the analyst would naturally divide by hand from two summed counts (as f6).",
     "Compute the Headline"),
    (r"^sources: headline: .* cites only pasted|^replay: \[q#\] is a pasted result", "ds-mode skill",
     "Run every number through the query runner; paste a result only when the runner can't compute it, "
     "and say why.",
     "An experiment readout whose interval is easy to compute by hand (as f5).",
     "--pasted"),
    (r"^estimand: no request was given|^flags: no check log", "project setup",
     "Save the request to request.md and keep the logs next to the readout, so ds-verify can check them.",
     "None: this is setup, not a model mistake.", None),
    (r"^grade: abstained on a case with a valid answer", "ds-mode skill",
     "Answer with the estimate that fits the question when the cause isn't identified; 'can't tell' only "
     "when the data can't support the number.",
     "A full-rollout question where Adjusted answers it and the cause is not identified (as f1, f3).",
     "not a reason to abstain"),
    (r"^grade: answered # where the right answer is can't tell", "overlay (a person writes it)",
     "Mark the metric available: false in metrics.json, with a note on why, so the agent stops at it.",
     "A request for a metric whose only column is a look-alike (as f7).", "available"),
    (r"^grade: headline # outside", "a person decides",
     "Read the runs' readouts and ds-verify reports: a wrong number with no failing check means a check is "
     "missing, and the mistake class goes to references/mistake-classes.md.",
     "Reproduce the mechanism behind the wrong number in a small synthetic table.", None),
]


def normalize(text):
    """A pattern key: the readout line a message quotes, metric names, quotes, ids and numbers taken out."""
    text = str(text)
    text = re.sub(r"(the overlay defines) \S+ as .*?; (the Metric line lacks) .*", r"\1 <metric>; \2 <columns>", text)
    text = re.sub(r"(the overlay marks) \S+ (unavailable).*", r"\1 <metric> \2", text)
    text = re.sub(r"('ruled in' is hedged)(?: and no flagged check backs it|; a flagged check shows the anomaly).*",
                  lambda m: m.group(0)[:m.end(1) - m.start(0)] + (" without a flagged check" if "no flagged" in m.group(0)
                                                                     else " with a flagged check"), text)
    text = re.sub(r":\s*(?:-\s|Headline:|says neither).*$", "", text)
    text = re.sub(r"`[^`]*`|\"[^\"]*\"|“[^”]*”", "'…'", text)
    text = re.sub(r"\[(q\d+|check:[^\]]+)\]", "[q#]", text)
    text = re.sub(r"\b[a-z_]+#\d+\b", "check#", text)
    text = re.sub(r"[-+−]?\d+(?:[.,]\d+)*(?:%|pp)?", "#", text)
    return re.sub(r"\s+", " ", text).strip().lower()[:160]


def lesson_for(key):
    for pattern, layer, proposal, fixture, probe in LESSONS:
        if re.search(pattern, key):
            return {"layer": layer, "proposal": proposal, "fixture": fixture, "probe": probe}
    return {"layer": "a person decides", "proposal": "No lesson matches this pattern yet; read the examples.",
            "fixture": "Write one from the examples if the mistake is real.", "probe": None}


def covered(probe):
    if not probe or not os.path.exists(DS_MODE_SKILL):
        return False
    return probe.lower() in open(DS_MODE_SKILL, encoding="utf-8").read().lower()


# --- reading runs --------------------------------------------------------------------------------------------

def first(folder, *names):
    return next((os.path.join(folder, n) for n in names if os.path.exists(os.path.join(folder, n))), None)


def read(path):
    return open(path, encoding="utf-8", errors="replace").read() if path else None


def analysis_runs(folders):
    for folder in folders:
        readout = first(folder, "readout.md", "result.md")
        if not readout:
            print(f"ds-retro: skipping {folder}: no readout.md or result.md", file=sys.stderr)
            continue
        yield {"id": folder, "readout": readout, "queries": first(folder, ".ds-queries.log", "queries.log"),
               "checks": first(folder, ".ds-checks.log", "checks.log"), "request": first(folder, "request.md"),
               "db": first(folder, "warehouse.db"), "overlay": os.environ.get("DS_OVERLAY_DIR"), "grade": None}


def eval_runs(results_dirs, arms):
    for results in results_dirs:
        grades = {}
        summary = os.path.join(results, "summary.json")
        if os.path.exists(summary):
            for run in json.load(open(summary)).get("runs", []):
                grades[f"{run['fixture']}__{run['arm']}__{run['run']}"] = run
        for name in sorted(os.listdir(results)):
            folder = os.path.join(results, name)
            meta_path = os.path.join(folder, "meta.json")
            if not os.path.isfile(meta_path):
                continue
            meta = json.load(open(meta_path))
            if meta.get("arm") not in arms or meta.get("execution", "ok") not in ("ok", "timeout", "max_turns", "empty_reply"):
                continue
            fixture = os.path.join(FIXTURES, meta["fixture"])
            overlay = os.path.join(fixture, "overlay")
            yield {"id": os.path.join(os.path.basename(results.rstrip("/")), name),
                   "readout": first(folder, "result.md"), "queries": first(folder, "queries.log"),
                   "checks": first(folder, "checks.log"), "request": first(fixture, "task.md"),
                   "db": first(fixture, "warehouse.db"), "overlay": overlay if os.path.isdir(overlay) else None,
                   "grade": grades.get(name)}


def signals(run):
    """[(pattern key, the message it came from)] for one run, each pattern once."""
    text = read(run["readout"]) or ""
    queries = dv.vr.read_jsonl(run["queries"]) if run["queries"] else None
    checks = dv.vr.read_jsonl(run["checks"]) if run["checks"] else None
    report = dv.run_all(text, queries, checks, run["db"], run["overlay"], read(run["request"]))
    found = [(f"{f['check']}: {f['message']}") for f in report["findings"] if f["status"] in ("fail", "could_not_verify")]
    grade = run.get("grade")
    if grade and not grade.get("correct") and grade.get("miss") != "not_executed":
        found.append(f"grade: {grade.get('reason', '')}")
    seen, out = set(), []
    for message in found:
        key = normalize(message)
        if key not in seen:
            seen.add(key)
            out.append((key, message))
    return out


# --- proposals -----------------------------------------------------------------------------------------------

def propose(runs, min_runs):
    groups = {}
    for run in runs:
        for key, message in signals(run):
            groups.setdefault(key, []).append((run["id"], message))
    proposals = []
    for key, hits in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if len(hits) < min_runs:
            continue
        lesson = lesson_for(key)
        proposal = {"pattern": key, "runs": len(hits), "examples": hits[:3], **lesson, "covered": covered(lesson["probe"])}
        if key.startswith("grade:"):
            # Would the existing gate have caught these misses? Count the ds-verify failures on the same runs.
            runs_hit = {run for run, _ in hits}
            proposal["caught"] = sum(1 for run in runs_hit
                                     if any(r == run and not k.startswith("grade:") for k, rs in groups.items() for r, _ in rs))
        proposals.append(proposal)
    return proposals, {k: len(v) for k, v in groups.items()}


def render(proposals, counts, runs_read, min_runs):
    lines = [f"# ds-retro: {len(proposals)} proposal(s) from {runs_read} run(s)", "",
             f"Each pattern below was seen in {min_runs} or more runs. These are proposals: a person approves each "
             "one, and it goes in only after the eval gate (plain prompting misses its fixture, ds-mode with the rule "
             "gets it right, the fixture fails again without the rule). Metric definitions are a person's to write.", ""]
    for i, p in enumerate(proposals, 1):
        lines += [f"## {i}. {p['pattern']}", "",
                  f"- Seen in: {p['runs']} runs",
                  f"- Where the fix belongs: {p['layer']}",
                  f"- Proposal: {p['proposal']}"]
        if p["covered"]:
            lines.append("- ds-mode already has a rule for this, so the runs broke it: prefer a gate that catches it "
                         "(ds-verify run before replying) over more text.")
        if "caught" in p:
            lines.append(f"- ds-verify also failed {p['caught']} of these {p['runs']} runs, so running it before replying "
                         f"would have caught {'all' if p['caught'] == p['runs'] else 'some'} of them.")
        lines.append(f"- Fixture for the eval gate: {p['fixture']}")
        lines.append("- Examples:")
        lines += [f"  - {run}: {message[:200]}" for run, message in p["examples"]]
        lines.append("")
    rare = sorted((k for k, n in counts.items() if n < min_runs))
    if rare:
        lines += [f"Seen in fewer than {min_runs} runs, so not proposed yet: {len(rare)} pattern(s)."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--analyses", nargs="*", default=[], help="finished analysis directories")
    parser.add_argument("--results", nargs="*", default=[], help="eval results directories")
    parser.add_argument("--arms", default="full", help="eval arms to read (comma-separated)")
    parser.add_argument("--min-runs", type=int, default=2, help="runs a pattern needs before it is proposed")
    parser.add_argument("--out", default="ds-retro", help="where proposals.md goes")
    parser.add_argument("--json", help="also write the proposals as JSON")
    args = parser.parse_args(argv)
    missing = [d for d in args.analyses + args.results if not os.path.isdir(d)]
    if missing or not (args.analyses or args.results):
        print(f"ds-retro: give --analyses or --results directories{'; not found: ' + ', '.join(missing) if missing else ''}",
              file=sys.stderr)
        return 3
    runs = list(analysis_runs(args.analyses)) + list(eval_runs(args.results, args.arms.split(",")))
    proposals, counts = propose(runs, args.min_runs)
    text = render(proposals, counts, len(runs), args.min_runs)
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, ".gitignore"), "w") as handle:
        handle.write("# Proposals quote readouts; keep them out of git unless a person copies one into a PR.\n*\n")
    with open(os.path.join(args.out, "proposals.md"), "w", encoding="utf-8") as handle:
        handle.write(text)
    print(text)
    if args.json:
        with open(args.json, "w") as handle:
            json.dump({"proposals": proposals, "counts": counts, "runs": len(runs)}, handle, indent=2, default=str)
    return 1 if proposals else 0


if __name__ == "__main__":
    sys.exit(main())
