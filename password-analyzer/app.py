# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze_password

app = Flask(__name__)
CORS(app)  # Allows the frontend to call this API

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    password = data.get('password', '')

    if not password:
        return jsonify({"error": "No password provided"}), 400

    if len(password) > 128:
        return jsonify({"error": "Password too long"}), 400

    result = analyze_password(password)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Password Analyzer API running"})

if __name__ == '__main__':
    print("🔐 Password Analyzer API running on http://localhost:5000")
    app.run(debug=True, port=5000)
