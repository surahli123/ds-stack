#!/usr/bin/env python3
"""Lint a markdown doc for the structure, format and length failures agents repeat.

    python3 doc_lint.py doc.md --type readout|memo|plan|handover|reference|other [--json]
    python3 doc_lint.py doc.md --spine spine.json     # type comes from the spine

Every rule traces to a failure counted in 119 agent-written docs (see
rules.json next to this file). Rules marked "fail" exit 1; "warn" rules are
for the author to judge. Exit 0 when nothing fails, 2 on a usage error.

This checks what a script can see: where the answer sits, emphasis, tables,
log drift, clutter, length. Whether the doc makes sense to its reader is the
cold-read skill's job.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass

HERE = os.path.dirname(os.path.abspath(__file__))
ANSWER_LABELS = r"answer|summary|tl;?dr|bottom line|decision|recommendation|bluf|the ask|headline|verdict|result"
HANDOVER_LABELS = ANSWER_LABELS + r"|status|state|next step|where things stand"
EMPHASIS_CAPS = {"NOT", "ONLY", "MUST", "NEVER", "ALWAYS", "CRITICAL", "IMPORTANT", "NOTE", "WARNING",
                 "LOCKED", "DONE", "NO", "DO", "DON'T", "REQUIRED", "MANDATORY", "BLOCKED", "CANNOT", "ALL"}
STOPWORDS = set("""a an the and or but if then else of to in on at by for with from as is are was were be been being
this that these those it its it's we you your our they their them he she his her not no yes can could should would will
may might must do does did done have has had into than so such also just more most less least very about over under
up down out off all any each every some other which who whom whose what when where why how there here i me my""".split())
STAT_WORDS = re.compile(r"\b(statistically significant|significant(?:ly)?|causal(?:ly)?|caused|drives|driven by|prove[sd]? that|definitively)\b", re.I)
STAT_SUPPORT = re.compile(r"(\bp\s*[<=>]|\bp-value|confidence interval|\b95% ci\b|\bci\b|\ba/b test|\bab test|\bt-test|\bz-test|chi-square|"
                          r"\bexperiment|\brandomi[sz]ed|\bholdout|\bcontrol group|difference-in-differences|\bregression discontinuity)", re.I)
ANSWER_LIKE = re.compile(r"\b(keep|recommend\w*|should|don't|do not|approve\w*|roll(?:ing)? back|ship|stop|choose|cancel|launch|kill|"
                         r"adopt|retire|merge|blocked|failing|fails|broken|is live|shipped|works|done|decided)\b|"
                         r"[-+\u2212]?\d+(?:\.\d+)?\s*(?:pp\b|%|percentage points?\b|x\b)", re.I)
METHOD_START = re.compile(r"^\W*(data sources?|method(?:ology)?|background|context|approach|scope|this (?:doc|document|note|page)|"
                          r"we (?:pulled|ran|looked|started)|i (?:ran|pulled|looked|started))\b", re.I)
RESTATED_HEADING = re.compile(r"\b(restated|recap|again|in summary|to summari[sz]e)\b", re.I)
COMMON_CODES = re.compile(r"^(?:Q[1-4]|H[1-6]|P[0-4]|V\d+)$")
HEDGES = re.compile(r"\b(might|may|could|possibly|likely|suggests?|appears?|seems?|perhaps|probably)\b", re.I)
THINKING = re.compile(r"\b(on second thought|hmm|wait,|to be honest|honest caveat|worth noting|it'?s worth|earned its keep|"
                      r"as (?:mentioned|noted) (?:above|earlier)|needless to say)\b|,\s*restated\b", re.I)
FIRST_PERSON_PROCESS = re.compile(r"\bI (ran|did|checked|read|looked|found|wrote|used|tried|spent|went|started|noticed|verified)\b")
METADATA = re.compile(r"^\s*(?:[-*]\s*)?\**(status|owner|date|author|workflow|session|tokens?|model|branch|commit|created|updated|"
                      r"last updated|sources?|grounding|reviewers?)\**\s*:", re.I)
AGENT_ARTIFACTS = re.compile(r"\bwf_[0-9a-f]{4,}|/private/tmp/|/tmp/(?:claude-\d+|ds-runs|tmp\.[A-Za-z0-9]+|[0-9a-f]{8,})\S*|"
                             r"\b\d+(?:\.\d+)?[MK] tokens\b|\bsession_[0-9A-Za-z]{8,}")
VERIFIED_BADGE = re.compile(r"\(verified\)|\u2713\s*verified|\u2705\s*verified|\bverified:\s|\*\*verified\b|\bverified\s*\u2713", re.I)
ID_CODES = re.compile(r"(?<![\w/.-])[A-Z]{1,2}#?\d{1,3}(?:[-–]\d{1,3})?(?![\w%])")
LOG_LINE = re.compile(r"\b(DONE|RESOLVED|FIXED|UPDATED?|SHIPPED|CLOSED|EXECUTED|RECONCILED|COMPLETED|MERGED)\b[^\n]{0,30}\d{4}-\d{2}-\d{2}|~~[^~]+~~")
LOG_HEADING = re.compile(r"(execution record|changelog|change log|activity log|history|update log|progress log|what (?:actually )?happened)", re.I)


@dataclass
class Finding:
    rule: str
    severity: str
    line: int
    message: str


def load_rules():
    with open(os.path.join(HERE, "rules.json")) as handle:
        return {k: v for k, v in json.load(handle).items() if not k.startswith("_")}


BUDGETS = load_rules()["D12"]["budgets"]


class Doc:
    def __init__(self, text):
        self.lines = text.splitlines()
        self.code = set()
        fence = False
        for i, line in enumerate(self.lines):
            if line.lstrip().startswith("```"):
                fence = not fence
                self.code.add(i)
            elif fence:
                self.code.add(i)
        self.headings = [(i, len(m.group(1)), m.group(2).strip()) for i, line in enumerate(self.lines)
                         if i not in self.code for m in [re.match(r"^(#{1,6})\s+(.*)$", line)] if m]
        appendix = next((i for i, _, t in self.headings if re.match(r"(appendix|annex)\b", t, re.I)), len(self.lines))
        self.body_end = appendix

    def appendix_word_count(self):
        return sum(len(self.words(line)) for i, line in enumerate(self.lines[self.body_end:], self.body_end)
                   if i not in self.code and not re.match(r"^#{1,6}\s", line))

    def prose_lines(self, end=None):
        end = self.body_end if end is None else end
        for i, line in enumerate(self.lines[:end]):
            if i in self.code or line.lstrip().startswith("|") or re.match(r"^#{1,6}\s", line):
                continue
            yield i, line

    def words(self, text):
        text = re.sub(r"`[^`]*`", " x ", text)
        return re.findall(r"[A-Za-z0-9][A-Za-z0-9'%.\-]*", text)

    def body_word_count(self):
        count = sum(len(self.words(line)) for _, line in self.prose_lines())
        for i, line in enumerate(self.lines[:self.body_end]):
            if i not in self.code and line.lstrip().startswith("|") and not re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
                count += len(self.words(line))
        return count

    def paragraph(self, index):
        """The run of non-blank lines around `index`."""
        start = end = index
        while start > 0 and self.lines[start - 1].strip():
            start -= 1
        while end + 1 < len(self.lines) and self.lines[end + 1].strip():
            end += 1
        return " ".join(self.lines[start:end + 1])

    def sections(self):
        bounds = [i for i, _, _ in self.headings] + [len(self.lines)]
        out = []
        for idx, (start, level, title) in enumerate(self.headings):
            text = " ".join(l for j, l in enumerate(self.lines[start + 1:bounds[idx + 1]], start + 1) if j not in self.code)
            out.append((start, title, text))
        return out


def answer_like_opening(doc):
    """Line of an H1 or first paragraph that states a claim or recommendation, else None."""
    seen = 0
    for i, line in enumerate(doc.lines[:doc.body_end]):
        if i in doc.code or not line.strip() or METADATA.match(line):
            continue
        text = re.sub(r"^#{1,6}\s+", "", line)
        if METHOD_START.match(text):
            return None
        if ANSWER_LIKE.search(text):
            return i
        seen += len(doc.words(line))
        if seen > 60:
            return None
    return None


def strip_quoted(line):
    return re.sub(r"`[^`]*`|\"[^\"\n]*\"|\u201c[^\u201d\n]*\u201d", " ", line)


def check(text, doc_type="other", rules=None):
    rules = rules or load_rules()
    doc = Doc(text)
    found = []

    def add(rule, line, message):
        found.append(Finding(rule, rules[rule]["severity"], line + 1, message))

    words_total = max(doc.body_word_count(), 1)
    per100 = 100 / words_total
    prose = list(doc.prose_lines())

    # D1 answer first: a labelled answer (or status, for handovers) within the first 150 words.
    labels = HANDOVER_LABELS if doc_type == "handover" else ANSWER_LABELS
    label_re = re.compile(rf"^\s*(?:#{{1,6}}\s+.*?\b|[-*]\s+\**\s*|\**\s*)({labels})\b", re.I)
    seen, located = 0, None
    for i, line in enumerate(doc.lines[:doc.body_end]):
        if i in doc.code:
            continue
        if re.match(r"^#\s", line) and seen == 0:
            continue
        if label_re.match(line):
            located = i
            break
        seen += len(doc.words(line))
        if seen > 150:
            break
    if located is None:
        located = answer_like_opening(doc)
    if located is None and doc_type != "reference":
        add("D1", 0, f"no labelled answer{' or status' if doc_type == 'handover' else ''} in the first 150 words; "
                     "open with the answer, decision or ask, then the evidence")

    # D2 bold density; D3 bold-label bullets; D4 caps emphasis.
    bold = [(i, m) for i, line in prose for m in re.finditer(r"\*\*[^*\n]+\*\*|__[^_\n]+__", line)]
    density = len(bold) * per100
    if density > rules["D2"]["threshold"]:
        add("D2", bold[0][0], f"{density:.1f} bold spans per 100 words (limit {rules['D2']['threshold']}); bold only what a skimmer must not miss")
    bullets = [(i, line) for i, line in prose if re.match(r"^\s*(?:[-*+]|\d+\.)\s+", line)]
    labelled = [i for i, line in bullets if re.match(r"^\s*(?:[-*+]|\d+\.)\s+\*\*[^*]+\*\*", line)]
    if len(bullets) >= 5 and len(labelled) / len(bullets) >= rules["D3"]["threshold"]:
        add("D3", labelled[0], f"{len(labelled)} of {len(bullets)} bullets open with a bold label; write sentences, or a table if it is data")
    caps = [(i, w) for i, line in prose for w in re.findall(r"\b[A-Z][A-Z']{1,}\b", strip_quoted(line)) if w in EMPHASIS_CAPS]
    if len(caps) >= rules["D4"]["threshold"]:
        add("D4", caps[0][0], f"{len(caps)} all-caps emphasis words ({', '.join(sorted({w for _, w in caps})[:5])}); say why it matters instead")

    # D5 log drift.
    log_hits = [i for i, line in enumerate(doc.lines) if i not in doc.code and LOG_LINE.search(line)]
    log_heads = [i for i, _, t in doc.headings if LOG_HEADING.search(t)]
    checkmarks = sum(line.count("✅") + line.count("✔") for i, line in enumerate(doc.lines) if i not in doc.code)
    if log_hits or log_heads or checkmarks >= 3:
        where = (log_hits + log_heads + [0])[0]
        add("D5", where, "the doc is turning into a log (dated DONE lines, strikethrough, history sections or check marks); "
                         "keep only the current state and let git hold the history")

    # D6 the same point restated: content-word overlap between sections.
    def content(text):
        return {w.lower() for w in doc.words(text) if w.lower() not in STOPWORDS and len(w) > 2}
    for i, _, title in doc.headings:
        if RESTATED_HEADING.search(title):
            add("D6", i, f"heading '{title[:40]}' announces a repeat; say each point once, where it belongs")
            break
    secs = [(start, title, content(text)) for start, title, text in doc.sections()]
    secs = [s for s in secs if len(s[2]) >= rules["D6"]["min_section_words"]]
    for a in range(len(secs)):
        for b in range(a + 1, len(secs)):
            sa, sb = secs[a][2], secs[b][2]
            overlap = len(sa & sb) / min(len(sa), len(sb))
            if overlap >= rules["D6"]["threshold"]:
                add("D6", secs[b][0], f"sections '{secs[a][1][:40]}' and '{secs[b][1][:40]}' share {overlap:.0%} of their content words; "
                                      "say each point once, where it belongs")

    # D7 process detail standing in for results.
    meta = [i for i, line in enumerate(doc.lines[:12]) if METADATA.match(line)]
    if len(meta) >= 2:
        add("D7", meta[0], f"{len(meta)} metadata fields open the doc; the reader needs the answer first, provenance last")
    verified = [i for i, line in prose if VERIFIED_BADGE.search(line)]
    if len(verified) >= rules["D7"]["verified_badges"]:
        add("D7", verified[0], f"{len(verified)} 'verified' badges; state the evidence once, in the evidence section")
    narration = [i for i, line in prose if FIRST_PERSON_PROCESS.search(line)]
    if len(narration) >= 2:
        add("D7", narration[0], "first-person process narration ('I ran', 'I checked'); report what is true, not what you did")
    artifacts = [i for i, line in enumerate(doc.lines) if AGENT_ARTIFACTS.search(line)]
    if artifacts:
        add("D7", artifacts[0], "agent artifacts (workflow ids, /tmp paths, token counts); the reader can't use them")

    # D8 inline clutter: code spans, undefined ID codes, arrows.
    code_spans = sum(len(re.findall(r"`[^`\n]+`", line)) for _, line in prose)
    if doc_type != "handover" and code_spans * per100 > rules["D8"]["code_per_100"]:
        add("D8", 0, f"{code_spans * per100:.1f} inline-code spans per 100 words; keep code font for real names the reader will type")
    defined = {m.group(1) for m in re.finditer(r"(?:^|\|)\s*[-*]?\s*\**([A-Z]{1,2}#?\d{1,3})\**\s*(?:[:(=\u2014\u2013|]|\s-\s)", text, re.M)}
    ids = [(i, m.group(0)) for i, line in prose for m in ID_CODES.finditer(re.sub(r"`[^`]*`", " ", line))
           if m.group(0) not in defined and not COMMON_CODES.match(m.group(0).split("-")[0].split("\u2013")[0])]
    if len(ids) * per100 >= rules["D8"]["ids_per_100"]:
        add("D8", ids[0][0], f"{len(ids)} ID codes such as {', '.join(sorted({c for _, c in ids})[:4])}; use names, or define each code once")
    arrows = sum(line.count("→") + line.count("->") + line.count("=>") for _, line in prose)
    if arrows >= rules["D8"]["arrows"]:
        add("D8", 0, f"{arrows} arrows; write the verb ('becomes', 'leads to', 'then')")

    # D9 prose packed into tables, and empty template tables.
    for i, line in enumerate(doc.lines):
        if i in doc.code or not line.lstrip().startswith("|") or re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        long = [c for c in cells if len(doc.words(c)) > rules["D9"]["max_cell_words"]]
        if long:
            add("D9", i, f"a table cell has {len(doc.words(long[0]))} words; move the prose out and keep the cell to a fact")
            break
    for i, line in enumerate(doc.lines):
        if i in doc.code or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not re.match(r"^\s*\|[\s:|-]+\|\s*$", line) and (all(not c for c in cells) or all(re.fullmatch(r"<[^>]*>|\.\.\.|TBD|", c) for c in cells)):
            add("D9", i, "an empty or placeholder table row; fill it or delete the table")
            break

    # D10 who is the reader.
    body = " ".join(line for _, line in prose)
    if re.search(r"\byou(?:r|rs)?\b", body, re.I) and re.search(r"\bthe (?:user|owner)\b", body, re.I):
        add("D10", 0, "the doc talks to 'you' and about 'the user/owner'; pick one reader and address them one way")

    # D11 thinking out loud and self-congratulation.
    thinking = [i for i, line in enumerate(doc.lines[:doc.body_end]) if i not in doc.code and THINKING.search(line)]
    if thinking:
        add("D11", thinking[0], "thinking out loud or self-praise left in; delete it or state the conclusion")

    # D12 length budget for the doc type. The appendix counts at half weight, so
    # renaming a section "Appendix" doesn't make its words free.
    budget = BUDGETS.get(doc_type, BUDGETS["other"])
    appendix_words = doc.appendix_word_count()
    weighted = words_total + appendix_words // 2
    if weighted > budget:
        extra = f" + {appendix_words} appendix words at half weight" if appendix_words else ""
        add("D12", 0, f"{words_total} body words{extra} = {weighted}; the {doc_type} budget is {budget}. "
                      "Cut repetition and process first, then move detail to an appendix")

    # D13 statistical and causal words without support nearby (DS editing guide).
    for i, line in prose:
        match = STAT_WORDS.search(line)
        if match and not STAT_SUPPORT.search(doc.paragraph(i)):
            add("D13", i, f"'{match.group(0)}' with no test, interval or design named nearby; back it or soften it")
            break

    # D14 hedges in the answer.
    if located is not None:
        answer_text = " ".join(doc.lines[located:located + 6])
        hedges = HEDGES.findall(answer_text)
        if len(hedges) > 1:
            add("D14", located, f"{len(hedges)} hedges in the answer ({', '.join(hedges[:3])}); state it at the strength the evidence supports")

    return found, words_total


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path")
    parser.add_argument("--type", choices=sorted(BUDGETS))
    parser.add_argument("--spine", help="spine.json written by ds-doc; its 'type' sets --type")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        with open(args.path, encoding="utf-8") as handle:
            text = handle.read()
        if args.spine:
            with open(args.spine, encoding="utf-8") as handle:
                spine_type = json.load(handle).get("type")
            if args.type and spine_type and args.type != spine_type:
                print(f"doc_lint: --type {args.type} contradicts the spine's type {spine_type}", file=sys.stderr)
                return 2
            args.type = args.type or spine_type
    except (OSError, ValueError) as err:
        print(f"doc_lint: {err}", file=sys.stderr)
        return 2
    args.type = args.type or "other"
    if args.type not in BUDGETS:
        print(f"doc_lint: unknown type {args.type!r}", file=sys.stderr)
        return 2
    findings, words = check(text, args.type)
    fails = [f for f in findings if f.severity == "fail"]
    if args.json:
        print(json.dumps({"path": args.path, "type": args.type, "words": words,
                          "fails": len(fails), "warns": len(findings) - len(fails),
                          "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        for f in findings:
            print(f"{args.path}:{f.line}: {f.severity} {f.rule} {f.message}")
        print(f"{len(fails)} fail, {len(findings) - len(fails)} warn, {words} body words ({args.type})")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
