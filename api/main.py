

from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask, request, jsonify
from agents.faq_agent import faq_agent
import asyncio

app = Flask(__name__)

@app.route("/faq", methods=["POST"])
def handle_faq():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    result = asyncio.run(faq_agent.run(question))

    return jsonify({
        "question": result.output.question,
        "answer": result.output.answer,
        "score": result.output.score,
        "source": result.output.source,
        "tokens": result.usage().__dict__
    })

@app.route("/")
def root():
    return "FAQ Agent is running"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
