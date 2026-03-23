"""CLI smoke tests - --version and --verify (no user input)."""
import subprocess
import sys


def test_cli_version():
    """job-app-copilot --version exits 0 and prints version."""
    result = subprocess.run(
        [sys.executable, "-m", "job_app_copilot", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout
    assert "job-app-copilot" in result.stdout.lower()


def test_cli_verify():
    """job-app-copilot --verify exits 0 (may or may not have .env)."""
    result = subprocess.run(
        [sys.executable, "-m", "job_app_copilot", "--verify"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Verifying" in result.stdout or "Job App Copilot" in result.stdout
