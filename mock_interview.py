import anthropic
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

def call_claude(prompt):
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text 
outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
output_files = [f for f in os.listdir(outputs_dir) if f.endswith(".txt")]
if not output_files:
    print("No application files found in outputs/.")
    exit()
callback_files = []
other_files = []
for filename in output_files:
    path = os.path.join(outputs_dir, filename)
    with open(path, "r") as f:
        content = f.read(2000)
    if "Callback: Yes" in content:
        callback_files.append(filename)
    else: 
        other_files.append(filename)
display_list = callback_files + other_files
for i, filename in enumerate(display_list, 1):
    print(f"{i}. {filename}")
choice = input("Enter the number of the application to mock interview: ")
index = int(choice) - 1
chosen_filename = display_list[index]
path = os.path.join(outputs_dir, chosen_filename)
with open(path, "r") as f:
    application_content = f.read()
num_questions = int(input("How many mock interview questions? "))
for question_num in range(1, num_questions + 1):
    prompt = f"""You are an interviewer for the role in this application. Based on the application below (company, job fit, gaps, tailored summary), ask the candidate one interview question (Question {question_num} of {num_questions}). Be specific to the role. Output only the question, nothing else.

Application:
{application_content}
"""
    question = call_claude(prompt)
    print(f"\nQuestion {question_num} of {num_questions}:")
    print(question)
    answer = input("Type your answer (or 'done' to stop): ")
    if answer.strip().lower() == "done":
        break
    feedback_prompt = f"""You are a hiring manager interviewing for this role. Using the application context below, evaluate the candidate's answer to the interview question. Provide:

1) What was strong (1-2 bullets)
2) What to improve (1-2 bullets)
3) A better version of the answer (3-6 sentences)

Application:
{application_content}

Question:
{question}

Answer:
{answer}
"""
    feedback = call_claude(feedback_prompt)
    print("\nFeedback:")
    print(feedback)
