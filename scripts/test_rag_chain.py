from app.rag_chain import ask_rag


def main() -> None:
    questions = [
        "Quels événements culturels puis-je faire prochainement dans le Val-de-Marne ?",
        "Je cherche une sortie à Nogent-sur-Marne",
        "Quels événements sont adaptés à une visite culturelle ?",
        "Y a-t-il des événements gratuits ?",
    ]

    for i, question in enumerate(questions, start=1):
        print("\n" + "=" * 50)
        print(f"TEST {i}")
        print("=" * 50)

        result = ask_rag(question)

        print("\nQUESTION")
        print(result["question"])

        print("\nRÉPONSE")
        print(result["answer"])

        print("\nSOURCES")
        for source in result["sources"]:
            print("-", source)


if __name__ == "__main__":
    main()