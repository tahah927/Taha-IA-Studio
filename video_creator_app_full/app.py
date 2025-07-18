from flask import Flask, render_template, request
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    generated_script = ""
    image_url = ""
    if request.method == "POST":
        topic = request.form["topic"]

        # GPT-4o: Generar guión
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Escribe un guion corto sobre: {topic}"}]
        )
        generated_script = response.choices[0].message.content.strip()

        # Unsplash: Buscar imagen
        unsplash_url = f"https://api.unsplash.com/photos/random?query={topic}&client_id={UNSPLASH_ACCESS_KEY}"
        image_response = requests.get(unsplash_url)
        if image_response.status_code == 200:
            image_url = image_response.json()["urls"]["regular"]

    return render_template("index.html", script=generated_script, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
