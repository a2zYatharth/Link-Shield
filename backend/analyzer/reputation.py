import requests
import whois
from datetime import datetime
from urllib.parse import urlparse

# 🔑 Replace with your actual keys
GOOGLE_API_KEY = "PASTE HERE"
VT_API_KEY = "VIRUSTOTAL API KEY "

def check_google_safe(url):
    try:
        endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"
        body = {
            "client": {"clientId": "linkshield", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        res = requests.post(endpoint, json=body, timeout=5)
        return {"malicious": "matches" in res.json()}
    except: return {"malicious": False}

def check_virustotal(url):
    try:
        headers = {"x-apikey": VT_API_KEY}
        res = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": url}, timeout=5)
        analysis_id = res.json()["data"]["id"]
        report = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_id}", headers=headers, timeout=5).json()
        return report["data"]["attributes"]["stats"]
    except: return {}

def check_urlhaus(url):
    try:
        res = requests.post("https://urlhaus-api.abuse.ch/v1/url/", data={"url": url}, timeout=8)
        return {"status": res.json().get("query_status"), "threat": res.json().get("threat")}
    except: return {}

def check_whois(url):
    try:
        domain = urlparse(url).netloc or url
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list): creation_date = creation_date[0]
        if creation_date:
            return {"registered": True, "age_days": (datetime.now() - creation_date).days}
        return {"registered": False}
    except: return {"registered": False}

def check_urlscan(url):
    try:
        res = requests.get(f"https://urlscan.io/api/v1/search/?q=url:\"{url}\"", timeout=5)
        results = res.json().get("results", [])
        if results:
            return {
                "found": True, 
                "screenshot": results[0].get("screenshot"),
                "malicious": results[0].get("verdicts", {}).get("overall", {}).get("malicious", False)
            }
        return {"found": False}
    except: return {"found": False}