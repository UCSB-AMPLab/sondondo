import re
from typing import Union
import pandas as pd

class PreprocessingDates:
    """
    A series of methods to clean and normalize date strings following some common patterns.
    """

    def __init__(self, date_series: Union[pd.Series, list[str]]) -> None:
        if isinstance(date_series, list):
            date_series = pd.Series(date_series)
        self.date_series = date_series

    def clean_date_strings(self, 
            placeholder_pattern: str = r'(?:x+|\.{3}|\[(?:roto|ilegible|borroso)(?::[^]]*)?]|n/a|Sin fecha|a los dias|-\[(?:roto|ilegible)])',
            replacement: str = "01") -> pd.Series:
        """
        Clean date strings by standardizing formats and handling various placeholder patterns.
        
        The function handles:
        - Forward slashes to hyphens conversion
        - Multiple placeholder patterns:
            * 'x', 'xx', 'xxx' etc.
            * '...'
            * '[roto]', '[roto: 01 al 21]'
            * '[ilegible]', '[ilegible: fecha]'
            * '[borroso]'
            * 'n/a'
            * 'Sin fecha'
            * 'a los dias'
            * '-[roto]', '-[ilegible]' (legacy format)
        - Removes non-numeric characters except hyphens
        - Strips trailing/leading hyphens and spaces
        
        Args:
            placeholder_pattern: Regex pattern for matching placeholder text
            replacement: String to replace placeholders with (default: "01")
            
        Returns:
            pd.Series: Cleaned date strings
        """
        
        cleaned = (self.date_series
                  .fillna("")
                  .str.lower()
                  .str.strip()
                 )
        
        cleaned = cleaned.str.replace("/", "-")
        cleaned = cleaned.str.replace(placeholder_pattern, replacement, regex=True)
        cleaned = cleaned.str.replace(r"[^0-9\-]", "", regex=True)
        cleaned = (cleaned
                  .str.replace(r"-+", "-", regex=True)
                  .str.strip("- ")
                 )
        
        cleaned = cleaned.replace("", pd.NA)
        
        return cleaned

    def standardize_date_strings(self) -> pd.Series:
        """
        Standardize the date strings from "%d-%m-%Y" to "%Y-%m-%d".
        """

        cleaned_dates = self.clean_date_strings()
        standardized_dates = cleaned_dates.apply(self._reverse_date_string)
        return standardized_dates


    def _reverse_date_string(self, date_string: str) -> str:
        """
        Reverse the date string from either "%d-%m-%Y" or "%m-%Y" to "%Y-%m-%d" or "%Y-%m" respectively.
        """
        if not isinstance(date_string, str):
            return date_string

        full_date_pattern = r"(\d{2})-(\d{2})-(\d{4})"
        partial_date_pattern = r"(\d{2})-(\d{4})"

        match = re.match(full_date_pattern, date_string)
        if match:
            day, month, year = match.groups()
            try:
                if not (1 <= int(month) <= 12 and 1 <= int(day) <= 31):
                    return date_string
                return f"{year}-{month}-{day}"
            except ValueError:
                return date_string

        match = re.match(partial_date_pattern, date_string)
        if match:
            month, year = match.groups()
            try:
                if not (1 <= int(month) <= 12):
                    return date_string
                return f"{year}-{month}"
            except ValueError:
                return date_string

        return date_string


class RecordIdGenerator:
    """
    Generates a unique ID record with the combination of columns
    "file" and "identifier" from a specified DataFrame.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def generate_id(self) -> pd.Series:
        """
        Generate the unique ID by combining "file" and "identifier" columns.
        """
        if "file" not in self.df.columns or "identifier" not in self.df.columns:
            raise ValueError("DataFrame must contain 'file' and 'identifier' columns.")

        raw_id = self.df["file"].astype(str) + "_" + self.df["identifier"].astype(str)
        return raw_id.apply(lambda x: x.replace(" ", "_").replace("/", "_").replace("\\", "_"))
    

