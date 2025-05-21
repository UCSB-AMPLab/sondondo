import logging
from project_code.helpers.DateNormalizer import AgeInferrer, DateNormalizer
from project_code.helpers.ColumnManager import ColumnManager
from pathlib import Path
from datetime import datetime
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
    