"""
Multi-user support - each user has their own resumes/ and outputs/ under users/{name}/.
"""
import os
import re
import shutil
from typing import Tuple


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
    base = os.path.dirname(os.path.abspath(__file__))
    users_dir = os.path.join(base, "users")
    legacy_outputs = os.path.join(base, "outputs")
    legacy_resumes = os.path.join(base, "resumes")

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
    os.makedirs(resumes_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

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
