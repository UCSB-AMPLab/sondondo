from pathlib import Path
from typing import List, Tuple, Union
import pandas as pd
from project_code.helpers.Preprocessing import PreprocessingDates
from datetime import datetime, timedelta
import calendar
import re
from project_code.helpers.LogerHandler import setup_logger

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
        self.logger = setup_logger("DatesExplorer")

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

        self.logger.info(f"Report saved to {filename_stem} with {len(valid_dates)} valid dates and {len(invalid_dates)} invalid dates")
        

class DateNormalizer:
    """
    A class to normalize a pandas Series of date values into a consistent YYYY-MM-DD format.

    Handles multiple date representations including:
      - ISO strings
      - Excel serial numbers
      - False dates (nonexistent calendar dates)
      - Partial dates
      - Roto/ilegible
      - remove brackets and quotes
    """
    def __init__(self, date_series: pd.Series) -> None:
        self.original_series = date_series
        self.normalized_series = pd.Series([None] * len(date_series), dtype=object)
        self.logger = setup_logger("DateNormalizer")
        self.logger.info(f"Initialized DateNormalizer with {len(date_series)} entries.")

    def normalize(self) -> pd.Series:
        for idx, value in self.original_series.items():
            try:
                norm_value = self._normalize_single_value(value, idx)

                if norm_value is None:
                    self.logger.warning(f"Failed to normalize '{value}' at index {idx}.")
                elif norm_value != value and not self._is_valid_iso(value):
                    # Only log if value was changed AND original was not valid ISO
                    self.logger.info(f"Harmonized '{value}' to '{norm_value}' at index {idx}.")

                self.normalized_series[idx] = norm_value

            except Exception as e:
                self.logger.error(f"Error normalizing '{value}' at index {idx}: {e}")
                self.normalized_series[idx] = None

        return self.normalized_series

    def _normalize_single_value(self, value: str, idx) -> Union[str, None]:

        value = self._strip_all_brackets_and_quotes(value)

        if self._is_valid_iso(value):
            return value

        if self._is_excel_serial(value):
            return self._convert_excel_serial(value)

        if self._day_is_missing(value):
            return self._add_missing_day(value)
        
        if self._month_is_missing(value):
            return self._add_missing_month(value, self.original_series, idx)

        if self._is_false_date(value):
            return self._correct_false_date(value)

        return None

    def _is_valid_iso(self, value: str) -> bool:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except (ValueError, TypeError):
            return False

    def _is_excel_serial(self, value: str) -> bool:
        try:
            date2int = int(value)
            return 1922 <= date2int <= 9999
        except (ValueError, TypeError):
            return False

    def _convert_excel_serial(self, value: str) -> str:
        serial = int(value)
        epoch = datetime(1899, 12, 30)
        dt = epoch + timedelta(days=serial)
        return dt.strftime("%Y-%m-%d")

    def _is_false_date(self, value: str) -> bool:
        if not isinstance(value, str):
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return False
        except ValueError:
            return True

    def _correct_false_date(self, value: str) -> str:
        parts = value.split("-")
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        firstday = 1
        lastday = calendar.monthrange(year, month)[1]
        day = firstday if day == 0 else lastday
        return f"{year:04d}-{month:02d}-{day:02d}"

    def _day_is_missing(self, value:str) -> bool:
        if re.fullmatch(r"\d{4}-\d{2}-?", value) or re.fullmatch(r"\d{2}/\d{4}", value):
            return True
        return False

    def _add_missing_day(self, value: str) -> Union[str, None]:
        if re.fullmatch(r"\d{4}-\d{2}-?", value):
            self.logger.info(f"Completing missing day for: {value}")
            parts = value.split("-")
            if len(parts) >= 2:
                year, month = parts[0], parts[1]
                return f"{int(year):04d}-{int(month):02d}-01"
            
        if re.fullmatch(r"\d{2}/\d{4}", value):
            parts = value.split("/")
            return f"{int(parts[1]):04d}-{int(parts[0]):02d}-01"

        return None
        
    def _month_is_missing(self, value: str) -> bool:
        if re.fullmatch(r"\d{4}--\d{2}", value):
            return True
        return False
    
    def _add_missing_month(self, value: str, original_series: pd.Series, idx: int) -> Union[str, None]:
        parts = value.split("-")
        year_str, month_str, day_str = parts
        for j in range(idx - 1, -1, -1):
            candidate = original_series.iloc[j]
            if isinstance(candidate, str) and len(
                    candidate) >= 10 and "x" not in candidate and "..." not in candidate:
                ref_parts = candidate[:10].split("-")
                if len(ref_parts) != 3:
                    continue
                ref_month = ref_parts[1]
                return f"{year_str}-{ref_month}-{day_str}"


    def _is_partial_date(self, value: str) -> bool:
        return isinstance(value, str) and any(keyword in value for keyword in ["x", "xx", "...", "..", "/", "roto",
                                                                               "ilegible","primeros",
                                                                                          "a los dias"])


    def _complete_partial_date(self, value: str, original_series: pd.Series, idx: int) -> Union[str, None]:
        self.logger.info(f"Completing partial date for: {value}")
        # 1. Missing day (e.g., '1834-10-' or '1834-10')
        if re.fullmatch(r"\d{4}-\d{2}-?", value):
            self.logger.info(f"Completing missing day for: {value}")
            parts = value.split("-")
            if len(parts) >= 2:
                year, month = parts[0], parts[1]
                return f"{int(year):04d}-{int(month):02d}-01"

        # 2. Missing month
        if re.fullmatch(r"\d{4}-\D+-\d{2}", value):
            parts = value.split("-")
            year_str, month_str, day_str = parts
            for j in range(idx - 1, -1, -1):
                candidate = original_series.iloc[j]
                if isinstance(candidate, str) and len(
                        candidate) >= 10 and "x" not in candidate and "..." not in candidate:
                    ref_parts = candidate[:10].split("-")
                    if len(ref_parts) != 3:
                        continue
                    ref_month = ref_parts[1]
                    return f"{year_str}-{ref_month}-{day_str}"


        # 3. Missing year
        if (("x" in value[:4]) or ("." in value[:4])) and re.match(r".+-\d{2}-\d{2}", value):
            parts = value.split("-")
            year_str, month_str, day_str = parts
            for j in range(idx - 1, -1, -1):
                candidate = original_series.iloc[j]
                if isinstance(candidate, str) and len(
                        candidate) >= 10 and "x" not in candidate and "..." not in candidate:
                    ref_parts = candidate[:10].split("-")
                    if len(ref_parts) != 3:
                        continue
                    return f"{ref_parts[0]}-{month_str}-{day_str}"

        # 4. Wrong format
        if re.fullmatch(r"\d{2}/\d{4}", value):
            parts = value.split("/")
            return f"{int(parts[1]):04d}-{int(parts[0]):02d}-01"
        
        return None

    def _strip_all_brackets_and_quotes(self, value: str) -> str:
        """
        Remove all characters except digits, dashes, and x (lowercase only)
        """
        self.logger.info(f"Stripping brackets and quotes from: {value}")
        if not isinstance(value, str):
            return value
        value = re.sub(r'[^0-9\/\-]', '', value)
        value = value.lower()
        self.logger.info(f"Stripped value: {value}")
        return value.strip()


class AgeInferrer:
    def __init__(self, date_series: pd.Series) -> None:
        self.date_series = pd.to_datetime(date_series)
        self.logger = setup_logger("AgeInferrer")

    def parse_birth_age_to_timedelta(self, text: str) -> timedelta | None:
        t = text.lower().strip()
        t = re.sub(r'^["“”\'«]+|["“”\'»]+$', '', t)

        if t == "del día":
            return timedelta(days=0)

        m = re.match(r"(\d+)\s*mes(?:es)?\s*y\s*medio", t)
        if m:
            months = int(m.group(1))
            return timedelta(days=months * 30 + 15)

        m2 = re.fullmatch(
            r"(?:(\d+)\s*a[nñ]os?)?\s*"
            r"(?:(\d+)\s*mes(?:es)?)?"
            r"(?:\s*y\s*(\d+)\s*d[ií]as?)?",
            t
        )
        if m2:
            years = int(m2.group(1)) if m2.group(1) else 0
            months = int(m2.group(2)) if m2.group(2) else 0
            days = int(m2.group(3)) if m2.group(3) else 0
            return timedelta(days=years * 365 + months * 30 + days)

        # Pattern 3: "8 dias", "4 meses", "1 año"
        if re.search(r"d[ií]as?", t):
            m = re.search(r"(\d+)", t)
            if m:
                return timedelta(days=int(m.group(1)))
        if "mes" in t:
            m = re.search(r"(\d+)", t)
            if m:
                num = int(m.group(1))
                return timedelta(days=num * 30)
        if "año" in t or "ano" in t:
            m = re.search(r"(\d+)", t)
            if m:
                num = int(m.group(1))
                return timedelta(days=num * 365)

        return None

    def infer_birthdate(self, idx: int, age_desc: str) -> str | None:
        bapt = self.date_series.loc[idx]
        if pd.isna(bapt):
            return None

        delta = self.parse_birth_age_to_timedelta(age_desc)
        if delta is None:
            return None

        return (bapt - delta).strftime("%Y-%m-%d")

    def _is_iso_date(self, val: str) -> bool:
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return True
        except:
            return False

    def infer_all(self, age_series: pd.Series) -> pd.Series:
        results = []
        for idx, val in age_series.items():
            if isinstance(val, str) and any(
                    k in val.lower() for k in ["dia", "mes", "año", "ano", "medio", "días", "día"]):
                try:
                    result = self.infer_birthdate(idx, val) # type: ignore

                    if result is not None:
                        self.logger.info(
                            f"[AgeInferrer] Inferred birthdate at index {idx}: '{result}' from age='{val}' and baptism_date='{self.date_series.iloc[idx]}'" # type: ignore
                        )
                    else:
                        self.logger.warning(
                            f"[AgeInferrer] Failed to infer birthdate at index {idx} from age='{val}' and baptism_date='{self.date_series.loc[idx]}'" # type: ignore
                        )
                except Exception as e:
                    self.logger.error(
                        f"[AgeInferrer] Error inferring birthdate at index {idx} with value '{val}': {e}"
                    )
                    result = val
            else:
                if isinstance(val, str) and self._is_iso_date(val):
                    result = val
                else:
                    result = val
            results.append(result)
        return pd.Series(results, index=age_series.index, dtype="object")










