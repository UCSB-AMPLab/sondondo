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

    def clean_date_strings(self) -> pd.Series:
        """
        Clean the date strings by replacing all `/` characters with `-` and removing all non-numeric characters (except for the `-` character).
        """
        return self.date_series.str.replace("/", "-").str.replace(r"[^0-9\-]", "", regex=True).str.strip()

    def reverse_date_string(self, date_string: str) -> str:
        """
        Reverse the date string from "%d-%m-%Y" to "%Y-%m-%d".
        """

        if not isinstance(date_string, str):
            return date_string

        pattern = r"(\d{2})-(\d{2})-(\d{4})"
        match = re.match(pattern, date_string)
        if match:
            day, month, year = match.groups()
            try:
                if not (1 <= int(month) <= 12 and 1 <= int(day) <= 31):
                    return date_string
                return f"{year}-{month}-{day}"
            except ValueError:
                return date_string

        return date_string

    def standardize_date_strings(self) -> pd.Series:
        """
        Standardize the date strings from "%d-%m-%Y" to "%Y-%m-%d".
        """
        
        cleaned_dates = self.clean_date_strings()
        standardized_dates = cleaned_dates.apply(self.reverse_date_string)
        return standardized_dates


        
        
        
        