import re
import pandas as pd
from project_code.helpers.LogerHandler import setup_logger


class NamesManager:
    def __init__(self):
        # Add known filler terms or other annotation patterns here if needed
        self.filler_terms = {"n/a", "na"}
        self.logger = setup_logger("NamesManager")

    def clean_name(self, name: str) -> str | None:
        """
        Cleans a name string by:
        - Lowercasing
        - Removing non-alphabetic characters (keeps spaces and accented letters)
        - Removing known filler terms
        - Removing extra spaces
        """
        if not isinstance(name, str):
            return None
        
        name = name.lower()
        name = re.sub(r"[^a-zñáéíóúü\s]", "", name)         # keep only letters and spaces
        name = re.sub(r"\b(?:n/?a|na)\b", "", name)         # remove known filler terms
        name = re.sub(r"\s+", " ", name).strip()            # removes double/extra spaces

        return name if name else None
    
    def clean_series(self, series: pd.Series, label: str = "") -> pd.Series:
        """
        Applies clean_name to a pandas Series.
        Logs the number of valid and null results.
        """
        original_non_null = series.notna().sum()            # count non-null values
        cleaned_series = series.apply(self.clean_name)      # apply name cleaning function
        cleaned_non_null = cleaned_series.notna().sum()     # count cleaned non-null values

        null_count = len(series) - cleaned_non_null         # number of null/uncleanable values

        self.logger.info(
            f"[{label}] Cleaned {original_non_null} entries → "
            f"{cleaned_non_null} valid, {null_count} null or uncleanable"
        )

        return cleaned_series

