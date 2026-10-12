import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for sub in ("skills/ds-mode/checks", "skills/doc-tighten/tools", "skills/cold-read/tools", "skills/ds-experiment/tools",
            "eval", "safety"):
    sys.path.insert(0, os.path.join(ROOT, sub))
