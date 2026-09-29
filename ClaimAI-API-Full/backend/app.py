from flask import Flask
from flask_cors import CORS
from api.routes import api
from api.service import init_db
from pathlib import Path

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 250_000
CORS(app)

app.register_blueprint(api, url_prefix="/api")

@app.get("/")
def index():
    return """
    <h1>ClaimAI API Server</h1>
    <p>API is running.</p>
    <p><a href="/api/health">Check API health</a></p>
    """

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
