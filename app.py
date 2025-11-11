import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Load .env (chỉ dùng khi chạy local)
load_dotenv()

# Lấy API key từ biến môi trường
api_key = os.getenv("OPENAI_API_KEY")

# Khởi tạo client OpenAI
client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI thân thiện."},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.choices[0].message.content
        return jsonify({"reply": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
