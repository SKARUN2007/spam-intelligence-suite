from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import os
import json
import email
import re
import requests
from email import policy
from fpdf import FPDF
from fastapi.middleware.cors import CORSMiddleware
from database import log_scan, log_feedback, get_stats, init_db, DATA_DIR

app = FastAPI(title="Production Spam Intelligence API")
init_db()

# Environment-based CORS for security
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'ensemble_model.joblib')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'tfidf_vectorizer.joblib')
REPORTS_DIR = os.path.join(DATA_DIR, 'reports') # Move reports to data dir for persistence
os.makedirs(REPORTS_DIR, exist_ok=True)

# Load components
ensemble = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
vectorizer = joblib.load(VECTORIZER_PATH) if os.path.exists(VECTORIZER_PATH) else None

class EmailRequest(BaseModel):
    text: str

class FeedbackRequest(BaseModel):
    scan_id: int
    actual_label: str

def detect_homograph(text):
    sensitive_domains = ['google', 'paypal', 'microsoft', 'amazon', 'apple', 'facebook', 'bank', 'secure']
    domains = re.findall(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]', text.lower())
    alerts = []
    for domain in domains:
        for s in sensitive_domains:
            if s in domain and domain != f"{s}.com" and domain != f"www.{s}.com":
                alerts.append({"domain": domain, "target": s, "type": "Look-alike Domain"})
    return alerts

def get_geo_info(ip):
    if not ip or ip.startswith('127.') or ip.startswith('192.168.'):
        return {"country": "Internal Network", "city": "N/A", "flag": "🌐"}
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        data = r.json()
        if data['status'] == 'success':
            return {"country": data['country'], "city": data['city'], "flag": "📍"}
    except: pass
    return {"country": "Unknown", "city": "N/A", "flag": "❓"}

def generate_pdf_report(scan_id, result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(99, 102, 241)
    pdf.cell(0, 20, "SECURITY AUDIT REPORT", ln=True, align='C')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Scan ID: {scan_id}", ln=True)
    pdf.line(10, 40, 200, 40)
    pdf.set_font("helvetica", "B", 16)
    status_color = (255, 77, 77) if result['is_spam'] else (0, 230, 118)
    pdf.set_text_color(*status_color)
    pdf.cell(0, 15, f"THREAT LEVEL: {'HIGH' if result['is_spam'] else 'LOW'}", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Confidence: {result['confidence']}%", ln=True)
    report_path = os.path.join(REPORTS_DIR, f"report_{scan_id}.pdf")
    pdf.output(report_path)
    return report_path

@app.post("/predict")
def predict_spam(request: EmailRequest):
    text_vec = vectorizer.transform([request.text])
    prediction = ensemble.predict(text_vec)[0]
    prob = ensemble.predict_proba(text_vec)[0]
    is_spam = bool(prediction)
    label = "spam" if is_spam else "ham"
    confidence = round(float(prob[prediction]) * 100, 2)
    homograph_alerts = detect_homograph(request.text)
    scan_id = log_scan(request.text, label, confidence, is_spam)
    return {"scan_id": scan_id, "label": label, "confidence": confidence, "is_spam": is_spam, "homograph_alerts": homograph_alerts}

@app.post("/upload")
async def upload_email(file: UploadFile = File(...)):
    content = await file.read()
    msg = email.message_from_bytes(content, policy=policy.default)
    body = msg.get_body(preferencelist=('plain',)).get_content() if msg.get_body() else str(content)[:1000]
    received = msg.get_all('Received', [])
    ip = None
    if received:
        match = re.search(r'\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]', received[0])
        if match: ip = match.group(1)
    geo = get_geo_info(ip)
    text_vec = vectorizer.transform([body])
    prediction = ensemble.predict(text_vec)[0]
    prob = ensemble.predict_proba(text_vec)[0]
    is_spam = bool(prediction)
    scan_id = log_scan(body, "spam" if is_spam else "ham", round(float(prob[prediction])*100, 2), is_spam, json.dumps({"geo": geo}))
    return {"scan_id": scan_id, "label": "spam" if is_spam else "ham", "confidence": round(float(prob[prediction])*100, 2), "is_spam": is_spam, "geo": geo, "homograph_alerts": detect_homograph(body), "body": body, "metadata": {"subject": msg['Subject'], "from": msg['From']}}

@app.get("/report/{scan_id}")
async def get_report(scan_id: int):
    import sqlite3
    from database import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    r = conn.execute("SELECT text, label, confidence, is_spam, metadata FROM scans WHERE id = ?", (scan_id,)).fetchone()
    conn.close()
    if not r: raise HTTPException(status_code=404, detail="Scan not found")
    result = {"text": r[0], "label": r[1], "confidence": r[2], "is_spam": bool(r[3]), "metadata": json.loads(r[4] if r[4] else "{}")}
    path = generate_pdf_report(scan_id, result)
    return FileResponse(path, filename=f"Security_Audit_{scan_id}.pdf")

@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    log_feedback(request.scan_id, request.actual_label)
    return {"status": "success"}

@app.get("/stats")
def fetch_stats(): return get_stats()

if __name__ == "__main__":
    import uvicorn
    # Use PORT environment variable for Render compatibility
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
