# Security

## Reporting vulnerabilities

If you discover a security vulnerability, please report it responsibly. You can:

1. **Open a private security advisory** on GitHub: go to the repo → Security → Advisories → New draft
2. Or contact the maintainer directly

Please do not open public issues for security vulnerabilities.

## Security practices in this project

- API keys and secrets stored in `.env` only; never logged or printed
- `.env` file permissions checked and restrictive modes recommended
- User data directories created with owner-only permissions (0o700)
- Input validation: company names sanitized, file paths validated, sensitive paths (e.g. `.env`) blocked
- Dependencies pinned to minimum versions; run `pip audit` after install
