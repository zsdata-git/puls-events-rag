from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


INDEX_DIR = Path("data/vectorstore/faiss_index")


def main() -> None:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        str(INDEX_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    query = "Je cherche une sortie culturelle gratuite dans le Val-de-Marne"

    results = vectorstore.similarity_search(query, k=3)

    for i, doc in enumerate(results, start=1):
        print(f"\n--- Résultat {i} ---")
        print("Titre :", doc.metadata.get("title"))
        print("Ville :", doc.metadata.get("city"))
        print("Date :", doc.metadata.get("start_date"))
        print("URL :", doc.metadata.get("url"))
        print(doc.page_content[:500])


if __name__ == "__main__":
    main()