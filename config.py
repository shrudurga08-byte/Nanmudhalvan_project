"""Central configuration for LegalEase."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
API_URL = os.getenv("API_URL", "http://localhost:8000")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{(BASE_DIR / 'legalease.db').as_posix()}")

LOGO_PATH = BASE_DIR / "Image" / "Logo.png"
FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
