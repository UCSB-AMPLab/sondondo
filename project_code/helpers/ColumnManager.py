from pathlib import Path
import json
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename="logs/column_manager.log")
logger = logging.getLogger(__name__)

class ColumnManager:
    """
    Class to manage column names and mappings for different events.
    """

    def create_mapping(self, csv_file, mapping_file, dry_run=False):
        """
        Create a mapping from a CSV file.
        """
        logger.info(f"Creating mapping from {csv_file} to {mapping_file} with dry_run={dry_run}")
        df = pd.read_csv(csv_file, encoding="utf-8")
        mapping = df.columns.to_series().to_dict()
        if not dry_run:
            with open(mapping_file, "w", encoding="utf-8") as f:
                json.dump(mapping, f, indent=4, ensure_ascii=False)
            logger.info(f"Mapping created and saved to {mapping_file}")
        
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
        if not isinstance(csv_file, pd.DataFrame):
            df = pd.read_csv(csv_file, encoding="utf-8")
        else:
            df = csv_file
        mapping = self.load_mapping(mapping_file)
        logger.info(f"Harmonizing columns from {csv_file} using mapping from {mapping_file}")
        try:
            return df.rename(columns=mapping)
        except Exception as e:
            logger.error(f"Error harmonizing columns: {e}")
            raise e
