"""The knowledge version: a hash of everything that shapes an explanation. Every trace and
readout records it, so a result can always be traced to the knowledge that produced it.

Knowledge = the base library and cut templates shipped with the agent, plus the knowledge
folder (by default the overlay): patterns.json, metric_families.json, cut_templates.json and
readout_rules.json, which approved lessons write to.
"""

import hashlib
import os

from search_agent import CUTS, LIBRARY

FILES = ("patterns.json", "metric_families.json", "cut_templates.json", "readout_rules.json")


def files(knowledge_dir):
    out = [LIBRARY, CUTS]
    if knowledge_dir:
        out += [os.path.join(knowledge_dir, f) for f in FILES if os.path.exists(os.path.join(knowledge_dir, f))]
    return out


def version_hash(knowledge_dir):
    h = hashlib.sha256()
    for path in files(knowledge_dir):
        h.update(os.path.basename(path).encode())
        with open(path, "rb") as handle:
            h.update(handle.read())
    return h.hexdigest()
