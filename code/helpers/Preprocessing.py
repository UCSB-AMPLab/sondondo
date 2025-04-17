import re
import pandas as pd

class PreprocessingDates:
    """
    A series of methods to clean and normalize date strings following some common patterns.
    """

    def __init__(self, date_series: pd.Series | list[str]) -> None:
        self.date_series = date_series

    def clean_date_strings(self) -> pd.Series:
        """
        Clean the date strings by replacing all `/` characters with `-` and removing all non-numeric characters (except for the `-` character).
        """
        return self.date_series.str.replace("/", "-").str.replace(r"[^0-9\-]", "", regex=True).str.strip()

    def reverse_date_string(self, date_string: str) -> str:
        """
        Reverse the date string from "%d-%m-%Y" to "%Y-%m-%d".
        """

        pattern = r"(\d{2})-(\d{2})-(\d{4})"
        match = re.match(pattern, date_string)
        if match:
            day, month, year = match.groups()
            return f"{year}-{month}-{day}"
        else:
            return date_string

    def normalize_date_strings(self) -> pd.Series:
        """
        Normalize the date strings from "%d-%m-%Y" to "%Y-%m-%d".
        """
        
        cleaned_dates = self.clean_date_strings()
        normalized_dates = cleaned_dates.apply(self.reverse_date_string)
        return normalized_dates


        
        
        
        