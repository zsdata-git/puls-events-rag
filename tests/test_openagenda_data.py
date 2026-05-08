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


def test_events_are_recent():
    import pandas as pd

    df = pd.read_csv(DATA_PATH)

    # Conversion avec timezone UTC (IMPORTANT)
    df["firstdate_begin"] = pd.to_datetime(
        df["firstdate_begin"],
        utc=True,
        errors="coerce"
    )

    now = pd.Timestamp.now(tz="UTC")
    one_year_ago = now - pd.Timedelta(days=365)

    assert (df["firstdate_begin"] >= one_year_ago).all()