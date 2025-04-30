import re
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, filename="logs/names_explorer.log")
logger = logging.getLogger(__name__)

class NamesManager:
    def __init__(self):
        # Add known filler terms or other annotation patterns here if needed
        self.filler_terms = {"n/a", "na"}

    def clean_name(self, name: str) -> str | None:
        """
        Cleans a name string by:
        - Removing non-alphabetic characters
        - Lowercasing everything
        - Removing filler terms and annotations (parentheses, brackets)
        """
        if not isinstance(name, str):
            return None
        
        name = name.lower()
        name = re.sub(r"[^a-zñáéíóúü\s]", "", name)      # keep only letters and spaces
        name = re.sub(r"\b(?:n/?a|na)\b", "", name)      # remove known filler terms
        name = re.sub(r"\s+", " ", name).strip()

        return name if name else None
    
    def clean_series(self, series: pd.Series, label: str = "") -> pd.Series:
        """
        Cleans specified name-related columns in a pandas DataFrame.
        Returns a modified copy of the DataFrame with cleaned name fields.
        """
        original_non_null = series.notna().sum()
        cleaned_series = series.apply(self.clean_name)
        cleaned_non_null = cleaned_series.notna().sum()
        null_count = len(series) - cleaned_non_null

        logger.info(
            f"[{label}] Cleaned {original_non_null} entries → "
            f"{cleaned_non_null} valid, {null_count} null or uncleanable"
        )

        return cleaned_series

