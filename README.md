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
- filtre les événements sur le Val-de-Marne ;
- sélectionne les colonnes utiles ;
- nettoie les valeurs manquantes ;
- crée une colonne `text_for_rag` prête pour l’indexation vectorielle ;
- sauvegarde le fichier final dans `data/processed/openagenda_events.csv`.


## Tests

```bash
uv run pytest
```
