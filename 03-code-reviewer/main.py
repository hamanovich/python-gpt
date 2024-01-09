import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

PROMPT = """
You will receive a file's contents as text.
Generate a code review for the file.  
Indicate what changes should be made to improve its style, performance, readability, and maintainability.
If there are any reputable libraries that could be introduced to improve the code, suggest them.  
Be kind and constructive.
For each suggested change, include line numbers to which you are referring
"""


def code_review(file_path, model):
    with open(file_path, "r") as file:
        content = file.read()
    with open("code_review.txt", "w") as file:
        file.write(make_code_review_request(content, model))


def make_code_review_request(file_content, model):
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": f"Code review the following file: {file_content}"}
    ]
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages
        )

        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(
        description="Simple code reviewer for a file")
    parser.add_argument("file")
    parser.add_argument("--model", default="gpt-3.5-turbo")
    try:
        args = parser.parse_args()
        code_review(args.file, args.model)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    main()
