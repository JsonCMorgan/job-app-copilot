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
def main():
    print("How would you like to provide the job description?")
    print("1. Paste job description into this window")
    print("2. Load job description from a text file")
    choice = input("Enter 1 or 2: ")
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
        print(tailor_application(full_job_description))
    elif choice == "2":
        print("You chose to load from a file.")
        file_path = input("Enter the path to the text file: ")
        try:
            with open(file_path, "r") as f:
                job_description_text = f.read()
        except FileNotFoundError:
            print("File not found. Please check the path and try again.")
            return 
        print("Job description loaded successfully from file.")
        print(tailor_application(job_description_text))       
    else:
        print("Invalid choice. Please run the program again.")
    
if __name__ == "__main__":
    main()


