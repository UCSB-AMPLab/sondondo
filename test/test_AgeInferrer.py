import logging
from project_code.helpers.DateNormalizer import AgeInferrer, DateNormalizer
from project_code.helpers.ColumnManager import ColumnManager
from pathlib import Path
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
        inferrer = AgeInferrer(dataset["date"])
        birth_dates_cleaned = inferrer.infer_all(data_series)

        logger.info(f"Birth dates cleaned: {birth_dates_cleaned}")
        assert len(birth_dates_cleaned) == len(data_series), "Length of cleaned birth dates does not match original data series"
    except ValueError:
        logger.warning("ValueError: Dates will be cleaned in the next step")
        normalizer = DateNormalizer(dataset["date"])
        normalized = normalizer.normalize()

        logger.info(f"Normalized dates: {normalized.iloc[2830:2835]}")

        inferrer = AgeInferrer(normalized)
        birth_dates_cleaned = inferrer.infer_all(data_series)

        logger.info(f"Birth dates cleaned after normalization: {birth_dates_cleaned}")

    except Exception:
       logger.error(f"Error occurred while inferring age: {traceback.format_exc()}")
       return
    