from analyzer.heuristics import check_heuristics
from analyzer.explanation import generate_explanation
from analyzer.reputation import (
    check_google_safe, 
    check_virustotal, 
    check_urlhaus, 
    check_whois, 
    check_urlscan
)

def analyze_url(url):
    # 1. Internal Heuristics (HTTPS, Keywords, IPs)
    heuristics = check_heuristics(url)

    # 2. External Reputation & Intel
    google = check_google_safe(url)
    whois_data = check_whois(url)
    urlscan_data = check_urlscan(url)
    vt_data = check_virustotal(url)
    urlhaus_data = check_urlhaus(url)

    # 3. Bundle for the Explainer
    combined = {
        **heuristics,
        "google": google,
        "virustotal": vt_data,
        "urlhaus": urlhaus_data,
        "whois": whois_data,
        "urlscan": urlscan_data
    }

    # 4. Generate final scoring and human-readable reasons
    return generate_explanation(combined)