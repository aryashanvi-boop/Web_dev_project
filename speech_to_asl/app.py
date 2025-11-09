# app.py
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# phrase/word map → file name in static/asl_gestures/
ASL_DICT = {
    'hello': 'hello.gif',
    'thank you': 'thank you.gif',
    'yes': 'yes.gif',
    'no': 'no.gif',
    'please': 'please.gif'
}

@app.route("/")
def home():
    return render_template("index.html")

def translate_text_to_gestures(text: str):
    text = (text or "").lower().strip()
    tokens = text.split()
    gestures = []

    # greedy phrase matching first (e.g., "thank you")
    phrase_keys = sorted(ASL_DICT.keys(), key=lambda k: len(k.split()), reverse=True)
    i = 0
    while i < len(tokens):
        matched = False
        for k in phrase_keys:
            klen = len(k.split())
            if i + klen <= len(tokens):
                cand = " ".join(tokens[i:i+klen])
                if cand == k:
                    gestures.append(ASL_DICT[k])
                    i += klen
                    matched = True
                    break
        if matched:
            continue

        # fallback: fingerspell letters for this token
        for ch in tokens[i]:
            if ch.isalpha():
                gestures.append(f"{ch.lower()}.gif")
        i += 1
    return gestures

@app.post("/translate")
def translate():
    try:
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()
        gestures = translate_text_to_gestures(text)
        return jsonify({"gestures": gestures}), 200
    except Exception as e:
        # print full error to server console and return 500 JSON
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    os.makedirs(os.path.join("static", "asl_gestures"), exist_ok=True)
    # Run on a free port so macOS AirPlay doesn’t clash
    app.run(debug=True, host="127.0.0.1", port=5051)
