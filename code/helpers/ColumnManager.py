from pathlib import Path
import json
import pandas as pd


class ColumnManager:
    """
    Class to manage column names and mappings for different events.
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def load_mapping(self, mapping_path):  #return dictionary that used for mapping
        """
        Load a mapping from a JSON file.
        """
        with open(mapping_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def harmonize_columns(self, csv_file, mapping_file):
        """
        Harmonize the columns of a CSV file using a mapping.
        """
        df = pd.read_csv(csv_file, encoding="utf-8")
        mapping = self.load_mapping(mapping_file)
        return df.rename(columns=mapping)
