import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple, List, Union
from helpers.Preprocessing import PreprocessingDates
import logging

logging.basicConfig(level=logging.INFO, filename="logs/dates_explorer.log")
logger = logging.getLogger(__name__)


class DatesExplorer:
    """A class for exploring and validating date columns in a DataFrame."""
    
    def __init__(self, source_dataframe: pd.DataFrame, df_name: str) -> None:
        """
        Initialize the DatesExplorer with a source DataFrame.
        
        Args:
            source_dataframe: The DataFrame containing the date columns to explore
        """
        self.source_dataframe = source_dataframe
        self.df_name = df_name

    def report_column_dates(
        self,
        column_name: str,
        date_format: str = "%Y-%m-%d",
        save_report: bool = False,
        only_invalid_dates: bool = False,
        report_dir: Path = Path(__file__).parent.parent.parent / "reports",
        cleaned: bool = False,
        standardized: bool = False,

    ) -> Tuple[List[str], List[str]]:
        """
        Evaluate the values of a column, check if they are dates and return a report of valid and invalid dates.

        Args:
            column_name: The name of the column to evaluate
            date_format: The format of the dates in the column (default: "%Y-%m-%d")
            save_report: Whether to save the report to a file (default: False)
            only_invalid_dates: Whether to only save invalid dates in the report (default: False)

        Returns:
            Tuple[List[str], List[str]]: A tuple containing lists of valid and invalid dates

        Raises:
            KeyError: If the specified column does not exist in the DataFrame
            ValueError: If there are type errors in the date parsing
        """
        if column_name not in self.source_dataframe.columns:
            raise KeyError(f"Column '{column_name}' not found in DataFrame")

        valid_dates = []
        invalid_dates = []

        column_values = self.source_dataframe[column_name].dropna()
        if cleaned:
            column_values = PreprocessingDates(column_values).clean_date_strings()
        if standardized:
            column_values = PreprocessingDates(column_values).standardize_date_strings()

        for value in column_values:
            try:
                datetime.strptime(str(value), date_format)
                valid_dates.append(str(value))
            except ValueError:
                invalid_dates.append(str(value))
            except TypeError as e:
                raise ValueError(f"Type error for value '{value}': {str(e)}")

        if save_report:
            report_dir.mkdir(parents=True, exist_ok=True)
            self._save_report(
                valid_dates,
                invalid_dates,
                report_dir / f"{column_name}_report.txt",
                only_invalid_dates
            )

        return valid_dates, invalid_dates

    def _save_report(
        self,
        valid_dates: List[str],
        invalid_dates: List[str],
        filename: Path,
        only_invalid_dates: bool = False
    ) -> None:
        """
        Save the report of valid and invalid dates to a file.

        Args:
            valid_dates: List of valid dates
            invalid_dates: List of invalid dates
            filename: Path where to save the report
            only_invalid_dates: Whether to only save invalid dates
        """
        filepath = filename.parent
        filename_stem = filename.stem

        report_date = datetime.now().strftime("%Y-%m-%d")
        valid_dates_filename = f"{self.df_name}_{filename_stem}_valid_dates.txt"
        invalid_dates_filename = f"{self.df_name}_{filename_stem}_invalid_dates.txt"

        if not only_invalid_dates:
            with open(Path(filepath, valid_dates_filename), "w") as f:
                f.write(f"Report Date: {report_date}\n")
                f.write(f"Valid Dates: {len(valid_dates)}\n")
                f.write("\n".join(valid_dates))

        with open(Path(filepath, invalid_dates_filename), "w") as f:
            f.write(f"Report Date: {report_date}\n")
            f.write(f"Invalid Dates: {len(invalid_dates)}\n")
            f.write("\n".join(invalid_dates))

        logger.info(f"Report saved to {filename_stem} with {len(valid_dates)} valid dates and {len(invalid_dates)} invalid dates")
        

class DateNormalizer:
    def __init__(self, date_series: pd.Series) -> None:
        self.original_series = date_series
        self.normalized_series = pd.Series([None] * len(date_series), dtype=object)

    def normalize(self) -> pd.Series:
        for idx, value in self.original_series.items():
            self.normalized_series[idx] = self._normalize_single_value(value)
        return self.normalized_series

    def _normalize_single_value(self, value: str) -> str | None:
        if self._is_valid_iso(value):
            return value

        if self._is_excel_serial(value):
            return self._convert_excel_serial(value)

        if self._is_false_date(value):
            return self._correct_false_date(value)

        if self._is_partial_date(value):
            return self._complete_partial_date(value)

        if self._is_roto_or_ilegible(value):
            return self._resolve_roto(value)

        return None

    def _is_valid_iso(self, value: str) -> bool:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def _is_excel_serial(self, value: str) -> bool:
        try:
            date2int = int(value)
            return 1922 <= date2int <= 9999 # Excel serial numbers start from 1922 to avoid conflicts with real years
        except ValueError:
            return False

    def _convert_excel_serial(self, value: str) -> str:
        date2int = int(value)
        excel_epoch = datetime(1899, 12, 30)
        result = excel_epoch + timedelta(days=date2int)
        return result.strftime("%Y-%m-%d")
        


class AgeInferrer:
    """A class to infer the age of a person from a date of birth"""

    def __init__(self, date_series: pd.Series) -> None:
        self.date_series = date_series

