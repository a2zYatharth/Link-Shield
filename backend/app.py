import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer.url_checker import analyze_url
from services.db_service import init_db

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/preview-url", methods=["POST"])
def preview_url():
    url = request.json.get("url", "")
    if not url.startswith(("http://", "https://")): url = "https://" + url
    try:
        res = requests.get(url, allow_redirects=True, timeout=3, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
        return jsonify({"redirect_to": res.url})
    except: return jsonify({"redirect_to": url})

@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.json.get("url")
    return jsonify(analyze_url(url))

if __name__ == "__main__":
    app.run(debug=True)