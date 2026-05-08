# Puls Events RAG

Projet de chatbot intelligent pour recommandation culturelle.

## Stack

- Python
- FastAPI
- LangChain
- Mistral
- FAISS

## Installation

uv sync


## Étape 2 - Pré-processing OpenAgenda

Les événements sont récupérés depuis l’API OpenAgenda pour le département du Val-de-Marne.

Le script `scripts/fetch_openagenda.py` :
- interroge l’API OpenAgenda ;
- filtre les événements sur le Val-de-Marne, avec un historique récent (moins de 1 an) ;
- sélectionne les colonnes utiles ;
- nettoie les valeurs manquantes ;
- crée une colonne `text_for_rag` prête pour l’indexation vectorielle ;
- sauvegarde le fichier final dans `data/processed/openagenda_events.csv`.

## Lancer : 
```bash
uv run python scripts/fetch_openagenda.py
```

## Tests

```bash
uv run pytest
```

## Étape 3 - Base vectorielle FAISS

Les événements sont transformés en embeddings via un modèle HuggingFace (`all-MiniLM-L6-v2`) puis indexés dans une base FAISS.

Script :

```bash
uv run python scripts/build_vectorstore.py
```

Test : 
```bash
uv run python scripts/test_search_vectorstore.py
``` 

