# 🛡️ Spam Intelligence & Forensics Suite

An enterprise-grade email security platform that combines **Machine Learning** with **Cyber-Security Forensics** to identify and neutralize communication threats.

## 🚀 Key Features

### 🧠 Advanced AI Engine
- **Voting Ensemble Classifier**: High-precision detection using a majority-vote system across **Multinomial Naive Bayes, Support Vector Machines (SVM), and Random Forest**.
- **TF-IDF Semantic Analysis**: Context-aware word importance weighting for superior classification accuracy (**98.74%**).

### 🕵️ Security Forensics (Master Level)
- **Homograph Attack Detection**: Automatically flags domain impersonation attempts (e.g., `g00gle.com` vs `google.com`).
- **Geo-IP Mapping**: Extracts sender IP addresses from `.eml` headers to resolve geographic origin and country flags.
- **Deep File Analysis**: Supports drag-and-drop `.eml` parsing for full header and metadata inspection.

### 🛡️ Defensive Tools
- **Sandboxed "Safe Viewer"**: A specialized UI mode that strips malicious scripts and tracking pixels for safe content inspection.
- **Automated Security Audits**: Generates professional PDF reports summarizing forensics data and threat levels.
- **Persistence & Analytics**: SQLite-backed history tracking with a comprehensive Admin Dashboard.

## 🛠️ Technical Stack
- **Frontend**: Next.js 15 (App Router), Framer Motion, Lucide Icons, Axios.
- **Backend**: FastAPI (Python), Scikit-Learn, FPDF2 (Reporting), Joblib.
- **Database**: SQLite (Production-ready persistence).
- **Deployment**: Dockerized for seamless hosting on Render and Vercel.

## 🏁 Getting Started

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---
*Developed for Advanced Internship Project 2026*
