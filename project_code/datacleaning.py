import pandas as pd
from pathlib import Path

from utils.LoggerHandler import setup_logger

from utils.ColumnManager import ColumnManager

def setup_test_logger(test_name):
    """
    Set up a logger for a specific test.
    """
    logger = setup_logger(test_name)
    return logger

logger = setup_test_logger("datacleaning")