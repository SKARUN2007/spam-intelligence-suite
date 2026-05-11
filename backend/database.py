import sqlite3
import os

# Allow overriding paths via environment variables for cloud persistence
DATA_DIR = os.getenv('DATA_DIR', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'))
DB_PATH = os.path.join(DATA_DIR, 'spam_intelligence.db')

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        text TEXT,
        label TEXT,
        confidence REAL,
        is_spam INTEGER,
        metadata TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_id INTEGER,
        actual_label TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (scan_id) REFERENCES scans (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def log_scan(text, label, confidence, is_spam, metadata_json="{}"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO scans (text, label, confidence, is_spam, metadata)
    VALUES (?, ?, ?, ?, ?)
    ''', (text, label, confidence, 1 if is_spam else 0, metadata_json))
    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return scan_id

def log_feedback(scan_id, actual_label):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO feedback (scan_id, actual_label)
    VALUES (?, ?)
    ''', (scan_id, actual_label))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM scans')
    total_scans = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM scans WHERE is_spam = 1')
    total_spam = cursor.fetchone()[0]
    cursor.execute('SELECT id, timestamp, label, confidence, is_spam FROM scans ORDER BY timestamp DESC LIMIT 10')
    recent_scans = [{"id": r[0], "timestamp": r[1], "label": r[2], "confidence": r[3], "is_spam": bool(r[4])} for r in cursor.fetchall()]
    conn.close()
    return {
        "total_scans": total_scans,
        "total_spam": total_spam,
        "total_ham": total_scans - total_spam,
        "recent_scans": recent_scans
    }
