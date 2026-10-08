"""Parse a ds-mode readout into fields a script can grade.

The readout format lives in skills/ds-mode/SKILL.md. Parsing is tolerant of
markdown decoration (bold, backticks, code fences) but strict about the parts
that carry the answer: an `## Answer` section with a `Headline:` line.
"""

import re
from dataclasses import dataclass, field

NUMBER = r"[-+−]?\d+(?:\.\d+)?"
ABSTAIN = re.compile(r"^(can['’]?t|cannot|can not)\s+tell", re.I)
HEADLINE = re.compile(r"^\s*headline\s*:\s*(.+?)\s*$", re.I | re.M)
ALTERNATIVE = re.compile(r"^\s*[-*]\s*(.+?)\s*:\s*ruled\s+(in|out)\b(.*)$", re.I)
CHECK = re.compile(r"^\s*[-*]\s*([a-z_]+)\s*:\s*(pass|fail|could[ _]not[ _]run|skipped)\b", re.I)
LABEL = re.compile(r"\[(measured|inferred|guess)\]", re.I)
INTERVAL = re.compile(rf"({NUMBER})\s*(?:to|,|–|—|\.\.\.?)\s*({NUMBER})", re.I)


@dataclass
class Readout:
    headline: str = ""
    abstained: bool = False
    value: float | None = None
    interval: tuple | None = None
    alternatives: list = field(default_factory=list)
    checks: dict = field(default_factory=dict)
    sections: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)

    @property
    def ok(self):
        return not self.errors


def _clean(text):
    text = re.sub(r"^```[a-z]*\s*$", "", text, flags=re.M)
    return text.replace("**", "").replace("`", "").replace("−", "-")


def _sections(text):
    parts = re.split(r"^##\s+(.+?)\s*$", text, flags=re.M)
    return {parts[i].strip().lower(): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def _numbers(text):
    return [float(n.replace("−", "-")) for n in re.findall(NUMBER, text)]


def parse(text):
    out = Readout()
    cleaned = _clean(text or "")
    out.sections = _sections(cleaned)
    answer = next((body for name, body in out.sections.items() if name.startswith("answer")), None)
    if answer is None:
        out.errors.append("no '## Answer' section")
        return out
    match = HEADLINE.search(answer)
    if not match:
        out.errors.append("no 'Headline:' line in the Answer section")
        return out

    out.headline = match.group(1)
    if ABSTAIN.match(out.headline):
        out.abstained = True
    else:
        head, _, rest = out.headline.partition("(")
        values = _numbers(head)
        if not values:
            out.errors.append(f"headline has no number: {out.headline!r}")
        else:
            out.value = values[0]
        bounds = INTERVAL.search(rest)
        if bounds:
            low, high = (float(b.replace("−", "-")) for b in bounds.groups())
            out.interval = (min(low, high), max(low, high))

    why = next((body for name, body in out.sections.items() if name.startswith("why")), "")
    for line in why.splitlines():
        alt = ALTERNATIVE.match(line)
        if alt:
            label = LABEL.search(alt.group(3))
            out.alternatives.append({
                "name": alt.group(1).strip().lower(),
                "verdict": alt.group(2).lower(),
                "label": label.group(1).lower() if label else None,
            })
            continue
        check = CHECK.match(line)
        if check:
            status = check.group(2).lower().replace(" ", "_")
            out.checks[check.group(1).lower()] = status
    return out
