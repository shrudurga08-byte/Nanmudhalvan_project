"""Gemini integration: builds the prompt and returns generated legal text."""
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiDocumentGenerator:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or GEMINI_MODEL
        self._model = None  # created lazily so the app can start without a key

    @property
    def model(self):
        if self._model is None:
            if not GEMINI_API_KEY:
                raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")
            genai.configure(api_key=GEMINI_API_KEY)
            self._model = genai.GenerativeModel(self.model_name)
        return self._model

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective date: {dates}\n"
            f"Terms and conditions (semicolon separated): {terms}\n\n"
            "Formatting rules:\n"
            "- Output plain text only. Do NOT use markdown symbols such as #, ** or backticks.\n"
            "- Start with the document title on its own line.\n"
            "- Use numbered section headings on their own line, ending with a colon, "
            "e.g. '1. Services:'.\n"
            "- Use '- ' for bullet points where appropriate.\n"
            "- Use [square-bracket placeholders] for any details not provided.\n"
            "- Ensure formal legal structure with multiple sections and legal clauses, "
            "include every provided term, and end with a signature block.\n"
        )
        response = self.model.generate_content(prompt)
        return response.text