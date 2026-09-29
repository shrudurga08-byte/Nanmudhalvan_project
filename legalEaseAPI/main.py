from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from legalEaseAPI.database import Base, engine
from legalEaseAPI import models  # noqa: F401  (registers tables)
from legalEaseAPI.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LegalEase - AI Legal Document Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Welcome to LegalEase AI Legal Document Generator API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)