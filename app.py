import requests

def generate_ai_reading(cards):
    """Generate tarot interpretation using local Ollama model."""
    summary = ", ".join(
        [f"{c['name']} ({'reversed' if c['reversed'] else 'upright'})" for c in cards]
    )

    prompt = f"""
    You are a mystical tarot reader.
    Give a poetic, insightful interpretation for these three cards (past, present, future):
    {summary}.
    Write in one short paragraph.
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
            return f"Error: Ollama returned status {response.status_code}"
    except Exception as e:
        return f"(Local AI unavailable) {e}"
