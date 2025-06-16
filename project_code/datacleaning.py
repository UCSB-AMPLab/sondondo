import pandas as pd
from pathlib import Path

from helpers.ColumnManager import ColumnManager


data = ["bautismos", "entierros", "matrimonios"]
filesorigins = [Path("data/raw") / f"{d}.csv" for d in data]
filesmappings = [Path("data/mappings") / f"{d}Mapping.json" for d in data]

for data, fileorigin, filemapping in zip(data, filesorigins, filesmappings):
    column_manager = ColumnManager()
    dataset = column_manager.harmonize_columns(fileorigin, filemapping)
    dataset = column_manager.return_useful_columns(dataset)
    print(f"Dataset for {data}:\n{dataset.head()}\n")