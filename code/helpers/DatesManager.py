import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Optional
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
        report_dir: Path = Path(__file__).parent.parent.parent / "reports"
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
        
