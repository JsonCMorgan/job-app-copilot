import anthropic
from dotenv import load_dotenv
import os
import datetime
import pyperclip
import re
from typing import Optional

from email_utils import offer_email_output
from user_utils import get_user_paths

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("Error: ANTHROPIC_API_KEY not found. Add it to your .env file.")
    exit(1)
client = anthropic.Anthropic(api_key=api_key)
def read_resume(resumes_dir: str) -> str:
    path = os.path.join(resumes_dir, "master_resume.txt")
    if not os.path.isfile(path):
        print(f"Resume not found. Add master_resume.txt to {resumes_dir}")
        exit(1)
    with open(path, "r") as f:
        return f.read()
def call_claude(prompt):
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
def tailor_application(job_description, resumes_dir: str):
    resume = read_resume(resumes_dir)
    prompt = f"""
You are a professional job application assistant.
Your task is to tailor my resume to the job description.
observe the formatting of my resume (headings, bullet style, spacing, font, font size, font colour,line spacing, indentation, paragraph structure, headlines, subheadings, body text, etc.)

Here is my resume:
{resume}

Here is the job description:
{job_description}

Please provide:
1. A tailored professional summary (3-4 sentences)
2. 5 tailored bullet point rewrites from my experience
3. A cover letter draft

Be specific and match the language of the job description.
"""
    return call_claude(prompt)
def build_header(company_name, job_posting_date, application_deadline):
    header = (
        f"Company: {company_name}\n"
        f"Job Posting Date: {job_posting_date}\n"
        f"Application Deadline: {application_deadline}\n\n"
    )
    return header
def score_fit(resume_text, job_description):
    prompt = f"""You are a professional resume scoring assistant."""
    prompt += "\n\nOUTPUT FORMAT: Return a section titled 'Job Fit Summary' with lines for Skills, Tools, Experience, and Compensation. Use 1-5 stars and include (X/5)."
    prompt += "\n\nAlso include a section titled 'Gaps' listing skills or tools the job requires that are not clearly shown on the resume. List one per line."
    prompt += f"\n\nHere is the resume:\n{resume_text}\n\nHere is the job description:\n{job_description}"
    return call_claude(prompt)
def sanitize_company_for_filename(company_name: str) -> Optional[str]:
    if not company_name or not company_name.strip():
        return None
    safe = re.sub(r'[<>:"/\\|?*.\s]', '_', company_name.strip())
    safe = re.sub(r'_+', '_', safe)
    safe = safe.strip('_')
    return safe.lower() if safe else None
def parse_date(date_str: str) -> Optional[datetime.date]:
    try:
        return datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None
def build_output_path(safe_company, today_str, outputs_dir: str):
    return os.path.join(outputs_dir, f"{safe_company}_application_{today_str}.txt")
def save_application(output_path, header, fit_summary, application_text):
    with open(output_path, "w") as f:
        f.write(header + fit_summary + "\n\n" + application_text)
def main():
    resumes_dir, outputs_dir = get_user_paths()
    resume_text = read_resume(resumes_dir)
    print("How would you like to provide the job description?")
    print("1. Paste job description into this window")
    print("2. Load job description from a text file")
    print("3. Copy job description from clipboard")
    while True:
        choice = input("Enter 1 or 2 or 3: ")
        if choice in ("1", "2", "3"):
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    while True:
        company_name = input("Enter the Company Name: ")
        safe_company = sanitize_company_for_filename(company_name)
        if not safe_company:
            print("Invalid company name. Avoid path characters (/, \\, ..) and ensure it's not empty.")
            continue
        break
    while True:
        job_posting_date = input("Enter the job posting date (YYYY-MM-DD): ")
        if job_posting_date:
            job_posting_date = parse_date(job_posting_date)
            if job_posting_date:
                break
            print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")
        else:
            print("Please enter a valid date.")
    while True:
        application_deadline = input("Enter the application deadline (YYYY-MM-DD): ")
        if application_deadline:
            application_deadline = parse_date(application_deadline)
            if application_deadline:
                break
            print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")
        else:
            print("Please enter a valid date.")

    header = build_header(company_name, job_posting_date, application_deadline)
    header = header + "Callback: No\n\n"
    
    if choice == "1":
        print("Paste the job description. Press enter on an empty line when you're done.")
        job_description = []
        while True:
            line = input()
            if line == "":
                break
            job_description.append(line)
            
        full_job_description = "\n".join(job_description)
        print("Job description loaded successfully.")
        application_text = tailor_application(full_job_description, resumes_dir)
        fit_summary = score_fit(resume_text, full_job_description)
        output_path = build_output_path(safe_company, today_str, outputs_dir)
        save_application(output_path, header, fit_summary, application_text)
        print(f"Saved to {output_path}")
        print(application_text)
        offer_email_output(header + fit_summary + "\n\n" + application_text, f"Job Application - {company_name}")
    elif choice == "2":
        print("You chose to load from a file.")
        file_path = input("Enter the path to the text file: ")
        try:
            with open(file_path, "r") as f:
                job_description_text = f.read()
        except FileNotFoundError:
            print("File not found. Please check the path and try again.")
            return 
        application_text = tailor_application(job_description_text, resumes_dir)
        fit_summary = score_fit(resume_text, job_description_text)
        output_path = build_output_path(safe_company, today_str, outputs_dir)
        save_application(output_path, header, fit_summary, application_text)
        print(f"Saved to {output_path}")
        print(application_text)
        offer_email_output(header + fit_summary + "\n\n" + application_text, f"Job Application - {company_name}")
    elif choice == "3":
        job_description_text = pyperclip.paste()
        application_text = tailor_application(job_description_text, resumes_dir)
        fit_summary = score_fit(resume_text, job_description_text)
        output_path = build_output_path(safe_company, today_str, outputs_dir)
        save_application(output_path, header, fit_summary, application_text)
        print(f"Saved to {output_path}")
        print(application_text)
        offer_email_output(header + fit_summary + "\n\n" + application_text, f"Job Application - {company_name}")
    else:
        print("Invalid choice. Please run the program again.")
    
if __name__ == "__main__":
    main()


