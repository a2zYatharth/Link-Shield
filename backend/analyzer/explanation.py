def generate_explanation(data):
    # Base heuristic data
    score = data.get("score", 0)
    reasons = data.get("reasons", [])
    detailed_sources = []
    
    # 🔹 WHOIS Analysis
    whois_info = data.get("whois", {})
    if whois_info.get("registered"):
        age = whois_info.get("age_days", 999)
        if age < 30:
            score += 40
            reasons.append(f"⚠️ New Domain: Registered only {age} days ago.")
    
    # 🔹 Reputation Engines
    engines = [
        ("Google", data.get("google", {}).get("malicious", False), 50),
        ("urlscan.io", data.get("urlscan", {}).get("malicious", False), 60),
        ("URLHaus", data.get("urlhaus", {}).get("status") == "ok", 60),
        ("VirusTotal", data.get("virustotal", {}).get("malicious", 0) > 0, 15)
    ]

    for name, flagged, penalty in engines:
        detailed_sources.append({"name": name, "flagged": flagged})
        if flagged:
            # VT uses a multiplier, others use flat penalty
            score += penalty if name != "VirusTotal" else (data["virustotal"]["malicious"] * penalty)

    # Logic Finalization
    score = min(score, 100)
    status = "dangerous" if score >= 60 else "suspicious" if score >= 25 else "safe"
    if not reasons: reasons = ["No major threats detected."]

    return {
        "status": status,
        "risk_score": score,
        "reasons": reasons,
        "sources": detailed_sources,
        "site_exists": data.get("site_exists", True), # The 'Circuit Breaker' flag
        "screenshot": data.get("urlscan", {}).get("screenshot"),
        "raw_data": data 
    }