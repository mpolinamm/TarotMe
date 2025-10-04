from flask import Flask, render_template, jsonify, session
import random, json, requests

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Load tarot data
with open("data/tarot_cards.json", "r", encoding="utf-8") as f:
    tarot_cards = json.load(f)

def draw_three_cards():
    cards = random.sample(tarot_cards, 3)
    for c in cards:
        c["reversed"] = random.choice([True, False])
    return cards

def generate_ai_reading(cards):
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
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=60
        )
        if resp.status_code == 200:
            return resp.json().get("response", "").strip()
        return f"Ollama error {resp.status_code}"
    except Exception as e:
        return f"Ollama not reachable: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/draw", methods=["GET"])
def api_draw():
    cards = draw_three_cards()
    ai_reading = generate_ai_reading(cards)
    return jsonify({"cards": cards, "reading": ai_reading})

if __name__ == "__main__":
    app.run(debug=True)
