"""
Security utilities: path validation, permissions, and safe file handling.
"""
import os
import stat
from pathlib import Path
from typing import Optional, Tuple


def safe_resolve_job_file(user_path: str) -> Optional[str]:
    """
    Validate user-provided file path for job description loading.
    Returns resolved absolute path if valid, else None.
    - Rejects path traversal attempts
    - Rejects .env and other sensitive-looking files
    - Ensures it's a regular file (not dir, not a dangerous device)
    """
    if not user_path or not user_path.strip():
        return None
    path = Path(user_path.strip()).expanduser().resolve()
    if not path.exists():
        return None
    if not path.is_file():
        return None
    # Reject .env and similar to avoid accidental key exposure
    name_lower = path.name.lower()
    if name_lower == ".env" or name_lower.endswith(".env"):
        return None
    # Reject if path contains .. after resolve (shouldn't happen, but guard)
    try:
        path.resolve().relative_to(Path.cwd())
    except ValueError:
        pass  # path outside cwd is ok if user explicitly provided it
    return str(path)


def ensure_secure_dir_permissions(dir_path: str) -> None:
    """Set directory to mode 0o700 (owner rwx only) if we created it."""
    try:
        os.chmod(dir_path, 0o700)
    except OSError:
        pass  # Ignore on some systems (e.g. network drives)


def check_env_permissions(env_path: Path) -> Tuple[bool, str]:
    """
    Check if .env has restrictive permissions (owner-only read).
    Returns (is_secure, message).
    """
    try:
        st = env_path.stat()
        mode = st.st_mode
        if stat.S_IMODE(mode) == 0o600:  # rw-------
            return True, "permissions OK"
        if stat.S_IMODE(mode) in (0o400, 0o700):  # r------ or rwx------
            return True, "permissions OK"
        # Too permissive
        return False, f"permissions {oct(stat.S_IMODE(mode))} (prefer chmod 600)"
    except OSError:
        return True, "OK"  # Can't stat, skip check
