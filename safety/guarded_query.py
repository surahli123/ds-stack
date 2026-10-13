"""The reference guarded runner now lives with the skill that uses it:
skills/ds-mode/tools/guarded_query.py. This module re-exports it, so existing
imports and the self-test keep working."""

import importlib.util
import os

_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "skills", "ds-mode", "tools", "guarded_query.py")
_spec = importlib.util.spec_from_file_location("_ds_mode_guarded_query", os.path.normpath(_PATH))
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
globals().update({name: value for name, value in vars(_module).items() if not name.startswith("__")})
