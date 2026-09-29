from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_core.gemini_generator import GeminiDocumentGenerator
from ai_core.generator import sanitize_text
from legalEaseAPI.database import get_db
from legalEaseAPI.models import LegalDocument

router = APIRouter()
gemini_generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=1)
    parties: str = Field(min_length=1)
    terms: str = ""
    dates: str = Field(min_length=1)


class DocumentUpdate(BaseModel):
    content: str = Field(min_length=1)


def _to_dict(d: LegalDocument, with_content: bool = True) -> dict:
    data = {
        "id": d.id,
        "document_type": d.document_type,
        "parties": d.parties,
        "terms": d.terms,
        "dates": d.dates,
        "created_at": d.created_at.isoformat(),
        "updated_at": d.updated_at.isoformat(),
    }
    if with_content:
        data["document"] = d.content
    return data


@router.post("/generate")
def generate_legal_document(request: DocumentRequest, db: Session = Depends(get_db)):
    try:
        raw = gemini_generator.generate_document(
            request.document_type, request.parties, request.terms, request.dates
        )
    except RuntimeError as e:  # e.g. missing API key
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini error: {e}")

    text = sanitize_text(raw)
    doc = LegalDocument(
        document_type=request.document_type, parties=request.parties,
        terms=request.terms, dates=request.dates, content=text,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "document": text}


@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    rows = db.scalars(select(LegalDocument).order_by(LegalDocument.id.desc()).limit(50)).all()
    return [_to_dict(r, with_content=False) for r in rows]


@router.get("/documents/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.get(LegalDocument, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    return _to_dict(doc)


@router.put("/documents/{doc_id}")
def update_document(doc_id: int, body: DocumentUpdate, db: Session = Depends(get_db)):
    doc = db.get(LegalDocument, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    doc.content = body.content
    db.commit()
    db.refresh(doc)
    return _to_dict(doc)


@router.delete("/documents/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.get(LegalDocument, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    db.delete(doc)
    db.commit()
    return {"deleted": doc_id}