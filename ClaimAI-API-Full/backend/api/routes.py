from datetime import datetime
from flask import Blueprint, jsonify, request, abort, Response
from .service import db, get_claim, serialize, add_audit, now, DEFAULT_CLAIMS

api = Blueprint("api", __name__)

def claim_or_404(scenario):
    if scenario not in DEFAULT_CLAIMS:
        abort(404, description="Claim not found")
    row = get_claim(scenario)
    if row is None:
        abort(404, description="Claim not found")
    return row

@api.get("/health")
def health():
    return jsonify(ok=True, service="claimai-api")

@api.get("/claims")
def all_claims():
    rows = db().execute("SELECT * FROM claims ORDER BY scenario").fetchall()
    return jsonify(claims=[serialize(row) for row in rows])

@api.get("/claims/<scenario>")
def get_one(scenario):
    return jsonify(claim=serialize(claim_or_404(scenario)))

@api.put("/claims/<scenario>")
def update_claim(scenario):
    claim_or_404(scenario)
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Request body must be valid JSON")

    fields = ["sector", "policy", "date", "location", "loss"]
    values = []
    for field in fields:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            abort(422, description=f"{field} is required")
        values.append(value.strip())

    try:
        datetime.strptime(values[2], "%Y-%m-%d")
    except ValueError:
        abort(422, description="date must use YYYY-MM-DD")

    db().execute("""
        UPDATE claims
        SET sector=?, policy=?, incident_date=?, location=?, loss=?, updated_at=?
        WHERE scenario=?
    """, (*values, now(), scenario))
    add_audit(scenario, "claim_updated", "Claim details updated")
    db().commit()
    return jsonify(claim=serialize(claim_or_404(scenario)))

@api.post("/claims/<scenario>/evidence")
def add_evidence(scenario):
    item = claim_or_404(scenario)
    evidence = min(item["evidence"] + 1, item["evidence_total"])
    readiness = min(max(item["readiness"], 56), 91)
    db().execute("""
        UPDATE claims SET evidence=?, readiness=?, updated_at=? WHERE scenario=?
    """, (evidence, readiness, now(), scenario))
    add_audit(scenario, "evidence_added", "Additional evidence source connected")
    db().commit()
    return jsonify(claim=serialize(claim_or_404(scenario)))

@api.post("/claims/<scenario>/verify")
def verify(scenario):
    claim_or_404(scenario)
    db().execute("""
        UPDATE claims
        SET status='verified', readiness=91, evidence=evidence_total, updated_at=?
        WHERE scenario=?
    """, (now(), scenario))
    add_audit(scenario, "verification_completed",
              "Evidence sources were cross-checked for this demo")
    db().commit()
    return jsonify(claim=serialize(claim_or_404(scenario)))

@api.post("/claims/<scenario>/reset")
def reset(scenario):
    claim_or_404(scenario)
    db().execute("DELETE FROM audit WHERE scenario=?", (scenario,))
    db().execute("DELETE FROM claims WHERE scenario=?", (scenario,))
    item = DEFAULT_CLAIMS[scenario]
    timestamp = now()
    db().execute("""
        INSERT INTO claims
        (scenario,sector,policy,incident_date,location,loss,status,readiness,
         evidence,evidence_total,created_at,updated_at)
        VALUES (?,?,?,?,? ,?,'draft',42,3,6,?,?)
    """, (
        scenario, item["sector"], item["policy"], item["date"],
        item["location"], item["loss"], timestamp, timestamp
    ))
    add_audit(scenario, "draft_created", "Demo claim reset")
    db().commit()
    return jsonify(claim=serialize(claim_or_404(scenario)))

@api.get("/claims/<scenario>/package")
def package(scenario):
    item = claim_or_404(scenario)
    content = f"""ClaimAI Claim Package

Policy: {item['policy']}
Sector: {item['sector']}
Incident: {item['incident_date']}, {item['location']}

Reported loss:
{item['loss']}

Verification: {'VERIFIED' if item['status'] == 'verified' else 'IN PROGRESS'}
Confidence: {item['readiness']}%
Evidence: {item['evidence']} of {item['evidence_total']} sources connected

Demo artifact — final coverage and settlement decisions remain with the authorized insurer.
"""
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition":
                 f'attachment; filename="claimai-{scenario}-package.txt"'}
    )
