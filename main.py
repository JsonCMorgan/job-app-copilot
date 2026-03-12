import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)
def read_resume():
    with open("resumes/master_resume.txt", "r") as f:
        return f.read()
def call_claude(prompt):
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
def tailor_application(job_description):
    resume = read_resume()
    prompt = f"""
You are a professional job application assistant.
Your task is to tailor my resume to the job description.

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


