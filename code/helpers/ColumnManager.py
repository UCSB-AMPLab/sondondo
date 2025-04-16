from pathlib import Path
import json
import pandas as pd


class ColumnManager:
    """
    Class to manage column names and mappings for different events.
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def create_mapping(self, csv_file, mapping_file, dry_run=False):
        """
        Create a mapping from a CSV file.
        """
        df = pd.read_csv(csv_file, encoding="utf-8")
        mapping = df.columns.to_series().to_dict()
        if not dry_run:
            with open(mapping_file, "w", encoding="utf-8") as f:
                json.dump(mapping, f, indent=4, ensure_ascii=False)
        return mapping

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
