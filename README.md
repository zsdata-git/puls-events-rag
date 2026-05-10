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

## Étape 4 - Chaîne RAG LangChain + Mistral

Le système charge l’index FAISS, récupère les événements les plus pertinents avec un retriever LangChain, puis transmet le contexte au modèle Mistral pour générer une réponse en français.

Commande de test :

```bash
$env:PYTHONPATH="."
uv run python scripts/test_rag_chain.py
```

Tests effectués :

- Requête générale : recommandations pertinentes.
- Requête géographique : récupération cohérente d’événements liés à la ville demandée.
- Requête thématique : résultats globalement pertinents.
- Requête sur attribut de gratuité : résultats exploitables, mais dépendants de la qualité des champs descriptifs OpenAgenda.

Conclusion : la chaîne RAG fonctionne. Les réponses sont construites à partir des documents récupérés dans FAISS, puis reformulées en langage naturel par le modèle Mistral. La qualité dépend principalement de la complétude des métadonnées OpenAgenda. 

## Étape 5 — API REST avec FastAPI

Le système RAG est maintenant exposé via une API REST permettant d’interroger les événements culturels.

### Lancer l’API

```bash
uv run uvicorn app.main:app --reload
```

L’API est accessible à l’adresse :
http://127.0.0.1:8000

Documentation interactive (Swagger) :
http://127.0.0.1:8000/docs

+ Endpoints disponibles
**GET /**

Vérifie que l’API fonctionne.

**GET /health**

Retourne le statut de l’API.

**POST /ask**

Permet de poser une question au système RAG.

Exemple :
{
  "question": "Je cherche une sortie culturelle à Nogent-sur-Marne"
}

Réponse :
{
  "question": "...",
  "answer": "...",
  "sources": [...]
}

**POST /rebuild**

Reconstruit la base vectorielle FAISS à partir des données OpenAgenda.


Test de l’API

Un script de test est disponible :
```bash
uv run python scripts/api_test.py
```

Ce script :

- vérifie le endpoint /health
- envoie une requête au endpoint /ask

✅ Résultat

Une API REST locale permettant :

d’interroger un chatbot RAG
d’obtenir des recommandations d’événements
de reconstruire dynamiquement l’index FAISS