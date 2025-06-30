from typing import Union
import pandas as pd
from pathlib import Path
import os

from utils.LoggerHandler import setup_logger

from utils.ColumnManager import ColumnManager

from actions.normalizers.DatesNormalizer import DateNormalizer
from georesolver import PlaceResolver

def setup_test_logger(test_name):
    """
    Set up a logger for a specific test.
    """
    logger = setup_logger(test_name)
    return logger

logger = setup_test_logger("datacleaning")

def prepare_dataset(csv_file: Union[str, Path]):

    logger.info(f"Preparing dataset from {csv_file}")

    dataset_event = os.path.basename(csv_file).split('.')[0].lower()
    if dataset_event not in ["matrimonios", "nacimientos", "defunciones"]:
        logger.error(f"Unsupported dataset event: {dataset_event}")
        raise ValueError(f"Unsupported dataset event: {dataset_event}")
    column_manager = ColumnManager()
    mapped_df = column_manager.harmonize_columns(csv_file, mapping_file=Path("data/mappings") / f"{dataset_event}Mapping.json")
    df = column_manager.return_useful_columns(mapped_df)
    logger.info(f"Dataset prepared with {len(df)} rows and {len(df.columns)} columns")
    return df

if __name__ == "__main__":
    # Example usage
    csv_file = Path("data/raw/matrimonios.csv")
    df = prepare_dataset(csv_file)
    print(df.head())