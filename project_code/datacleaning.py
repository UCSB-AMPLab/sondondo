import pandas as pd
from pathlib import Path

from utils.LoggerHandler import setup_logger

from utils.ColumnManager import ColumnManager

from actions.normalizers.DatesNormalizer import DateNormalizer

def setup_test_logger(test_name):
    """
    Set up a logger for a specific test.
    """
    logger = setup_logger(test_name)
    return logger

logger = setup_test_logger("datacleaning")

dummyPandasSerieswithDates = pd.Series([
    "2023-01-01",
    "2022-12-31",
    "2021-06-15",
    "invalid_date",
    "2020-02-29"
])

def test_date_normalizer():
    """
    Test the DateNormalizer class.
    """
    logger.info("Starting test_date_normalizer")
    
    normalizer = DateNormalizer(dummyPandasSerieswithDates)
    normalized_dates = normalizer.normalize()
    
    logger.info(f"Normalized dates: {normalized_dates}")


test_date_normalizer()