"""
Streamlit Community Cloud entry point.

Deploy settings:
  Main file path: streamlit_app.py
  (Repository root — same folder as requirements.txt)

Local run:
  streamlit run streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH for `import src.*`
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# UI lives in web_ui.py; importing executes Streamlit widgets at module level.
import src.presentation.web_ui  # noqa: F401
