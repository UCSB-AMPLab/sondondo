import re
from typing import Union
import unicodedata
import numpy as np
import pandas as pd
from utils.LoggerHandler import setup_logger


class NamesNormalizer:
    SIC_ILEGIBLE_PATTERN = re.compile(r"[\(\[\{]?\s*(sic|ilegible)\s*[\)\]\}]?", re.IGNORECASE)
    QUOTED_TEXT_PATTERN = re.compile(r'"([^"]+)"')
    COMMA_NAME_PATTERN = re.compile(r"^([^\n,]+),\s(.+)$")
    NON_ALPHA_PATTERN = re.compile(r"[^a-zñáéíóúü\s]")
    EXTRA_SPACES_PATTERN = re.compile(r"\s+")
    FILLER_TERMS_PATTERN = re.compile(r"\b(?:n/?a|na)\b", re.IGNORECASE)
    ROTO_PATTERN = re.compile(r"\b(?:roto|rota)\b", re.IGNORECASE)
    DON_PATTERN = re.compile(r"\b(?:don|doña)\s\b", re.IGNORECASE)

    def __init__(self):
        self.logger = setup_logger("NamesNormalizer")

    def clean_name(self, name: str) -> Union[str, float]:
        if not isinstance(name, str):
            return np.nan

        original_name = name
        name = unicodedata.normalize("NFKC", name)

        name = self.SIC_ILEGIBLE_PATTERN.sub("", name)
        name = re.sub(r"N\.", "", name)
        name = self.COMMA_NAME_PATTERN.sub(r"\2 \1", name)
        name = self.QUOTED_TEXT_PATTERN.sub("", name)
        
        name = name.lower()
        name = self.EXTRA_SPACES_PATTERN.sub(" ", name).strip()
        name = self.NON_ALPHA_PATTERN.sub("", name)
        name = self.FILLER_TERMS_PATTERN.sub("", name)
        name = self.ROTO_PATTERN.sub("", name)
        name = self.DON_PATTERN.sub("", name)
        name = self.EXTRA_SPACES_PATTERN.sub(" ", name).strip()

        self.logger.info(f"Original name: {original_name} → Cleaned: {name}")

        return name if name else np.nan

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

