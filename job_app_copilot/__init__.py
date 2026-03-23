"""Job App Copilot - tailor applications, track callbacks, practice interviews."""

import os
from pathlib import Path

__version__ = "0.1.0"

# When installed, load .env from ~/.job-app-copilot so users don't need to be in a specific folder
_parent = str(Path(__file__).resolve().parents[1])
if "site-packages" in _parent or "dist-packages" in _parent:
    home_env = Path.home() / ".job-app-copilot" / ".env"
    if home_env.exists():
        from dotenv import load_dotenv
        load_dotenv(home_env)
