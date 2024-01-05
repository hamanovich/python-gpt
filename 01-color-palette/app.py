from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import dotenv_values
import json

config = dotenv_values('.env')

client = OpenAI(api_key=config["OPENAI_API_KEY"])


def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that response to text prompts for color palettes.
    You should generate color palettes that fit the theme, mood or instructions in the prompt.
    The palettes should be between 2 and 8 colors.

    Desired Format: a JSON array of hexadecimal color codes

    Text: {msg}
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

    return json.loads(completion.choices[0].message.content)


app = Flask(
    __name__,
    template_folder="templates",
    static_url_path="",
    static_folder="static")


@app.route("/palette", methods=["POST"])
def prompt_palette():
    query = request.form.get("query")
    return {"colors": get_colors(query)}


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
