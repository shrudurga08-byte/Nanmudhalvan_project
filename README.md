# LegalEase - AI Legal Document Generator

Streamlit (frontend) + FastAPI (backend) + Gemini (AI) + SQLite (database).

## 1. Create the environment
Windows (PowerShell):
    python -m venv venv
    venv\Scripts\activate

macOS / Linux:
    python3 -m venv venv
    source venv/bin/activate

## 2. Install dependencies
    pip install -r requirements.txt

## 3. Configure the API key
    copy .env.example .env      (Windows)   |   cp .env.example .env   (macOS/Linux)
Edit `.env` and set GEMINI_API_KEY (get one at https://aistudio.google.com/apikey).

## 4. (Optional) generate placeholder logos
    python create_logo.py

## 5. Run
Terminal 1:  uvicorn legalEaseAPI.main:app --reload
Terminal 2:  streamlit run frontend/app.py
(or just `./run.sh` on macOS/Linux, `run.bat` on Windows)

- API docs:  http://localhost:8000/docs
- App:       http://localhost:8501

The SQLite file `legalease.db` is created automatically on first start.

## API
POST /generate            create + save a document
GET  /documents           list saved documents
GET  /documents/{id}      fetch one
PUT  /documents/{id}      update edited content
DELETE /documents/{id}    delete

## Deployment
Backend (Render/Railway/Fly.io):  uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port $PORT
Frontend (Streamlit Community Cloud): set API_URL to the deployed backend URL.
On hosts with ephemeral disks, set DATABASE_URL to a hosted Postgres (and `pip install psycopg2-binary`).
