"""
Company Research - Search web for company/news/job-relevant info, summarize with Claude.
Uses DuckDuckGo (free, no API key) for search; Claude for filtering & summarization.
"""
import os
import re
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from ddgs import DDGS
import anthropic

from email_utils import offer_email_output
from user_utils import get_user_paths

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("Error: ANTHROPIC_API_KEY not found. Add it to your .env file.")
    exit(1)

client = anthropic.Anthropic(api_key=api_key)


def sanitize_company_for_filename(company_name: str) -> Optional[str]:
    """Safe filename from company name (reuse pattern from main.py)."""
    if not company_name or not company_name.strip():
        return None
    safe = re.sub(r'[<>:"/\\|?*.\s]', '_', company_name.strip())
    safe = re.sub(r'_+', '_', safe).strip('_')
    return safe.lower() if safe else None


def call_claude(prompt: str) -> str:
    """Send prompt to Claude, return response text."""
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def search_company(company: str, job_title: str, max_per_query: int = 15) -> str:
    """
    Run news + text searches to get company-relevant content.
    Uses DDGS.news() for articles + DDGS.text() for broader coverage.
    """
    all_snippets = []
    seen_bodies = set()

    # NEWS search - best for company announcements, earnings, leadership
    news_queries = [
        f"{company} corporation news",
        f"{company} company announcement",
        f"{company} CEO",
    ]
    ddgs = DDGS()
    for q in news_queries:
        try:
            results = ddgs.news(q, max_results=max_per_query, timelimit="m")
            for r in results:
                body = (r.get("body") or "").strip()
                title = r.get("title", "")
                url = r.get("url", "")
                if body and body not in seen_bodies:
                    seen_bodies.add(body)
                    all_snippets.append(f"[NEWS: {title}]\n{body}\nSource: {url}\n")
        except Exception as e:
            print(f"  (News search warning for '{q}': {e})")

    # TEXT search - broader, add "corporation"/"company" to reduce gaming/consumer noise
    text_queries = [
        f"{company} corporation culture",
        f"{company} company {job_title}",
        f"{company} workplace culture careers",
    ]
    for q in text_queries:
        try:
            results = ddgs.text(q, max_results=max_per_query)
            for r in results:
                body = (r.get("body") or "").strip()
                title = r.get("title", "")
                href = r.get("href", "")
                if body and body not in seen_bodies:
                    seen_bodies.add(body)
                    all_snippets.append(f"[{title}]\n{body}\nSource: {href}\n")
        except Exception as e:
            print(f"  (Search warning for '{q}': {e})")

    return "\n---\n".join(all_snippets) if all_snippets else ""


def main():
    _, outputs_dir = get_user_paths()

    while True:
        company_name = input("Company name: ").strip()
        safe_company = sanitize_company_for_filename(company_name)
        if safe_company:
            break
        print("Invalid company name. Avoid path characters (/, \\, ..) and ensure it's not empty.")

    job_title = input("Job title or role (e.g. 'Software Engineer'): ").strip()
    if not job_title:
        job_title = "position"

    print("Searching the web...")
    raw_content = search_company(company_name, job_title)

    if not raw_content:
        print("No search results found. Try different keywords or check connectivity.")
        return

    print("Filtering and summarizing with Claude...")
    prompt = f"""You are helping a job candidate prepare for an interview at {company_name} for a {job_title} role.

Below are web search results (news, articles, snippets) about the company. Your task:
1. Extract and summarize ALL information relevant to the job and interview prep: company news, culture, growth, challenges, recent developments, leadership, workplace.
2. Ignore off-topic content (e.g. product specs, gaming forums, technical support) but USE any business/company content you find.
3. ALWAYS produce a summary. Do NOT say "no useful information" or suggest alternative search terms. Work with what you have. If results are sparse, summarize what exists and note "Consider supplementing with [company] careers page or newsroom."
4. Format as:
   - Key company news/recent developments
   - Culture/values (if found)
   - Notable challenges or opportunities
   - Insights useful for the candidate

Use bullet points. Be concise. Aim for at least half a page of actionable content.

---
RAW SEARCH RESULTS:
{raw_content[:18000]}
---
Provide the filtered, summarized output:"""

    summary = call_claude(prompt)

    today_str = datetime.now().strftime("%Y-%m-%d")
    output_path = os.path.join(outputs_dir, f"{safe_company}_research_{today_str}.txt")
    header = f"Company: {company_name}\nJob/role: {job_title}\nResearch date: {today_str}\n\n"
    with open(output_path, "w") as f:
        f.write(header + summary)

    print(f"Saved to {output_path}")
    offer_email_output(header + summary, f"Company Research - {company_name}")


if __name__ == "__main__":
    main()
