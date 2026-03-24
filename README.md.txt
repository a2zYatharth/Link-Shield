							🛡️ LinkShield Pro


LinkShield Pro is a full-stack cybersecurity tool designed to deconstruct and analyze suspicious links before you click them. It provides a multi-layered defense by combining real-time redirect unmasking, domain reputation scoring, and automated "site existence" verification.

🚀 Key Features
Real-time Unmasking: Detects and follows redirects for short-links (bit.ly, tinyurl) as you type.

Multi-Engine Analysis: Aggregates data from Google Safe Browsing, VirusTotal, and URLHaus.

WHOIS Insight: Identifies "Zero-Day" phishing by flagging domains registered within the last 30 days.

Visual Evidence: Displays automated screenshots via urlscan.io to view sites safely.

Existence Check: Instant DNS resolution to verify if a site actually exists before running deep scans.

🛠️ Setup & Activation
Follow these steps to get the tool running on your local machine.

1. Clone the Repository
Bash
git clone https://github.com/yourusername/linkshield-pro.git
cd linkshield-pro
2. Backend Setup (Python/Flask)
Navigate to the backend folder:

Bash
cd backend
Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
Install dependencies:

Bash
pip install flask flask-cors requests python-whois
Run the server:

Bash
python app.py
The backend will start on http://127.0.0.1:5000.

3. Frontend Setup (React)
Open a new terminal and navigate to the frontend folder:

Bash
cd frontend
Install the packages:

Bash
npm install
Start the application:

Bash
npm start
The tool will open in your browser at http://localhost:3000.

🔑 Configuration
Open backend/analyzer/reputation.py and insert your API keys to enable full scanning:

Google Safe Browsing API

VirusTotal API

🧠 How it Works
The tool calculates a Risk Score based on several weighted factors:

DNS Lookup: Immediate check if the domain is registered.

Age Factor: Newer domains (less than 30 days) receive a high-risk penalty.

Reputation: Cross-referencing 5+ global security databases.

Heuristics: Checking for HTTPS, IP-based URLs, and brand impersonation