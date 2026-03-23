# Job App Copilot

A Python CLI that helps you tailor job applications, track callbacks, and practice interviews using Claude AI.

---

## Features

- **Multi-user support** — Each user has their own profile (`users/{name}/`): resume, applications, research, callbacks
- **Tailored applications** — Paste a job description and get a tailored resume summary, bullet rewrites, and cover letter draft
- **Job fit scoring** — Automatically scores your resume against the job (Skills, Tools, Experience, Compensation) and identifies gaps
- **Application tracking** — Saves each application with company, dates, and callback status
- **Mock interviews** — Practice interview questions based on your saved applications (prioritizes Callback: Yes)
- **Callback tracking** — Mark applications when you get a callback
- **Interview calendar** — Generate .ics files for interview scheduling
- **Gap analysis** — Analyzes gaps across applications to prioritize learning
- **Company research** — Searches web for company news/culture, filters for job relevance, summarizes
- **Email output** — Option to email the output to yourself (main.py, research_company.py, mock_interview.py, create_interview_event.py)

---

## Tech Stack

- **Python 3**
- **Anthropic Claude** (claude-sonnet-4-5) — resume tailoring, scoring, mock interviews
- **python-dotenv** — environment variable management
- **pyperclip** — clipboard support for job descriptions
- **ddgs** — web search for company research (free, no API key)

---

## Installation

### Recommended: Use a virtual environment

Isolates job-app-copilot from other Python projects so `pip-audit` only reports issues in this app's dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"            # Includes pip-audit
pip-audit                          # Verify no known vulnerabilities
```

Run `pip install --upgrade pip` if pip-audit reports pip vulnerabilities.

### Running tests

```bash
pytest
```

### Option A: Install from GitHub

```bash
pip install git+https://github.com/JsonCMorgan/job-app-copilot.git
```

Works on **Windows, macOS, and Linux**. Requires Python 3.9+.

### Option B: Install from PyPI (when published)

```bash
pip install job-app-copilot
```

### Option C: Run from source (for development)

```bash
git clone https://github.com/JsonCMorgan/job-app-copilot.git
cd job-app-copilot
pip install -e .
```

Put your `.env` in the project root (or in `~/.job-app-copilot/`).

---

## Setup (after install)

1. **Add your API key** — Create a `.env` file:
   - **Installed (pip):** Put in `~/.job-app-copilot/.env` (Windows: `%USERPROFILE%\.job-app-copilot\.env`)
   - **From source:** Put in the project root or `~/.job-app-copilot/`
   - Add: `ANTHROPIC_API_KEY=your_key_here`

2. **(Optional) Email output** — Add to `.env`: `EMAIL_SENDER=your@gmail.com` and `EMAIL_APP_PASSWORD=your_app_password`  
   Gmail: create an [App Password](https://myaccount.google.com/apppasswords) (requires 2FA)

3. **Add your resume** — On first run, profiles for **jason** and **peta** are created. Select your name, then add your resume to:
   - **Installed:** `~/.job-app-copilot/users/{yourname}/resumes/master_resume.txt`
   - **From source:** `users/{yourname}/resumes/master_resume.txt` (or copy from `resumes/` when prompted)

4. **Verify setup** (optional but recommended):
   ```bash
   job-app-copilot --verify
   chmod 600 ~/.job-app-copilot/.env   # restrict .env to owner only
   ```

---

## Usage

| Feature | Command (when installed) | From source |
|---------|---------------------------|-------------|
| Main application flow | `job-app-copilot` | `python main.py` |
| Mock interview | `job-app-mock-interview` | `python mock_interview.py` |
| Mark callback | `job-app-mark-callback` | `python mark_callback.py` |
| Create calendar event | `job-app-create-event` | `python create_interview_event.py` |
| Analyze gaps | `job-app-analyze-gaps` | `python analyze_gaps.py` |
| Company research | `job-app-research` | `python research_company.py` |

You can also run `python -m job_app_copilot` for the main flow.

---

## Install Verification

After installing, verify your setup:

```bash
job-app-copilot --verify
```

Checks: `.env` presence, file permissions, API key configured (without revealing it), data directory, and profiles.

```bash
job-app-copilot --version
```

---

## Input Validation & Security

This project implements defensive coding practices relevant to IT and Cybersecurity:

- **API key validation** — Exits with clear message if `ANTHROPIC_API_KEY` is missing
- **Input sanitization** — Company names sanitized for safe filenames (path traversal prevention)
- **Date validation** — `YYYY-MM-DD` format with calendar validity checks
- **Validation loops** — Re-prompts on invalid input instead of exiting
- **Guard clauses** — Early returns for empty or invalid data
- **Path validation** — Job description file paths validated; `.env` and sensitive files blocked
- **File permissions** — `~/.job-app-copilot` and user dirs created with `0o700`; warns if `.env` is world-readable

### Secure Installation

1. **Use HTTPS** — `pip install git+https://github.com/...` (not `git://`)
2. **Restrict .env** — After creating `.env`, run `chmod 600 .env` (or `icacls .env /inheritance:r /grant:r "%USERNAME%:R"` on Windows) so only you can read it
3. **Audit dependencies** — Run `pip install pip-audit && pip-audit` after install to check for known vulnerabilities (use a venv for accurate results)
4. **Verify install** — Run `job-app-copilot --verify` to confirm setup

---

## Project Structure

```
job-app-copilot/
├── pyproject.toml          # Package config (pip install)
├── job_app_copilot/        # Main package
│   ├── main.py             # Main application flow
│   ├── mock_interview.py   # Mock interview practice
│   ├── mark_callback.py    # Mark applications as callback
│   ├── create_interview_event.py  # Generate .ics calendar files
│   ├── analyze_gaps.py     # Gap analysis
│   ├── research_company.py # Web search + Claude summary
│   ├── user_utils.py      # Multi-user profile selection
│   └── email_utils.py     # Optional email output
├── main.py, mock_interview.py, ...  # Wrappers (run from source)
├── users/                  # Per-user data (from source; installed uses ~/.job-app-copilot/users/)
└── .env                    # API key (create this, not in repo)
```

---

## License

MIT
