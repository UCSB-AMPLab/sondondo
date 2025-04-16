import pandas as pd
from pathlib import Path
from datetime import datetime

class DatesExplorer:
    def __init__(self, source_dataframe):
        self.source_dataframe = source_dataframe

    def report_column_dates(self, column_name, date_format: str = "%Y-%m-%d", save_report: bool = False, only_invalid_dates: bool = False):
        """
        Evaluate the values of a column, check if they are dates and return a report of valid and invalid dates.

        Args:
            df (pd.DataFrame): The DataFrame containing the column to evaluate.
            column_name (str): The name of the column to evaluate.
            date_format (str): The format of the dates in the column.
            save_report (bool): Whether to save the report to a file.
        """
        valid_dates = []
        invalid_dates = []

        column_values = self.source_dataframe[column_name].dropna()

        for value in column_values:
            try:
                datetime.strptime(value, date_format)
                valid_dates.append(value)
            except ValueError:
                invalid_dates.append(value)
            except TypeError:
                print(f"Type error for {value}")
                raise ValueError(f"Type error for {value}")

        if save_report:
            report_dir = Path(__file__).parent.parent.parent / "reports"
            report_dir.mkdir(parents=True, exist_ok=True)
            self.save_report(valid_dates, invalid_dates, report_dir / f"{column_name}_report.txt", only_invalid_dates)

        return valid_dates, invalid_dates

    def save_report(self, valid_dates, invalid_dates, filename: str, only_invalid_dates: bool = False):
        """
        Save the report of valid and invalid dates to a file.
        """

        filepath = Path(filename).parent
        filename = Path(filename).stem

        report_date = datetime.now().strftime("%Y-%m-%d")
        valid_dates_filename = f"{filename}_valid_dates_{report_date}.txt"
        invalid_dates_filename = f"{filename}_invalid_dates_{report_date}.txt"

        if not only_invalid_dates:
            with open(Path(filepath, valid_dates_filename), "w") as f:
                f.write(f"Valid Dates: {len(valid_dates)}\n")
                for date in valid_dates:
                    f.write(f"{date}\n")

        with open(Path(filepath, invalid_dates_filename), "w") as f:
            f.write(f"Invalid Dates: {len(invalid_dates)}\n")
            for date in invalid_dates:
                f.write(f"{date}\n")

        print(f"Report saved to {filename}")
        
        