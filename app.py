from flask import Flask, render_template, redirect, url_for, session
import random, json, requests

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Change to anything you like

# Load tarot card data
with open("data/tarot_cards.json", "r", encoding="utf-8") as f:
    tarot_cards = json.load(f)

def draw_three_cards():
    """Randomly select 3 tarot cards (can be upright or reversed)."""
    cards = random.sample(tarot_cards, 3)
    for card in cards:
        card["reversed"] = random.choice([True, False])
    return cards

def generate_ai_reading(cards):
    """Ask the local Ollama LLM for a tarot interpretation."""
    summary = ", ".join(
        [f"{c['name']} ({'reversed' if c['reversed'] else 'upright'})" for c in cards]
    )

    prompt = f"""
    You are a mystical tarot reader.
    Provide a poetic, insightful interpretation for these three tarot cards:
    {summary}.
    Explain them as past, present, and future in one short paragraph.
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "").strip()
        else:
            return f"Error: Ollama returned status code {response.status_code}."
    except Exception as e:
        return f"Ollama not reachable. Make sure it's running with 'ollama serve'. Error: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/draw")
def draw_cards():
    cards = draw_three_cards()
    session["cards"] = cards
    return redirect(url_for("reading"))

@app.route("/reading")
def reading():
    cards = session.get("cards", [])
    if not cards:
        return redirect(url_for("index"))
    ai_reading = generate_ai_reading(cards)
    return render_template("reading.html", cards=cards, ai_reading=ai_reading)

if __name__ == "__main__":
    app.run(debug=True)
