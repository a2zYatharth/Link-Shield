from urllib.parse import urlparse
import re
import socket
import requests

COMMON_BRANDS = ["google.com", "facebook.com", "amazon.com", "paypal.com"]

def check_domain_exists(domain):
    try:
        # DNS Resolution check
        socket.gethostbyname(domain)
        return True
    except:
        return False

def check_http_alive(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        # Try HEAD first for speed
        res = requests.head(url, timeout=5, allow_redirects=True, headers=headers)
        if res.status_code < 400: return True
        # Fallback to GET
        res = requests.get(url, timeout=5, allow_redirects=True, headers=headers)
        return res.status_code < 500
    except:
        return False

def check_heuristics(url):
    reasons = []
    score = 0
    parsed = urlparse(url)

    # Auto-fix missing scheme
    if not parsed.scheme:
        url = "https://" + url
        parsed = urlparse(url)

    domain = parsed.netloc.lower()
    
    # 🔥 CRITICAL: DNS EXISTENCE CHECK
    exists = check_domain_exists(domain)
    
    if not exists:
        reasons.append("Site does not exist: This domain cannot be resolved (DNS Failure).")
        score += 60
    else:
        if not check_http_alive(url):
            reasons.append("The website is registered but not responding (Offline).")
            score += 15

    if parsed.scheme != "https":
        reasons.append("The link is not using HTTPS.")
        score += 10

    if re.match(r"^\d+\.\d+\.\d+\.\d+$", domain):
        reasons.append("URL uses an IP address instead of a domain name.")
        score += 30

    # Brand Impersonation check
    for legit in COMMON_BRANDS:
        base = legit.split('.')[0]
        if base in domain and domain != legit:
            reasons.append(f"Impersonation Risk: Domain mimics {legit}.")
            score += 35

    return {
        "score": score,
        "reasons": reasons,
        "normalized_url": url,
        "site_exists": exists  # Pass to the final response
    }