"""Shared result format and run log for every check.

Every check returns a Result. `emit` prints it as one JSON line and appends it
to .ds-checks.log in the working directory (or to $DS_CHECKS_LOG when set), so
whether a check ran can be read from the log instead of trusted from the
agent's own report. Each logged run gets an id (`mix_shift#2`: the second
mix_shift in this log) for the readout to cite, and records the query ids its
inputs came from (`from`), so a reviewer can trace a check back to its data.
"""

import json
import os
import time
from dataclasses import asdict, dataclass, field

PASS = "pass"
FLAG = "flag"
FAIL = "fail"
COULD_NOT_RUN = "could_not_run"

LOG_NAME = ".ds-checks.log"
EXIT_CODES = {PASS: 0, FLAG: 1, FAIL: 1, COULD_NOT_RUN: 2}


@dataclass
class Result:
    check: str
    status: str
    summary: str
    details: dict = field(default_factory=dict)


class SpecError(ValueError):
    """The spec is missing or malformed, so the check cannot run."""


def require(spec, key, kind):
    if key not in spec:
        raise SpecError(f"missing '{key}'")
    value = spec[key]
    if kind is int:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise SpecError(f"'{key}' must be a non-negative integer")
    elif not isinstance(value, kind):
        raise SpecError(f"'{key}' must be {kind.__name__}")
    return value


def log_path(log_dir=None):
    return os.environ.get("DS_CHECKS_LOG") or os.path.join(log_dir or os.getcwd(), LOG_NAME)


def read_log(path):
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


def emit(result, log_dir=None, sources=None):
    path = log_path(log_dir)
    runs = sum(1 for entry in read_log(path) if entry.get("check") == result.check)
    payload = {"id": f"{result.check}#{runs + 1}", "from": list(sources or []), **asdict(result)}
    print(json.dumps(payload, sort_keys=True))
    with open(path, "a") as log:
        log.write(json.dumps({"ts": round(time.time(), 3), **payload}, sort_keys=True) + "\n")
    return EXIT_CODES[result.status]
