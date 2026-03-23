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

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/JsonCMorgan/job-app-copilot.git
   cd job-app-copilot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API key**
   - Create a `.env` file in the project root
   - Add: `ANTHROPIC_API_KEY=your_key_here`
   - Get a key at [console.anthropic.com](https://console.anthropic.com)

4. **(Optional) Email output** — At the end of runs, you can optionally email the output to yourself:
   - Add to `.env`: `EMAIL_SENDER=your@gmail.com` and `EMAIL_APP_PASSWORD=your_app_password`
   - Gmail: create an [App Password](https://myaccount.google.com/apppasswords) (requires 2FA)

4. **Add your resume**
   - On first run, profiles for **jason** and **peta** are created
   - Select your name, then add `users/{yourname}/resumes/master_resume.txt` with your resume
   - (Or copy from `resumes/master_resume.txt` when prompted)

---

## Usage

| Script | Command | Description |
|--------|---------|-------------|
| Main application flow | `python main.py` | Tailor an application from job description (paste, file, or clipboard) |
| Mock interview | `python mock_interview.py` | Practice interview questions for a chosen application |
| Mark callback | `python mark_callback.py` | Mark an application as "Callback: Yes" |
| Create calendar event | `python create_interview_event.py` | Generate .ics file for an interview |
| Analyze gaps | `python analyze_gaps.py` | See which gaps appear most across applications |
| Company research | `python research_company.py` | Search web for company info, summarize for interview prep |

---

## Input Validation & Security

This project implements defensive coding practices relevant to IT and Cybersecurity:

- **API key validation** — Exits with clear message if `ANTHROPIC_API_KEY` is missing
- **Input sanitization** — Company names sanitized for safe filenames (path traversal prevention)
- **Date validation** — `YYYY-MM-DD` format with calendar validity checks
- **Validation loops** — Re-prompts on invalid input instead of exiting
- **Guard clauses** — Early returns for empty or invalid data

---

## Project Structure

```
job-app-copilot/
├── main.py                 # Main application flow
├── mock_interview.py       # Mock interview practice
├── mark_callback.py        # Mark applications as callback
├── create_interview_event.py  # Generate .ics calendar files
├── analyze_gaps.py         # Gap analysis across applications
├── research_company.py      # Web search + Claude summary for company research
├── user_utils.py           # Multi-user profile selection
├── email_utils.py          # Optional email output
├── users/                  # Per-user data (not in repo)
│   └── {name}/
│       ├── resumes/
│       │   └── master_resume.txt
│       └── outputs/        # Applications, research, .ics files
├── resumes/                # Legacy (migrate to users/{name}/)
├── outputs/                # Legacy (migrate to users/{name}/)
└── .env                    # API key (create this, not in repo)
```

---

## License

MIT
