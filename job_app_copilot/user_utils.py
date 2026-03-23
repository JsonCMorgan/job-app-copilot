"""
Multi-user support - each user has their own resumes/ and outputs/ under users/{name}/.
Uses project directory when running from source; ~/.job-app-copilot when installed.
"""
import os
import re
import shutil
from typing import Tuple

from job_app_copilot.secure_utils import ensure_secure_dir_permissions


def get_app_root() -> str:
    """Base directory for user data (public for verify/setup)."""
    return _get_app_root()


def _get_app_root() -> str:
    """Base directory for user data. Uses home dir when installed (site-packages)."""
    this_file = os.path.abspath(__file__)
    pkg_dir = os.path.dirname(this_file)
    parent = os.path.dirname(pkg_dir)
    # When installed, package lives in site-packages/job_app_copilot/
    if "site-packages" in parent or "dist-packages" in parent:
        return os.path.join(os.path.expanduser("~"), ".job-app-copilot")
    # Editable install or running from repo: use repo root (parent of job_app_copilot)
    return parent


def _sanitize_username(name: str) -> str:
    """Safe folder name from user input."""
    if not name or not name.strip():
        return ""
    safe = re.sub(r'[<>:"/\\|?*.\s]', '_', name.strip())
    safe = re.sub(r'_+', '_', safe).strip('_')
    return safe.lower() if safe else ""


def get_user_paths() -> Tuple[str, str]:
    """
    Prompt user to select or create profile. Returns (resumes_dir, outputs_dir).
    Creates users/{name}/resumes/ and users/{name}/outputs/.
    """
    base = get_app_root()
    users_dir = os.path.join(base, "users")
    legacy_outputs = os.path.join(base, "outputs")
    legacy_resumes = os.path.join(base, "resumes")

    # Ensure base dir exists with restrictive permissions when we create it
    if not os.path.isdir(base):
        os.makedirs(base, mode=0o700, exist_ok=True)
        ensure_secure_dir_permissions(base)

    # On first run, create default profiles: jason and peta
    if not os.path.isdir(users_dir) or not os.listdir(users_dir):
        for name in ("jason", "peta"):
            ud = os.path.join(users_dir, name)
            os.makedirs(os.path.join(ud, "resumes"), exist_ok=True)
            os.makedirs(os.path.join(ud, "outputs"), exist_ok=True)

    existing = []
    if os.path.isdir(users_dir):
        existing = [d for d in os.listdir(users_dir) if os.path.isdir(os.path.join(users_dir, d)) and not d.startswith(".")]
    existing.sort()

    if existing:
        print("\nExisting users:")
        for i, name in enumerate(existing, 1):
            print(f"  {i}. {name}")
        print(f"  Or enter a new name")
        while True:
            choice = input("\nSelect user (number) or enter new name: ").strip()
            if not choice:
                print("Please enter a number or name.")
                continue
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(existing):
                    username = existing[idx - 1]
                    break
                print("Invalid number.")
            else:
                username = _sanitize_username(choice)
                if username:
                    break
                print("Invalid name.")
    else:
        print("\nNo users yet. Enter your name to create a profile.")
        while True:
            choice = input("Your name: ").strip()
            username = _sanitize_username(choice)
            if username:
                break
            print("Invalid name. Use letters, numbers, hyphens.")

    resumes_dir = os.path.join(users_dir, username, "resumes")
    outputs_dir = os.path.join(users_dir, username, "outputs")
    os.makedirs(resumes_dir, mode=0o700, exist_ok=True)
    os.makedirs(outputs_dir, mode=0o700, exist_ok=True)
    ensure_secure_dir_permissions(resumes_dir)
    ensure_secure_dir_permissions(outputs_dir)

    # One-time migration: if user's outputs empty and legacy outputs exist, offer to copy
    if not os.listdir(outputs_dir) and os.path.isdir(legacy_outputs):
        legacy_files = [f for f in os.listdir(legacy_outputs) if not f.startswith(".")]
        if legacy_files:
            mig = input(f"Copy {len(legacy_files)} existing file(s) from outputs/ to your profile? (y/n): ").strip().lower()
            if mig in ("y", "yes"):
                for f in legacy_files:
                    shutil.copy2(os.path.join(legacy_outputs, f), os.path.join(outputs_dir, f))
                print("Copied.")

    # Copy legacy resume if user has none and legacy exists
    resume_path = os.path.join(resumes_dir, "master_resume.txt")
    if not os.path.isfile(resume_path) and os.path.isfile(os.path.join(legacy_resumes, "master_resume.txt")):
        mig = input("Copy existing resume to your profile? (y/n): ").strip().lower()
        if mig in ("y", "yes"):
            shutil.copy2(os.path.join(legacy_resumes, "master_resume.txt"), resume_path)
            print("Copied.")

    print(f"\nUsing profile: {username}\n")
    return resumes_dir, outputs_dir
