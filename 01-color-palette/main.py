from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values('.env')

client = OpenAI(
    api_key=config["OPENAI_API_KEY"]
)

prompt = """
You are a color palette generating assistant that response to text prompts for color palettes
You should generate color palettes that fit the theme, mood or instructions in the prompt.
The palettes should be between 2 and 8 colors.

Desired Format: a JSON array of hexadecimal color codes

Text: a beatiful sunset

Result:
"""

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
