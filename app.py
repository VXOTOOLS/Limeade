from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# 🔑 Mets ta clé Gemini ici (ou variable d'environnement Render)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# mémoire simple (conversation)
chat_history = []

# stock action pour Roblox
last_action = {}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global chat_history, last_action

    user_message = request.json.get("message")

    # ajouter à l'historique
    chat_history.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    # appel Gemini
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
        json={
            "contents": chat_history
        }
    )

    data = response.json()

    ai_reply = data["candidates"][0]["content"]["parts"][0]["text"]

    # ajouter réponse IA
    chat_history.append({
        "role": "model",
        "parts": [{"text": ai_reply}]
    })

    # 🔥 détection action Roblox
    if "house" in ai_reply.lower():
        last_action = {"type": "build_house"}

    return jsonify({
        "reply": ai_reply
    })


@app.route("/action", methods=["GET"])
def action():
    return jsonify(last_action)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
