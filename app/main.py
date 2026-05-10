import subprocess
import sys

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.rag_chain import ask_rag


app = FastAPI(
    title="Puls-Events RAG API",
    description="API REST pour interroger un assistant RAG d'événements culturels.",
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "Puls-Events RAG API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide.")

    result = ask_rag(request.question)
    return result


@app.post("/rebuild")
def rebuild():
    try:
        fetch_result = subprocess.run(
            [sys.executable, "scripts/fetch_openagenda.py"],
            capture_output=True,
            text=True,
            check=True,
        )

        build_result = subprocess.run(
            [sys.executable, "scripts/build_vectorstore.py"],
            capture_output=True,
            text=True,
            check=True,
        )

        return {
            "status": "success",
            "message": "Index FAISS reconstruit avec succès.",
            "fetch_output": fetch_result.stdout,
            "build_output": build_result.stdout,
        }

    except subprocess.CalledProcessError as error:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Erreur pendant la reconstruction de l'index.",
                "error": error.stderr,
            },
        )
    