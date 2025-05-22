import logging
from helpers.DateNormalizer import AgeInferrer, DateNormalizer
from helpers.ColumnManager import ColumnManager
from pathlib import Path
from datetime import timedelta
import pandas as pd
import pytest
import traceback

LOGS_DIR = Path(__file__).parent.parent / "logs" / "test_results"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def setup_test_logger(test_name):
    """Set up a logger for a specific test"""
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.INFO)

    # Remove all handlers associated with the logger
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a file handler
    log_file = LOGS_DIR / f"{test_name}.log"
    fh = logging.FileHandler(log_file, mode='w')
    fh.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(fh)
    logger.propagate = False

    return logger

def test_age_inferrer():
    logger = setup_test_logger("test_age_inferrer")
    logger.info("Starting test_age_inferrer")

    columnManager = ColumnManager()
    dataset = columnManager.harmonize_columns(
        Path(__file__).parent.parent / "data" / "raw" / "bautismos.csv", 
        Path(__file__).parent.parent / "data" / "mappings" / "bautismosMapping.json"
        )
    data_series = dataset["birth_date"]

    try:
        logger.warning("ValueError: Dates will be cleaned in the next step")
        dates = dataset["date"].copy()
        normalizer = DateNormalizer(dates)
        normalized = normalizer.normalize()

        logger.info(f"Normalized dates: {normalized.iloc[2830:2835]}")

        inferrer = AgeInferrer(normalized)
        birth_dates_cleaned = inferrer.infer_all(data_series)

        validation_df = pd.DataFrame({
            "original_dates": dates,
            "normalized_dates": normalized,
            "original_birth_dates": data_series,
            "inferred_birth_dates": birth_dates_cleaned
        })
        logger.info(f"Validation DataFrame: {validation_df.sample(10)}")


    except Exception:
       logger.error(f"Error occurred while inferring age: {traceback.format_exc()}")
       return


dummy_series = pd.Series(["1900-01-01"] * 10)

@pytest.fixture
def inferrer():
    return AgeInferrer(dummy_series)

@pytest.mark.parametrize("age_text,expected", [
    ("del día", timedelta(days=0)),
    ("5 días", timedelta(days=5)),
    ("20 dias", timedelta(days=20)),
    ("1 mes", timedelta(days=30)),
    ("2 meses", timedelta(days=60)),
    ("3 meses y medio", timedelta(days=105)),
    ("1 año", timedelta(days=365)),
    ("2 años", timedelta(days=730)),
    ("1 año 2 meses", timedelta(days=365 + 60)),
    ("1 año 2 meses 10 días", timedelta(days=365 + 60 + 10)),
    ("3 meses y 10 días", timedelta(days=90 + 10)),
    ("1 mes y 20 días", timedelta(days=30 + 20)),
    ("  2    meses   y   medio ", timedelta(days=60 + 15)),
    ("5 “días”", timedelta(days=5)),
    ("1 año, 1 mes y 1 día", timedelta(days=365 + 30 + 1)),  # even with punctuation
    ("", None),
    ("edad desconocida", None),
    ("año y medio", None),  # Not supported yet
])
def test_parse_birth_age_to_timedelta(inferrer, age_text, expected):
    assert inferrer.parse_birth_age_to_timedelta(age_text) == expected