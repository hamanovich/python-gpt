from openai import OpenAI
from dotenv import dotenv_values
import argparse

config = dotenv_values('.env')

client = OpenAI(api_key=config["OPENAI_API_KEY"])


def bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    return bold_start + text + bold_end


def blue(text):
    blue_start = "\033[34m"
    blue_end = "\033[0m"
    return blue_start + text + blue_end


def red(text):
    red_start = "\033[31m"
    red_end = "\033[0m"
    return red_start + text + red_end


def main():
    parser = argparse.ArgumentParser(
        description="Simple command line chatbot with GPT-3.5")

    parser.add_argument("--personality", type=str,
                        help="A brief summary of the chatbot's personality", default="friendly and helpful")

    args = parser.parse_args()

    messages = [{"role": "system", "content": f"You are a conversational chatbot. Your personality is: {
        args.personality}"}]

    while True:
        try:
            user_input = input(bold(blue("You: ")))
            messages.append({"role": "user", "content": user_input})

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            messages.append(completion.choices[0].message)

            print(bold(red("Assistant: ")),
                  completion.choices[0].message.content)

        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
