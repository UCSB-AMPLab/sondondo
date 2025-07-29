import re
import pandas as pd
import numpy as np
import pytest
from helpers import attributeHarmonizer
from helpers.LogerHandler import setup_logger
from helpers.ColumnManager import ColumnManager
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent / "logs" / "test_results"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

logger = setup_logger("test_attributeHarmonizer", log_dir=LOGS_DIR)
logger.info("Starting test_attributeHarmonizer")

datasets = {
    "bautismos": {
        "csv_file": "data/raw/bautismos.csv",
        "mapping_file": "data/mappings/bautismosMapping.json"
    },
    "entierros": {
        "csv_file": "data/raw/entierros.csv",
        "mapping_file": "data/mappings/entierrosMapping.json"
    },
    "matrimonios": {
        "csv_file": "data/raw/matrimonios.csv",
        "mapping_file": "data/mappings/matrimoniosMapping.json"
    }
}

for dataset in datasets.values():
    column_manager = ColumnManager()
    dataset = column_manager.harmonize_columns(dataset["csv_file"], dataset["mapping_file"])
    #logger.info(f"Dataset columns: {dataset.columns.tolist()}")
    if any(re.search(r'_legitimacy_', col) for col in dataset.columns):
        legitimacy_columns = [col for col in dataset.columns if '_legitimacy_' in col]
        df = dataset[legitimacy_columns]
        logger.info(f"Legitimacy columns: {df.columns.tolist()}")
