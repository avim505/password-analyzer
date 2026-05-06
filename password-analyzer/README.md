# 🔐 Password Strength Analyzer & Brute-Force Simulator

A cybersecurity tool that analyzes password strength using real entropy mathematics, estimates crack times across multiple attack vectors, detects common weakness patterns, and simulates brute-force attacks. Built with Python and vanilla JavaScript — no frameworks, no fluff.

---

## 🖥️ Live Demo

Open `index.html` directly in any browser. No installation required for the frontend.

---

## 📸 Features

- **Shannon Entropy Calculation** — mathematically measures how unpredictable a password is based on character pool size and length
- **Crack Time Estimation** — estimates time to crack across 4 real-world attack scenarios
- **Pattern Detection** — identifies 7 common weakness patterns attackers exploit
- **Brute-Force Simulation** — simulates actual brute-force attempts on short passwords; projects combination counts for longer ones
- **Character Analysis** — breaks down lowercase, uppercase, digits, and special character usage
- **Real-Time Feedback** — instant analysis as you type, no page refresh needed
- **REST API** — Flask backend exposes analysis as a JSON endpoint for integration

---

## 🧠 Security Concepts Demonstrated

| Concept                      | Implementation                                                        |
| ---------------------------- | --------------------------------------------------------------------- |
| Shannon Entropy              | `H = L × log₂(N)` where L = length, N = character pool size           |
| Attack Vector Modeling       | Online throttled, online unthrottled, offline bcrypt, offline MD5/GPU |
| Dictionary Attack Awareness  | 20 most common passwords checked against zxcvbn database              |
| Credential Stuffing Patterns | Detects predictable formats like `Capital + word + numbers`           |
| Cryptographic Hash Awareness | Crack times vary by hash type (bcrypt vs MD5)                         |
| Brute-Force Complexity       | Combination count = sum of N^i for i = 1 to password length           |

---

## 🛠️ Tech Stack

| Layer           | Technology            | Purpose                                        |
| --------------- | --------------------- | ---------------------------------------------- |
| Frontend        | HTML, CSS, JavaScript | UI, real-time analysis, visualizations         |
| Backend         | Python 3, Flask       | REST API server                                |
| Analysis Engine | zxcvbn (Dropbox)      | Industry-standard entropy + pattern scoring    |
| API Layer       | Flask-CORS            | Cross-origin requests between frontend and API |

---

## 📁 Project Structure

```
password-analyzer/
├── analyzer.py        # Core security logic — entropy, crack times, pattern detection
├── app.py             # Flask REST API server
├── index.html         # Standalone frontend — works without the backend
├── requirements.txt   # Python dependencies
└── README.md          # You are here
```

---

## ⚡ Quick Start

### Option 1 — Frontend Only (Fastest)

No installation needed. Just open the file in your browser:

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/password-analyzer.git
cd password-analyzer

# Open directly in browser
open index.html          # macOS
start index.html         # Windows
xdg-open index.html      # Linux
```

### Option 2 — Full Stack (Frontend + Python API)

**Requirements:** Python 3.8+

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/password-analyzer.git
cd password-analyzer

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Start the API server
python app.py
```

API will be running at `http://localhost:5000`

Then open `index.html` in your browser.

---

## 🔌 API Reference

### `POST /analyze`

Analyzes a password and returns full security report.

**Request:**

```json
{
  "password": "MyP@ssw0rd123!"
}
```

**Response:**

```json
{
  "password_length": 14,
  "entropy_bits": 91.8,
  "score": 4,
  "strength_label": "Very Strong",
  "strength_color": "#10b981",
  "crack_times": {
    "Online (throttled)": "3,241 years",
    "Online (unthrottled)": "32 years",
    "Offline — bcrypt": "12 hours",
    "Offline — MD5/GPU": "Instant"
  },
  "pattern_warnings": [],
  "suggestions": ["Strong password! Store it in a password manager."],
  "character_analysis": {
    "has_lowercase": true,
    "has_uppercase": true,
    "has_digits": true,
    "has_symbols": true,
    "unique_chars": 13
  }
}
```

### `GET /health`

Returns API status.

```json
{ "status": "ok", "message": "Password Analyzer API running" }
```

---

## 🧪 How the Entropy Calculation Works

Entropy is calculated using the formula:

```
H = L × log₂(N)
```

Where:

- `H` = entropy in bits
- `L` = password length
- `N` = size of the character pool used

| Character Set        | Pool Size |
| -------------------- | --------- |
| Lowercase only (a–z) | 26        |
| + Uppercase (A–Z)    | 52        |
| + Digits (0–9)       | 62        |
| + Symbols (!@#...)   | 94        |

A password with 94-character pool and 16 characters has:

```
H = 16 × log₂(94) = 16 × 6.55 = 104.8 bits
```

At 100 billion guesses per second, that would take approximately **125 million years** to crack.

---

## ⚔️ Attack Scenarios Modeled

| Scenario              | Speed               | Real-World Example            |
| --------------------- | ------------------- | ----------------------------- |
| Online (rate-limited) | 100/sec             | Login form with lockout       |
| Online (unthrottled)  | 10,000/sec          | Login with no rate limiting   |
| Offline — bcrypt      | 10,000,000/sec      | Cracking a stolen bcrypt hash |
| Offline — MD5/GPU     | 100,000,000,000/sec | GPU rig attacking MD5 hash    |

---

## 🚨 Pattern Weaknesses Detected

The tool flags passwords that match any of these patterns:

1. Password is in the top 20 most commonly used passwords
2. Contains repeated characters (`aaa`, `111`)
3. Contains sequential patterns (`123`, `abc`, `qwerty`)
4. Follows `Capital + word + numbers` format (`Michael1990`)
5. Contains authentication-related keywords (`password`, `admin`, `login`)
6. Shorter than 8 characters
7. No special characters

---

## 📦 Dependencies

```
flask==3.0.0
flask-cors==4.0.0
zxcvbn==4.4.28
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## 🔒 Security Note

This tool is built for **educational and awareness purposes only**. Passwords analyzed are never stored, logged, or transmitted anywhere. The brute-force simulation runs entirely locally and is capped at 4-character passwords to prevent browser or system overload.

---

## 📚 Relevant Certifications & Exam Domains

This project directly maps to content covered in:

- **ISC2 Certified in Cybersecurity (CC)** — Domain 3: Access Controls, Domain 5: Security Operations
- **CompTIA Security+** — Domain 3.7: Authentication and Authorization
- **AWS Security Specialty** — Identity and Access Management concepts

---

## 👤 Author

**Avinesh Mohanaranjan**
IT Graduate | Technical Support Manager

- GitHub: [@avim505](https://github.com/avim505)
- LinkedIn: [your-linkedin](https://linkedin.com/in/avineshmohanaranjan)
