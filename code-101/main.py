
from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values('.env')

client = OpenAI(
    api_key=config["OPENAI_API_KEY"]
)

prompt = input("Type your prompt: ")

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
)

print(completion.choices[0].message.content)
