from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI


INDEX_DIR = Path("data/vectorstore/faiss_index")


def load_vectorstore() -> FAISS:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        str(INDEX_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def format_documents(docs) -> str:
    context_parts = []

    for i, doc in enumerate(docs, start=1):
        context_parts.append(
            f"""
Événement {i}
Titre : {doc.metadata.get("title")}
Ville : {doc.metadata.get("city")}
Date : {doc.metadata.get("start_date")}
URL : {doc.metadata.get("url")}
Contenu : {doc.page_content}
"""
        )

    return "\n".join(context_parts)


def ask_rag(question: str) -> dict:
    load_dotenv()

    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    docs = retriever.invoke(question)
    context = format_documents(docs)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
Tu es un assistant intelligent pour Puls-Events.
Tu recommandes des événements culturels dans le Val-de-Marne.

Règles :
- Réponds uniquement avec les informations présentes dans le contexte.
- Si l'information n'est pas disponible, dis-le clairement.
- Propose des recommandations concrètes.
- Mentionne le titre, la ville, la date et l'URL quand disponible.
- Réponds en français.
""",
            ),
            (
                "human",
                """
Question utilisateur :
{question}

Contexte récupéré depuis FAISS :
{context}
""",
            ),
        ]
    )

    llm = ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.2,
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    return {
        "question": question,
        "answer": response.content,
        "sources": [
            {
                "title": doc.metadata.get("title"),
                "city": doc.metadata.get("city"),
                "date": doc.metadata.get("start_date"),
                "url": doc.metadata.get("url"),
            }
            for doc in docs
        ],
    }