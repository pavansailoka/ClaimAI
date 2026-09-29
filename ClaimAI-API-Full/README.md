# ClaimAI Full API Project

## Structure

- `backend/` - Flask application
- `backend/api/` - separate API routes and service/database layer
- `backend/data/` - SQLite database created automatically
- `frontend/` - frontend files can be connected to the API
- `.venv/` - created locally by setup script; not included in the ZIP

## Requirements

Windows + Python 3.11 or newer.

## One-click setup

1. Open `backend`.
2. Double-click `setup_windows.bat`.
3. Double-click `run_windows.bat`.
4. Open `http://127.0.0.1:5000/api/health`.

Expected:

{"ok":true,"service":"claimai-api"}

## Manual setup

```powershell
cd backend
py -3 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

## API

GET `/api/health`
GET `/api/claims`
GET `/api/claims/<scenario>`
PUT `/api/claims/<scenario>`
POST `/api/claims/<scenario>/evidence`
POST `/api/claims/<scenario>/verify`
POST `/api/claims/<scenario>/reset`
GET `/api/claims/<scenario>/package`

Scenarios: `agriculture`, `motor`, `health`, `property`.

## Important

The `.venv` folder is intentionally not packaged because virtual environments contain machine-specific binaries. The setup script creates it automatically on your PC.
