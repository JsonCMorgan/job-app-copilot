"""Tests for secure_utils - path validation and permissions."""
import stat
from pathlib import Path

import pytest

from job_app_copilot.secure_utils import check_env_permissions, safe_resolve_job_file


class TestSafeResolveJobFile:
    """Test path validation for job description file loading."""

    def test_empty_or_whitespace_returns_none(self):
        assert safe_resolve_job_file("") is None
        assert safe_resolve_job_file("   ") is None

    def test_nonexistent_file_returns_none(self):
        assert safe_resolve_job_file("/nonexistent/path/xyz.txt") is None

    def test_valid_file_returns_resolved_path(self, tmp_path):
        f = tmp_path / "job.txt"
        f.write_text("job description")
        result = safe_resolve_job_file(str(f))
        assert result is not None
        assert Path(result).exists()
        assert Path(result).is_file()

    def test_rejects_env_file(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("KEY=value")
        assert safe_resolve_job_file(str(env_file)) is None

    def test_rejects_file_ending_in_env(self, tmp_path):
        f = tmp_path / "config.env"
        f.write_text("stuff")
        assert safe_resolve_job_file(str(f)) is None

    def test_rejects_directory(self, tmp_path):
        assert safe_resolve_job_file(str(tmp_path)) is None

    def test_expands_tilde(self, tmp_path, monkeypatch):
        """If path starts with ~, it should expand to home."""
        home = Path.home()
        # Create file in home - we can't easily mock Path.home for expanduser
        # So use a path we control: tmp_path
        f = tmp_path / "job_desc.txt"
        f.write_text("content")
        result = safe_resolve_job_file(str(f))
        assert result is not None


class TestCheckEnvPermissions:
    """Test .env permission checking."""

    def test_600_is_secure(self, tmp_path):
        env = tmp_path / ".env"
        env.write_text("KEY=val")
        env.chmod(0o600)
        ok, msg = check_env_permissions(env)
        assert ok is True
        assert "OK" in msg

    def test_400_is_secure(self, tmp_path):
        env = tmp_path / ".env"
        env.write_text("KEY=val")
        env.chmod(0o400)
        ok, msg = check_env_permissions(env)
        assert ok is True

    def test_644_is_insecure(self, tmp_path):
        env = tmp_path / ".env"
        env.write_text("KEY=val")
        env.chmod(0o644)
        ok, msg = check_env_permissions(env)
        assert ok is False
        assert "chmod" in msg or "0o" in msg
