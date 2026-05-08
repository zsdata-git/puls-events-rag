from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/processed/openagenda_events.csv")


def test_openagenda_file_exists():
    assert DATA_PATH.exists()


def test_openagenda_file_is_not_empty():
    df = pd.read_csv(DATA_PATH)
    assert len(df) > 0


def test_required_columns_exist():
    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "uid",
        "title_fr",
        "description_fr",
        "location_department",
        "firstdate_begin",
        "canonicalurl",
        "text_for_rag",
    ]

    for column in required_columns:
        assert column in df.columns


def test_text_for_rag_is_not_empty():
    df = pd.read_csv(DATA_PATH)
    assert df["text_for_rag"].notna().all()
    assert (df["text_for_rag"].str.len() > 20).all()


def test_events_are_from_val_de_marne():
    df = pd.read_csv(DATA_PATH)
    assert (df["location_department"] == "Val-de-Marne").all()