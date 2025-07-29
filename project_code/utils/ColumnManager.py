from pathlib import Path
import json
from typing import Union
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename=Path(__file__).parent.parent.parent / "logs/column_manager.log")
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

    def load_mapping(self, mapping_path: Union[str, Path]) -> dict:
        """
        Load a mapping from a JSON file.
        """
        with open(mapping_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def harmonize_columns(self, csv_file: Union[str, pd.DataFrame], mapping_file: Union[str, Path]) -> pd.DataFrame:
        """
        Harmonize the columns of a CSV file using a mapping.

        :param csv_file: Path to the CSV file or a DataFrame.
        :param mapping_file: Path to the JSON mapping file.
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

    def return_useful_columns(self, df, useful_columns_mapping: Union[str, Path] = Path("data/mappings/usefulColumnsMapping.json")):
        """
        Return a DataFrame with only the useful columns specified in the mapping.
        """
        mapping = self.load_mapping(useful_columns_mapping)
        mapkey = df["event_type"].iloc[0].lower()
        if mapkey not in mapping:
            logger.error(f"Event type '{mapkey}' not found in useful columns mapping.")
            raise ValueError(f"Event type '{mapkey}' not found in useful columns mapping.")
        
        useful_columns = mapping[mapkey] # returns a list of columns
        logger.info(f"Returning useful columns for event type '{mapkey}': {useful_columns}")
        return df[useful_columns]
    