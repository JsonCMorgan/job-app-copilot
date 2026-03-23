"""Tests for email validation (no SMTP calls)."""
import pytest

from job_app_copilot.email_utils import _looks_like_email


class TestLooksLikeEmail:
    """Test basic email format validation."""

    def test_valid_emails(self):
        assert _looks_like_email("user@example.com") is True
        assert _looks_like_email("a@b.co") is True
        assert _looks_like_email(" name@domain.org ") is True

    def test_invalid_emails(self):
        assert _looks_like_email("") is False
        assert _looks_like_email("no-at-sign") is False
        assert _looks_like_email("@nodomain") is False
        assert _looks_like_email("nolocal@") is False
        assert _looks_like_email("bad@") is False
        assert _looks_like_email("a@b") is False  # no dot in domain
