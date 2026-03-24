import { useState, useEffect } from "react";
import { analyzeLink } from "../services/api";

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loadingPreview, setLoadingPreview] = useState(false);

  // --- REDIRECT PREVIEW ---
  useEffect(() => {
    const delayDebounceFn = setTimeout(async () => {
      const shorteners = ["bit.ly", "tinyurl", "t.co", "goo.gl", "bitly.com"];
      if (url.length > 5 && shorteners.some(s => url.includes(s))) {
        setLoadingPreview(true);
        try {
          const res = await fetch("http://localhost:5000/preview-url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url }),
          });
          const data = await res.json();
          if (data.redirect_to && data.redirect_to !== url) setPreviewUrl(data.redirect_to);
        } catch (err) { console.error(err); } 
        finally { setLoadingPreview(false); }
      } else { setPreviewUrl(null); }
    }, 600);
    return () => clearTimeout(delayDebounceFn);
  }, [url]);

  // --- MAIN ANALYZE FUNCTION ---
  const handleAnalyze = async () => {
    if (!url) return;
    setResult(null);
    setShowDetails(false);
    setLoading(true);
    
    try {
      const res = await analyzeLink(url);
      
      // 🔥 SITE EXISTENCE POPUP WARNING
      if (res.site_exists === false) {
        alert("⚠️ SITE NOT FOUND\nThis domain does not exist or cannot be resolved. Please check the spelling or the link status.");
        setLoading(false);
        return; // Break the execution
      }

      setResult(res);
    } catch (err) { 
      alert("Analysis failed. Check if Backend is running."); 
    } finally { 
      setLoading(false); 
    }
  };

  const getStatusColor = (status) => {
    if (status === "dangerous") return "#ef4444";
    if (status === "suspicious") return "#f59e0b";
    return "#10b981";
  };

  return (
    <div style={{ padding: "40px", maxWidth: "700px", margin: "0 auto", fontFamily: "Inter, sans-serif" }}>
      <h1 style={{ textAlign: "center", marginBottom: "30px" }}>🛡️ LinkShield Pro</h1>

      <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
        <input
          type="text"
          placeholder="Paste link to scan (e.g. bit.ly/xyz)..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ flex: 1, padding: "15px", borderRadius: "10px", border: "2px solid #e2e8f0", outline: "none" }}
        />
        <button onClick={handleAnalyze} disabled={loading} style={{ padding: "0 30px", borderRadius: "10px", background: "#000", color: "#fff", cursor: "pointer", fontWeight: "bold" }}>
          {loading ? "Scanning..." : "Analyze"}
        </button>
      </div>

      {loadingPreview && <p style={{ fontSize: "12px", color: "#718096" }}>🔍 Checking for redirects...</p>}
      {previewUrl && (
        <div style={{ padding: "12px", background: "#fffbeb", border: "1px solid #fef3c7", borderRadius: "8px", marginBottom: "20px" }}>
          <small style={{ color: "#92400e", fontWeight: "bold" }}>UNMASKED DESTINATION:</small>
          <div style={{ wordBreak: "break-all", fontSize: "14px", color: "#b45309" }}>{previewUrl}</div>
        </div>
      )}

      {result && (
        <div style={{ marginTop: "30px", borderTop: "1px solid #eee", paddingTop: "20px" }}>
          <div style={{ marginBottom: "25px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
              <span style={{ fontWeight: "700" }}>Security Trust Score</span>
              <span style={{ fontWeight: "700", color: getStatusColor(result.status) }}>{Math.max(0, 100 - result.risk_score)}%</span>
            </div>
            <div style={{ width: "100%", height: "12px", background: "#edf2f7", borderRadius: "10px", overflow: "hidden" }}>
              <div style={{ width: `${Math.max(0, 100 - result.risk_score)}%`, height: "100%", background: getStatusColor(result.status), transition: "width 1s ease" }} />
            </div>
          </div>

          <h2 style={{ color: getStatusColor(result.status), margin: "10px 0" }}>{result.status.toUpperCase()}</h2>

          <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "20px" }}>
            {result.sources?.map((src, i) => (
              <span key={i} style={{ fontSize: "12px", padding: "5px 12px", borderRadius: "20px", background: src.flagged ? "#fee2e2" : "#d1fae5", color: src.flagged ? "#991b1b" : "#065f46", border: "1px solid" }}>
                {src.name} {src.flagged ? "🚩" : "✅"}
              </span>
            ))}
          </div>

          <div style={{ background: "#f8fafc", padding: "15px", borderRadius: "10px", marginBottom: "20px" }}>
            <h4 style={{ margin: "0 0 10px 0" }}>Intelligence Findings:</h4>
            <ul style={{ paddingLeft: "20px", fontSize: "14px", color: "#4a5568" }}>
              {result.reasons?.map((r, i) => <li key={i} style={{ marginBottom: "5px" }}>{r}</li>)}
            </ul>
          </div>

          {result.screenshot && (
            <div style={{ marginBottom: "20px" }}>
              <h4 style={{ margin: "0 0 10px 0" }}>Visual Evidence (Remote Screenshot):</h4>
              <img src={result.screenshot} alt="Site Screenshot" style={{ width: "100%", borderRadius: "12px", border: "1px solid #ddd", boxShadow: "0 4px 12px rgba(0,0,0,0.1)" }} />
            </div>
          )}

          <button onClick={() => setShowDetails(!showDetails)} style={{ background: "none", border: "none", color: "#4f46e5", cursor: "pointer", fontSize: "14px", fontWeight: "600" }}>
            {showDetails ? "▼ Hide Technical Audit" : "▶ Show Raw Security Data"}
          </button>
          {showDetails && (
            <pre style={{ marginTop: "10px", padding: "15px", background: "#1e293b", color: "#38bdf8", borderRadius: "10px", fontSize: "11px", overflowX: "auto" }}>
              {JSON.stringify(result.raw_data || result, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}