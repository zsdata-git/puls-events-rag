from pathlib import Path

import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


INPUT_PATH = Path("data/processed/openagenda_events.csv")
OUTPUT_DIR = Path("data/vectorstore/faiss_index")


def load_events() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {INPUT_PATH}. "
            "Lance d'abord scripts/fetch_openagenda.py"
        )

    df = pd.read_csv(INPUT_PATH)

    if "text_for_rag" not in df.columns:
        raise ValueError("La colonne text_for_rag est absente du fichier CSV.")

    df = df.dropna(subset=["text_for_rag"])
    return df


def create_documents(df: pd.DataFrame) -> list[Document]:
    documents = []

    for _, row in df.iterrows():
        metadata = {
            "uid": str(row.get("uid", "")),
            "title": str(row.get("title_fr", "")),
            "city": str(row.get("location_city", "")),
            "department": str(row.get("location_department", "")),
            "region": str(row.get("location_region", "")),
            "start_date": str(row.get("firstdate_begin", "")),
            "end_date": str(row.get("firstdate_end", "")),
            "url": str(row.get("canonicalurl", "")),
        }

        document = Document(
            page_content=str(row["text_for_rag"]),
            metadata=metadata,
        )

        documents.append(document)

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    return splitter.split_documents(documents)


def build_faiss_index(chunks: list[Document]) -> FAISS:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    return vectorstore


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_events()
    documents = create_documents(df)
    chunks = split_documents(documents)
    vectorstore = build_faiss_index(chunks)

    vectorstore.save_local(str(OUTPUT_DIR))

    print(f"{len(df)} événements chargés")
    print(f"{len(documents)} documents créés")
    print(f"{len(chunks)} chunks créés")
    print(f"Index FAISS sauvegardé dans : {OUTPUT_DIR}")


if __name__ == "__main__":
    main()