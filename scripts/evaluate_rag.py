from pathlib import Path

import pandas as pd

from app.rag_chain import ask_rag


OUTPUT_PATH = Path("data/processed/rag_evaluation_results.csv")


TEST_QUESTIONS = [
    {
        "question": "Quels événements culturels puis-je faire prochainement dans le Val-de-Marne ?",
        "expected_keywords": ["Val-de-Marne", "ville", "date", "url"],
    },
    {
        "question": "Je cherche une sortie à Nogent-sur-Marne",
        "expected_keywords": ["Nogent-sur-Marne"],
    },
    {
        "question": "Quels événements sont adaptés à une visite culturelle ?",
        "expected_keywords": ["visite", "culture"],
    },
    {
        "question": "Y a-t-il des événements gratuits ?",
        "expected_keywords": ["gratuit", "entrée libre", "inscription"],
    },
]


def keyword_score(answer: str, expected_keywords: list[str]) -> float:
    answer_lower = answer.lower()
    matched = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() in answer_lower
    ]

    return round(len(matched) / len(expected_keywords), 2)


def source_coverage_score(sources: list[dict]) -> float:
    if not sources:
        return 0.0

    valid_sources = 0

    for source in sources:
        if (
            source.get("title")
            and source.get("city")
            and source.get("date")
            and source.get("url")
        ):
            valid_sources += 1

    return round(valid_sources / len(sources), 2)


def evaluate() -> pd.DataFrame:
    rows = []

    for item in TEST_QUESTIONS:
        question = item["question"]
        expected_keywords = item["expected_keywords"]

        print(f"Évaluation : {question}")

        result = ask_rag(question)

        rows.append(
            {
                "question": question,
                "answer": result["answer"],
                "keyword_score": keyword_score(result["answer"], expected_keywords),
                "source_coverage_score": source_coverage_score(result["sources"]),
                "sources_count": len(result["sources"]),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = evaluate()
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print("\nRésultats d'évaluation :")
    print(df[["question", "keyword_score", "source_coverage_score", "sources_count"]])

    print(f"\nFichier sauvegardé : {OUTPUT_PATH}")


if __name__ == "__main__":
    main()