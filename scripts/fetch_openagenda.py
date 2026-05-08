from pathlib import Path
import pandas as pd
import requests


DATASET_ID = "evenements-publics-openagenda"
BASE_URL = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets"
OUTPUT_PATH = Path("data/processed/openagenda_events.csv")


def fetch_events(limit: int = 500) -> list[dict]:
    url = f"{BASE_URL}/{DATASET_ID}/records"

    params = {
        "limit": limit,
        "refine": "location_department:Val-de-Marne",
        "order_by": "firstdate_begin desc",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json().get("results", [])


def clean_events(events: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(events)

    # Conversion en datetime avec timezone UTC
    df["firstdate_begin"] = pd.to_datetime(
        df["firstdate_begin"],
        errors="coerce",
        utc=True,
    )

    # Date actuelle avec timezone UTC
    now = pd.Timestamp.now(tz="UTC")

    # Il y a 1 an
    one_year_ago = now - pd.Timedelta(days=365)

    # Garder uniquement les événements de moins d'un an
    df = df[df["firstdate_begin"] >= one_year_ago]

    columns_to_keep = [
        "uid",
        "title_fr",
        "description_fr",
        "longdescription_fr",
        "location_name",
        "location_city",
        "location_department",
        "location_region",
        "firstdate_begin",
        "firstdate_end",
        "canonicalurl",
        "keywords_fr",
    ]

    for column in columns_to_keep:
        if column not in df.columns:
            df[column] = ""

    df = df[columns_to_keep]

    df = df.drop_duplicates(subset=["uid"])
    df = df.dropna(subset=["title_fr"])

    df["description_fr"] = df["description_fr"].fillna("")
    df["longdescription_fr"] = df["longdescription_fr"].fillna("")
    df["location_name"] = df["location_name"].fillna("")
    df["location_city"] = df["location_city"].fillna("")
    df["location_department"] = df["location_department"].fillna("")
    df["location_region"] = df["location_region"].fillna("")
    df["firstdate_begin"] = df["firstdate_begin"].fillna("")
    df["firstdate_end"] = df["firstdate_end"].fillna("")
    df["canonicalurl"] = df["canonicalurl"].fillna("")
    df["keywords_fr"] = df["keywords_fr"].fillna("")

    df["text_for_rag"] = (
        "Titre : " + df["title_fr"].astype(str) + "\n"
        + "Description : " + df["description_fr"].astype(str) + "\n"
        + "Description longue : " + df["longdescription_fr"].astype(str) + "\n"
        + "Lieu : " + df["location_name"].astype(str) + ", "
        + df["location_city"].astype(str) + "\n"
        + "Département : " + df["location_department"].astype(str) + "\n"
        + "Région : " + df["location_region"].astype(str) + "\n"
        + "Date début : " + df["firstdate_begin"].astype(str) + "\n"
        + "Date fin : " + df["firstdate_end"].astype(str) + "\n"
        + "URL : " + df["canonicalurl"].astype(str)
    )

    return df


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    events = fetch_events(limit=100)
    df = clean_events(events)

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print(f"{len(df)} événements sauvegardés dans {OUTPUT_PATH}")


if __name__ == "__main__":
    main()