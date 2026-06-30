
from flask import Flask, render_template, request, jsonify
from chatbot_logic import get_response

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    message = data.get("message", "")
    user_name = data.get("user_name")

    if not message.strip():
        return jsonify({"reply": "Please type something!", "user_name": user_name})

    reply, user_name = get_response(message, user_name)
    return jsonify({"reply": reply, "user_name": user_name})


if __name__ == "__main__":
    app.run(debug=True)
