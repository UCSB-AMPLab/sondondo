import pandas as pd
from pathlib import Path

from helpers.LogerHandler import setup_logger

from helpers.ColumnManager import ColumnManager

def setup_test_logger(test_name):
    """
    Set up a logger for a specific test.
    """
    logger = setup_logger(test_name)
    return logger

logger = setup_test_logger("datacleaning")

def working_dataframes():
    """
    Returns a list of DataFrames ready for cleaning and harmonization.
    """

    data = ["bautismos", "entierros", "matrimonios"]
    filesorigins = [Path("data/raw") / f"{d}.csv" for d in data]
    filesmappings = [Path("data/mappings") / f"{d}Mapping.json" for d in data]

    dataframes = []

    for data, fileorigin, filemapping in zip(data, filesorigins, filesmappings):
        column_manager = ColumnManager()
        dataset = column_manager.harmonize_columns(fileorigin, filemapping)
        dataset = column_manager.return_useful_columns(dataset)
        logger.info(f"Dataset {data} columns: {dataset.columns.tolist()}")
        dataframes.append(dataset)

    return dataframes

if __name__ == "__main__":
    logger.info("Starting data cleaning process")
    dataframes = working_dataframes()
    for df in dataframes:
        logger.info(f"DataFrame shape: {df.shape}")
        logger.info(f"DataFrame columns: {df.columns.tolist()}")
