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
        name = re.sub(r"\(.*?\)", "", name)             # remove parentheses content
        name = re.sub(r"\[.*?\]", "", name)             # remove bracketed content
        name = re.sub(r"[^a-zñáéíóúü\s]", "", name)      # keep only letters and spaces
        name = re.sub(r"\b(?:n/?a|na)\b", "", name)      # remove known filler terms
        name = re.sub(r"\s+", " ", name).strip()

        return name if name else None
    
    def clean_dataframe(self, df: pd.DataFrame, name_columns: list[str]) -> pd.DataFrame:
        """
        Cleans specified name-related columns in a pandas DataFrame.
        Returns a modified copy of the DataFrame with cleaned name fields.
        """
        df_clean = df.copy()

        for col in name_columns:
            if col in df_clean.columns:
                original = df_clean[col]
                cleaned = original.apply(self.clean_name)
                df_clean[col] = cleaned

                total_entries += len(cleaned)
                cleaned_entries += cleaned.notna().sum()

        null_entries = total_entries - cleaned_entries

        logger.info(
            f"Names cleaned in {filename_stem}: "
            f"{len(name_columns)} columns processed, "
            f"{cleaned_entries} cleaned entries, "
            f"{null_entries} null or uncleanable entries"
        )

        return df_clean


