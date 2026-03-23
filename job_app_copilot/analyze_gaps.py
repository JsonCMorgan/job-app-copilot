import os
from dotenv import load_dotenv
import anthropic

from job_app_copilot.user_utils import get_user_paths

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("Error: ANTHROPIC_API_KEY not found. Add it to your .env file.")
    exit(1)
client = anthropic.Anthropic(api_key=api_key)


def main():
    _, outputs_dir = get_user_paths()
    output_files = [f for f in os.listdir(outputs_dir) if f.endswith(".txt")]

    all_gaps = []
    for filename in output_files:
        path = os.path.join(outputs_dir, filename)
        with open(path, "r") as f:
            content = f.read()
        if "Gaps" in content:
            start = content.find("Gaps")
            end = content.find("# 1. TAILORED", start)
            if end == -1:
                end = len(content)
            gap_block = content[start:end].strip()
            all_gaps.append(gap_block.replace("\n", " "))
        else:
            print(f"No Gaps section found in {filename}")

    if not all_gaps:
        print("No Gaps sections found in any files.")
        return

    combined_gaps = "\n\n---\n\n".join(all_gaps)
    prompt = "Below are the Gaps sections from multiple job applications. Which gaps appear most often? Rank them for prioritized learning.\n\n" + combined_gaps
    message = client.messages.create(model="claude-sonnet-4-5", max_tokens=1024, messages=[{"role": "user", "content": prompt}])
    print(message.content[0].text)
