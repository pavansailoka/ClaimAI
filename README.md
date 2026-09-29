# ClaimAI

ClaimAI is a full-stack insurance claim workflow management application designed to digitize and simplify the process of collecting, managing, verifying, and organizing claim information.

The application provides a web-based interface connected to a Python Flask backend and SQLite database. Users can manage different claim scenarios, update claim information, add evidence, verify claim data, reset scenarios, and generate a structured claim package.

> **Important:** ClaimAI is a claim-workflow management and information-recording system. It does not independently make insurance coverage or settlement decisions.

---

## Features

* Full-stack frontend and backend integration
* Insurance claim workflow management
* Multiple claim scenarios

  * Agriculture
  * Motor
  * Health
  * Property
* Claim information management
* Evidence upload and management
* Claim verification workflow
* Claim reset functionality
* SQLite database storage
* REST API integration
* Claim package generation
* Health-check API
* Single-server deployment for frontend and backend

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS

### Database

* SQLite

### API

* REST API

---

## Project Structure

```text
ClaimAI-Connected-Full/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── service.py
│   │
│   └── data/
│       └── claims.db
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── assets/
│
├── .venv/
├── setup_windows.bat
├── run_windows.bat
├── run.ps1
├── .gitignore
└── README.md
```

---

## Requirements

Before running the project, install:

* Python 3
* VS Code
* Web browser

Check Python installation:

```powershell
python --version
```

or:

```powershell
py --version
```

---

# Installation

## 1. Open the project

Extract the project ZIP and open the `ClaimAI-Connected-Full` folder in VS Code.

---

## 2. Create Virtual Environment

Open the VS Code terminal and run:

```powershell
py -m venv .venv
```

---

## 3. Activate Virtual Environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

at the beginning of the terminal.

---

## 4. Install Dependencies

Run:

```powershell
python -m pip install -r backend\requirements.txt
```

The main dependencies are:

```text
Flask
Flask-CORS
```

---

# Running the Application

Move into the backend folder:

```powershell
cd backend
```

Start the Flask server:

```powershell
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000/
```

Open this URL in your browser.

---

# API Endpoints

| Method | Endpoint                          | Description                   |
| ------ | --------------------------------- | ----------------------------- |
| GET    | `/api/health`                     | Check API status              |
| GET    | `/api/scenarios`                  | Get available claim scenarios |
| GET    | `/api/claims`                     | Get all claims                |
| GET    | `/api/claims/<scenario>`          | Get a specific claim          |
| PUT    | `/api/claims/<scenario>`          | Update claim information      |
| POST   | `/api/claims/<scenario>/evidence` | Add claim evidence            |
| POST   | `/api/claims/<scenario>/verify`   | Verify claim information      |
| POST   | `/api/claims/<scenario>/reset`    | Reset claim scenario          |
| GET    | `/api/claims/<scenario>/package`  | Generate claim package        |

---

# Testing the Backend

After starting Flask, open:

```text
http://127.0.0.1:5000/api/health
```

A successful response should look similar to:

```json
{
    "status": "ok",
    "service": "ClaimAI API",
    "version": "1.0"
}
```

---

# Frontend and Backend Connection

The ClaimAI frontend communicates with the Flask backend using REST API endpoints.

```text
User
  │
  ▼
Frontend
HTML + CSS + JavaScript
  │
  │ REST API
  ▼
Flask Backend
  │
  ▼
SQLite Database
```

The frontend and backend are served through the same Flask application.

Therefore, users can access the complete application through:

```text
http://127.0.0.1:5000/
```

---

# Claim Workflow

The basic ClaimAI workflow is:

```text
Select Claim Scenario
        ↓
View Claim Information
        ↓
Update Claim Details
        ↓
Add Evidence
        ↓
Verify Claim Information
        ↓
Generate Claim Package
```

Supported scenarios include:

```text
Agriculture
Motor
Health
Property
```

---

# Database

ClaimAI uses SQLite for local data storage.

The database is automatically maintained inside:

```text
backend/data/claims.db
```

It stores claim workflow information such as claim details, evidence, and verification-related data.

---

# Windows Quick Start

After the project has been extracted, you can also use:

```powershell
.\setup_windows.bat
```

This creates the virtual environment and installs the required dependencies.

Then run:

```powershell
.\run_windows.bat
```

The application will start at:

```text
http://127.0.0.1:5000/
```

---

# Important Note

ClaimAI is designed as a **claim workflow and information management system**.

It helps organize:

* Claim information
* Evidence
* Verification workflow
* Claim packages

It does **not independently determine insurance coverage, approve claims, reject claims, or calculate final settlement decisions**.

---

# Future Enhancements

Possible future improvements include:

* User authentication and role-based access
* Cloud database integration
* AI-assisted document analysis
* OCR for insurance documents
* Fraud-risk indicators
* Automated evidence classification
* Cloud deployment
* Email/SMS notifications
* Advanced analytics dashboard
* Secure document storage

---

# License

This project is intended for educational, demonstration, and prototype purposes.
