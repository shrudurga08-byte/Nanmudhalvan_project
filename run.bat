@echo off
call venv\Scripts\activate
start "LegalEase API" cmd /k "venv\Scripts\activate && uvicorn legalEaseAPI.main:app --reload --port 8000"
streamlit run frontend/app.py
