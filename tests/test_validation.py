"""Tests for input validation and sanitization."""
import datetime

import pytest

from job_app_copilot.main import build_header, parse_date, sanitize_company_for_filename


class TestSanitizeCompanyForFilename:
    """Test company name sanitization for safe filenames."""

    def test_empty_returns_none(self):
        assert sanitize_company_for_filename("") is None
        assert sanitize_company_for_filename("   ") is None

    def test_normal_name(self):
        assert sanitize_company_for_filename("Acme Corp") == "acme_corp"

    def test_strips_path_characters(self):
        assert "/" not in (sanitize_company_for_filename("Acme/Corp") or "")
        assert "\\" not in (sanitize_company_for_filename("Acme\\Corp") or "")
        assert ".." not in (sanitize_company_for_filename("Acme..Corp") or "")

    def test_collapses_underscores(self):
        result = sanitize_company_for_filename("Acme   Corp")
        assert "__" not in (result or "")

    def test_lowercase_output(self):
        assert sanitize_company_for_filename("ACME") == "acme"


class TestParseDate:
    """Test YYYY-MM-DD date parsing."""

    def test_valid_date(self):
        assert parse_date("2025-03-15") == datetime.date(2025, 3, 15)

    def test_with_whitespace(self):
        assert parse_date("  2025-03-15  ") == datetime.date(2025, 3, 15)

    def test_invalid_returns_none(self):
        assert parse_date("03-15-2025") is None
        assert parse_date("invalid") is None
        assert parse_date("2025-13-01") is None  # Invalid month


class TestBuildHeader:
    """Test application header building."""

    def test_includes_company_and_dates(self):
        d = datetime.date(2025, 3, 15)
        h = build_header("Acme", d, d)
        assert "Acme" in h
        assert "2025-03-15" in h
