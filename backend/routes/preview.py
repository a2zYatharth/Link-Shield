# backend/app.py or routes/preview.py
import requests
from flask import request, jsonify

@app.route('/preview-url', methods=['POST'])
def preview_url():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        # Follow redirects but don't download the whole page (HEAD request)
        response = requests.head(url, allow_redirects=True, timeout=3)
        return jsonify({
            "redirect_to": response.url,
            "is_redirect": response.url != url
        })
    except:
        return jsonify({"redirect_to": url, "is_redirect": False})