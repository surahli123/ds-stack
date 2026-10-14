"""Parse a ds-mode readout into fields a script can grade.

The readout format lives in skills/ds-mode/SKILL.md. Parsing is tolerant of
markdown decoration and of common phrasings, and reports what it could not
read instead of guessing:

- the headline yields every (number, unit) candidate; the grader picks the one
  in the gold unit, falls back to a unitless number, and never takes a number in
  another unit. Numbers glued to letters (v2, W40), dates and confidence levels
  ("95% CI") are ignored.
- full-width punctuation, the Unicode minus and Chinese units and range words
  (个百分点, 至) are normalized first. The fixed words the grader reads (section
  headings, "Headline:", "ruled in/out", check names) are English by contract;
  a readout whose alternatives all lack them gets a parse error, not a silent
  empty list.
- a headline with no number and words like "can't tell" or "insufficient" is an
  abstention.
- the Answer's estimate lines (Observed, Adjusted, Causal effect) are read
  separately, each as a number or as "not identified" / "not computed", so the
  grader can score the estimand the task asks for. A headline with two
  different estimates in the same unit before its parenthesis is a parse error.
- alternative lines match "ruled in/out" anywhere; "not ruled in/out" reads as
  undetermined. Bullet lines in that list that match neither are kept in
  `dropped` so the summary can report parse loss per arm.
"""

import re
from dataclasses import dataclass, field

NUMBER = r"(?<![\w.\-−])([-+−]?\d+(?:\.\d+)?)"
UNIT = r"\s*(pp\b|percentage[\s-]points?\b|points?\b|个?百分点|%|percent\b)"
CI_LEVEL = re.compile(r"\b(?:80|90|95|99)\s*%\s*(?=(?:confidence\s+)?(?:interval|CI)\b|置信)", re.I)
FULL_WIDTH = str.maketrans({"（": "(", "）": ")", "：": ":", "，": ",", "；": ";", "−": "-", "％": "%"})
DATE = re.compile(r"\b\d{4}-\d{2}(?:-\d{2})?\b|\b\d{4}-W\d{2}\b", re.I)
ABSTAIN_WORDS = re.compile(r"can['’]?t|cannot|can not|unable|unknown|insufficient|not enough|"
                           r"no reliable|indeterminate|undetermined|inconclusive|not possible", re.I)
NEGATIVE_WORDS = re.compile(r"\b(fell|fall|drop(?:ped)?|decreas\w*|declin\w*|down|lower|loss|lost|reduc\w*)\b", re.I)
HEADING = re.compile(r"^#{1,4}\s+(.+?)\s*#*\s*$", re.M)
HEADLINE = re.compile(r"^\s*[-*]?\s*headline\s*:\s*(.+?)\s*$", re.I | re.M)
VERDICT = re.compile(r"\b(not\s+)?ruled[\s-]*(?:(?:it|this|them|that)\s+)?(in|out)\b", re.I)
NAME_SPLIT = re.compile(r"\s*(?::|—|–|\s-\s)\s*")
CHECK = re.compile(r"^\s*[-*]\s*([a-z_]+)(?:\s*\([^)]*\))?\s*:\s*(pass|flag|fail|could[ _]not[ _]run|skipped)\b", re.I)
ESTIMATE = re.compile(r"^\s*[-*]?\s*(observed|adjusted|causal effect)\s*:\s*(.+?)\s*$", re.I | re.M)
TRACE_TAGS = re.compile(r"\[\s*(?:q\d+|check:[a-z_]+#\d+|given)(?:\s*[,;|]\s*(?:q\d+|check:[a-z_]+#\d+|given))*\s*\]", re.I)
LABEL = re.compile(r"\[(measured|inferred|guess)\]", re.I)
INTERVAL = re.compile(r"([-+−]?\d+(?:\.\d+)?)\s*%?\s*(?:to|,|–|—|\.\.\.?)\s*([-+−]?\d+(?:\.\d+)?)", re.I)
UNIT_NAMES = {"pp": "pp", "%": "percent", "percent": "percent"}


@dataclass
class Readout:
    headline: str = ""
    abstained: bool = False
    candidates: list = field(default_factory=list)
    interval: tuple | None = None
    alternatives: list = field(default_factory=list)
    dropped: list = field(default_factory=list)
    checks: dict = field(default_factory=dict)
    estimates: dict = field(default_factory=dict)
    sections: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)

    @property
    def ok(self):
        return not self.errors

    @property
    def value(self):
        return self.candidates[0][0] if self.candidates else None

    def value_in(self, unit):
        """First headline number in `unit` ('pp' or 'percent'), else the first unitless
        number. None when the headline only has numbers in another unit."""
        return pick(self.candidates, unit)

    def estimate_in(self, name, unit):
        """The number on an estimate line ('observed', 'adjusted', 'causal effect'), or None."""
        line = self.estimates.get(name)
        return pick(line["candidates"], unit) if line and line["status"] == "number" else None


def pick(candidates, unit):
    for number, found in candidates:
        if found == unit:
            return number
    return next((number for number, found in candidates if found is None), None)


def _clean(text):
    text = re.sub(r"^```[a-z]*\s*$", "", text, flags=re.M)
    text = TRACE_TAGS.sub(" ", text).translate(FULL_WIDTH)
    text = re.sub(r"\s*至\s*", " to ", text)
    return text.replace("**", "").replace("__", "").replace("`", "")


def _sections(text):
    parts = HEADING.split(text)
    return {parts[i].strip().lower(): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def _unit(raw):
    raw = raw.lower().strip()
    if raw.startswith("percentage") or raw.startswith("point") or raw == "pp" or raw.endswith("百分点"):
        return "pp"
    return UNIT_NAMES.get(raw, raw)


def _numbers_with_units(text, negative):
    found = []
    for match in re.finditer(NUMBER + f"(?:{UNIT})?", text, re.I):
        raw, unit = match.group(1), match.group(2)
        value = float(raw)
        if negative and raw[0] not in "+-":
            value = -value
        found.append((value, _unit(unit) if unit else None))
    return found


def _candidates(headline):
    """Order: numbers with a unit before the parenthesis, then with a unit inside
    it (an interval or a restatement), then unitless numbers before it."""
    text = CI_LEVEL.sub(" ", DATE.sub(" ", headline))
    head, _, paren = text.partition("(")
    negative = bool(NEGATIVE_WORDS.search(head))
    in_head = _numbers_with_units(head, negative)
    in_paren = [c for c in _numbers_with_units(paren, negative) if c[1]]
    return [c for c in in_head if c[1]] + in_paren + [c for c in in_head if not c[1]]


def parse(text):
    out = Readout()
    cleaned = _clean(text or "")
    out.sections = _sections(cleaned)
    answer = next((body for name, body in out.sections.items() if name.startswith("answer")), None)
    if answer is None:
        out.errors.append("no Answer section")
        return out
    match = HEADLINE.search(answer)
    if not match:
        out.errors.append("no 'Headline:' line in the Answer section")
        return out

    out.headline = match.group(1)
    out.candidates = _candidates(out.headline)
    head = CI_LEVEL.sub(" ", DATE.sub(" ", out.headline)).partition("(")[0]
    estimates = {c for c in _numbers_with_units(head, False) if c[1] in ("pp", "percent")}
    if len({unit for _, unit in estimates}) == 1 and len(estimates) > 1:
        out.errors.append(f"headline gives {len(estimates)} different estimates before its parenthesis; give one")
    for name, text in ESTIMATE.findall(answer):
        status = re.match(r"\s*not\s+(identified|computed)", text, re.I)
        found = _candidates(text)
        out.estimates[name.lower()] = {"text": text, "candidates": found,
                                       "status": f"not {status.group(1).lower()}" if status else ("number" if found else "unreadable")}
    if not out.candidates:
        if ABSTAIN_WORDS.search(out.headline):
            out.abstained = True
        else:
            out.errors.append(f"headline has neither a number nor an abstention: {out.headline!r}")
    elif re.match(r"^\s*(can['’]?t|cannot|can not)\s+tell", out.headline, re.I):
        out.abstained = True
    if "(" in out.headline:
        bounds = INTERVAL.search(CI_LEVEL.sub(" ", DATE.sub(" ", out.headline.split("(", 1)[1])))
        if bounds:
            low, high = (float(b) for b in bounds.groups())
            out.interval = (min(low, high), max(low, high))

    why = next((body for name, body in out.sections.items() if name.startswith("why")), "")
    in_alternatives = False
    for line in why.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*]\s*alternatives considered", stripped, re.I):
            in_alternatives = True
            continue
        if re.match(r"^[-*]\s*checks run", stripped, re.I):
            in_alternatives = False
            continue
        check = CHECK.match(line)
        if check and not in_alternatives:
            out.checks[check.group(1).lower()] = check.group(2).lower().replace(" ", "_")
            continue
        if not re.match(r"^[-*]\s+\S", stripped):
            continue
        body = re.sub(r"^[-*]\s*", "", stripped)
        verdict = VERDICT.search(body)
        if verdict:
            before = body[:verdict.start()].strip()
            subject = before or re.sub(r"^\s*(?::|by)?\s*", "", body[verdict.end():]).split(",")[0]
            name = NAME_SPLIT.split(subject.strip(), maxsplit=1)[0].strip().lower()
            label = LABEL.search(stripped)
            out.alternatives.append({
                "name": name,
                "line": body.lower(),
                "verdict": "undetermined" if verdict.group(1) else verdict.group(2).lower(),
                "label": label.group(1).lower() if label else None,
            })
        elif in_alternatives:
            out.dropped.append(stripped)
    if out.dropped and not out.alternatives:
        out.errors.append(f"none of the {len(out.dropped)} alternative lines says 'ruled in' or 'ruled out'")
    return out
