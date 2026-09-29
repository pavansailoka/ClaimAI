import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from flask import g

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATABASE = DATA_DIR / "claims.db"

DEFAULT_CLAIMS = {
    "agriculture": {
        "sector": "Agriculture · PMFBY",
        "policy": "PMFBY-UP-2025-88420",
        "date": "2025-08-18",
        "location": "Barabanki, Uttar Pradesh",
        "loss": "Paddy crop damaged by floodwater after unusually heavy rain."
    },
    "motor": {
        "sector": "Motor insurance",
        "policy": "MOT-IND-2025-01862",
        "date": "2025-08-23",
        "location": "Pune, Maharashtra",
        "loss": "Front bumper and left headlamp damaged in a low-speed collision."
    },
    "health": {
        "sector": "Health insurance",
        "policy": "HLT-FAM-2025-76542",
        "date": "2025-08-12",
        "location": "New Delhi",
        "loss": "Hospital reimbursement request for a three-day admission due to dengue fever."
    },
    "property": {
        "sector": "Property insurance",
        "policy": "HOME-2025-30491",
        "date": "2025-08-19",
        "location": "Chennai, Tamil Nadu",
        "loss": "Ground floor water damage after severe local flooding."
    },
}

def now():
    return datetime.now(timezone.utc).isoformat()

def db():
    if "db" not in g:
        DATA_DIR.mkdir(exist_ok=True)
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(_error=None):
    connection = g.pop("db", None)
    if connection:
        connection.close()

def init_db():
    connection = db()
    connection.executescript("""
    CREATE TABLE IF NOT EXISTS claims (
        scenario TEXT PRIMARY KEY,
        sector TEXT NOT NULL,
        policy TEXT NOT NULL,
        incident_date TEXT NOT NULL,
        location TEXT NOT NULL,
        loss TEXT NOT NULL,
        status TEXT NOT NULL,
        readiness INTEGER NOT NULL,
        evidence INTEGER NOT NULL,
        evidence_total INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scenario TEXT NOT NULL,
        event TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    for scenario, item in DEFAULT_CLAIMS.items():
        exists = connection.execute(
            "SELECT 1 FROM claims WHERE scenario=?", (scenario,)
        ).fetchone()
        if not exists:
            timestamp = now()
            connection.execute("""
                INSERT INTO claims
                (scenario, sector, policy, incident_date, location, loss,
                 status, readiness, evidence, evidence_total, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, 'draft', 42, 3, 6, ?, ?)
            """, (
                scenario, item["sector"], item["policy"], item["date"],
                item["location"], item["loss"], timestamp, timestamp
            ))
            connection.execute("""
                INSERT INTO audit (scenario,event,message,created_at)
                VALUES (?, ?, ?, ?)
            """, (scenario, "draft_created", "Demo claim draft created", timestamp))
    connection.commit()

def serialize(row):
    return {
        "id": row["scenario"],
        "sector": row["sector"],
        "policy": row["policy"],
        "date": row["incident_date"],
        "location": row["location"],
        "loss": row["loss"],
        "status": row["status"],
        "readiness": row["readiness"],
        "evidence": row["evidence"],
        "evidenceTotal": row["evidence_total"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }

def get_claim(scenario):
    return db().execute(
        "SELECT * FROM claims WHERE scenario=?", (scenario,)
    ).fetchone()

def add_audit(scenario, event, message):
    db().execute(
        "INSERT INTO audit (scenario,event,message,created_at) VALUES (?,?,?,?)",
        (scenario, event, message, now())
    )
