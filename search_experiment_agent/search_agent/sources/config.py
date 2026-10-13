"""Experiment configs, in one canonical shape.

Canonical config (what the rest of the agent reads):
    {"id": uuid, "name": display name, "experiment_name": the T1 key, "layer", "tags": [],
     "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" or None, "target_days": int or None,
     "control_group": group id, "hypothesis": text,
     "groups": [{"id", "name", "size", "parameters": {}}],
     "health_checks": [{"name", "status": "PASSED" | "WARNING" | "FAILED"}]}

- JsonDirConfig reads canonical files (the synthetic warehouse writes them).
- CliConfig is the work config CLI. It runs only outside the sandbox; write `to_canonical`
  at work from its JSON, with a test on one sanitized example.
"""

import json
import os
import re


def _norm(text):
    return re.sub(r"[^a-z0-9]", "", str(text).lower())


class JsonDirConfig:
    command = "a canonical config file in the configs folder"

    def __init__(self, folder):
        self.folder = folder
        self.by_id = {}
        if folder and os.path.isdir(folder):
            for name in os.listdir(folder):
                if name.endswith(".json"):
                    with open(os.path.join(folder, name), encoding="utf-8") as handle:
                        cfg = json.load(handle)
                    self.by_id[cfg["id"]] = cfg

    def get(self, config_id):
        return self.by_id.get(config_id)

    def find(self, name):
        hits = [c for c in self.by_id.values() if _norm(c.get("experiment_name")) == _norm(name)
                or _norm(c.get("name")) == _norm(name)]
        return hits


class CliConfig:
    """The work config CLI. Finish at work: run it outside the sandbox and map its JSON."""

    command = "the config CLI's details command, run outside the sandbox"

    def __init__(self, run):
        self.run = run

    def get(self, config_id):
        raise NotImplementedError("CliConfig.get: call the config CLI and return to_canonical(json)")

    def find(self, name):
        return []


def for_decide(cfg, split=None):
    """Canonical config -> ds-experiment's config shape (checks.py and decide.py read it).

    `split` is {group name: count of all exposed units} when the overlay names that count."""
    if not cfg:
        return None
    groups = [{"id": g.get("id"), "name": g.get("name"), "size_pct": g.get("size"),
               "parameters": g.get("parameters") or {}, "disabled": bool(g.get("disabled"))} for g in cfg.get("groups", [])]
    return {"experiment_id": cfg.get("id"), "name": cfg.get("name"), "hypothesis": cfg.get("hypothesis"),
            "groups": groups, "control_group": cfg.get("control_group"), "start": cfg.get("start"), "end": cfg.get("end"),
            "target_days": cfg.get("target_days"), "status": cfg.get("status"), "layer_id": cfg.get("layer"),
            "health_checks": [{"type": "sample_split" if "balanced" in str(h.get("name", "")).lower() else h.get("name"),
                               "name": h.get("name"), "status": h.get("status"), "metadata": {}}
                              for h in cfg.get("health_checks", [])],
            "settings": {}, "edits": [], "exposures": split or {}}
