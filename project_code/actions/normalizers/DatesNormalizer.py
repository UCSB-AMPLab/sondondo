from typing import Union
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import calendar
import re
from utils.LoggerHandler import setup_logger

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

    def _normalize_single_value(self, value: str, idx) -> Union[str, float, None]:

        if pd.isna(value):
            return np.nan

        if self._is_roto_or_ilegible(value):
            return self._resolve_roto(value)

        value = self._strip_all_brackets_and_quotes(value)

        if self._is_valid_iso(value):
            return value
        
        if self._is_inverted(value):
            return self._convert_inverted_date(value)

        if self._day_is_missing(value):
            return self._add_missing_day(value)

        if self._month_is_missing(value):
            return self._add_missing_month(value, self.original_series, idx)

        if self._year_is_missing(value):
            return self._add_missing_year(value, self.original_series, idx)

        if self._is_excel_serial(value):
            return self._convert_excel_serial(value)

        if self._is_false_date(value):
            return self._correct_false_date(value)

        return None

    def _is_valid_iso(self, value: str) -> bool:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except (ValueError, TypeError):
            return False

    def _is_inverted(self, value: str) -> bool:
        try:
            datetime.strptime(value, "%d-%m-%Y")
            return True
        except (ValueError, TypeError):
            return False
        
    def _convert_inverted_date(self, value: str) -> Union[str, None]:
        try:
            dt = datetime.strptime(value, "%d-%m-%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            self.logger.error(f"Invalid inverted date format: {value}")
            return None

    def _is_excel_serial(self, value: str) -> bool:
        try:
            date2int = int(value)
            return 1922 <= date2int <= 9999
        except (ValueError, TypeError):
            return False

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
                value_clean = f"{int(year):04d}-{int(month):02d}-01"
                if self._is_valid_iso(value_clean):
                    return value_clean
                self.logger.error(f"Invalid date after completing missing day: {value_clean}")
                return None

        if re.fullmatch(r"\d{2}/\d{4}", value):
            parts = value.split("/")
            value_clean = f"{int(parts[1]):04d}-{int(parts[0]):02d}-01"
            if self._is_valid_iso(value_clean):
                return value_clean
            self.logger.error(f"Invalid date after completing missing day: {value_clean}")

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
                self.logger.info(f"Completing missing month for: {value} with {candidate}")
                ref_parts = candidate[:10].split("-")
                if len(ref_parts) != 3:
                    continue
                ref_month = ref_parts[1]
                value_clean = f"{year_str}-{ref_month}-{day_str}"
                return value_clean if self._is_valid_iso(value_clean) else self.logger.error(
                    f"Invalid date after completing missing month: {value_clean}")

    def _year_is_missing(self, value: str) -> bool:
        if re.fullmatch(r"\d{2,3}-\d{2}-\d{2}", value):
            return True
        return False

    def _add_missing_year(self, value: str, original_series: pd.Series, idx: int) -> Union[str, None]:
        parts = value.split("-")
        year_str, month_str, day_str = parts
        for j in range(idx - 1, -1, -1):
            candidate = original_series.iloc[j]
            if isinstance(candidate, str) and len(
                    candidate) >= 10 and "x" not in candidate and "..." not in candidate:
                self.logger.info(f"Completing missing year for: {value} with {candidate}")
                ref_parts = candidate[:10].split("-")
                if len(ref_parts) != 3:
                    continue
                value_clean = f"{ref_parts[0]}-{month_str}-{day_str}"
                return value_clean if self._is_valid_iso(value_clean) else self.logger.error(
                    f"Invalid date after completing missing year: {value_clean}")

    def _convert_excel_serial(self, value: str) -> Union[str, None]:
        serial = int(value)
        epoch = datetime(1899, 12, 30)
        dt = epoch + timedelta(days=serial)
        value_clean = dt.strftime("%Y-%m-%d")
        if self._is_valid_iso(value_clean):
            return value_clean

        self.logger.error(f"Invalid date after converting Excel serial: {value_clean}")
        return None

    def _is_false_date(self, value: str) -> bool:
        if not isinstance(value, str):
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return False
        except ValueError:
            return True

    def _correct_false_date(self, value: str) -> Union[str, None]:
        parts = value.split("-")
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        firstday = 1
        lastday = calendar.monthrange(year, month)[1]
        day = firstday if day == 0 else lastday
        value_clean = f"{year:04d}-{month:02d}-{day:02d}"
        return value_clean if self._is_valid_iso(value_clean) else self.logger.error(
            f"Invalid date after correcting false date: {value_clean}"
        )

    def _strip_all_brackets_and_quotes(self, value: str) -> str:
        """
        Remove all characters except digits, dashes, slashes, and lowercase 'x'.
+       Both dashes and slashes are preserved because date formats may use either as separators (e.g., 'YYYY-MM-DD' or 'MM/DD/YYYY').
        """
        if not isinstance(value, str):
            return value
        value = re.sub(r'[^0-9\/\-]', '', value)
        value = value.lower()
        return value.strip()

    def _is_roto_or_ilegible(self, value: str) -> bool:
        return isinstance(value, str) and any(keyword in value for keyword in ["roto", "ilegible"])

    def _resolve_roto(self,value: str) -> Union[str, None]:
        
        value_clean = re.sub(r'[\[\]"\'?]', '', value)
        m = re.search(r"roto:\s*(?:del\s*)?(\d{1,2})\s*(?:al|o)\s*(\d{1,2})", value_clean)
        if m:
            start_day = int(m.group(1))
            end_day = int(m.group(2))
            avg_day = (start_day + end_day) // 2
            prefix = value.split('roto',1)[0].rstrip('-')
            parts = prefix.split('-')
            if len(parts) >= 2:
                year, month = parts[0], parts[1]
                value_clean = f"{int(year):04d}-{int(month):02d}-{avg_day:02d}"
                if self._is_valid_iso(value_clean):
                    return value_clean
                self.logger.error(
                    f"Invalid date after resolving roto: {value_clean}")

        if re.fullmatch(r"\d{4}-\d{2}-(xx|\.{2,3}|\D+)", value_clean):
            parts = value_clean.split("-")
            value_clean = f"{int(parts[0]):04d}-{int(parts[1]):02d}-01"
            if self._is_valid_iso(value_clean):
                return value_clean
            else:
                self.logger.error(
                    f"Invalid date after resolving roto: {value_clean}")
        
        if self._is_valid_iso(value_clean):
            return value_clean
        self.logger.error(
            f"Invalid date after resolving roto: {value_clean}")


class SimpleNormalizer:
    """
    This normalizer try to normalize date strings into a ISO 8601 format.
    It doesn't include all methods from DateNormalizer
    """

    def __init__(self) -> None:
        self.logger = setup_logger("DateNormalizer")

    def normalize(self, value: str) -> Union[str, float, None]:
        """
        Normalize a single date string into ISO 8601 format.
        """
        return self._normalize_single_value(value)


    def _normalize_single_value(self, value: str) -> Union[str, float, None]:
        """
        Normalize a single value into a specific format.
        """
        # Implement normalization logic here
        if pd.isna(value):
            return np.nan

        if self._is_roto_or_ilegible(value):
            return self._resolve_roto(value)

        value = self._strip_all_brackets_and_quotes(value)

        if self._is_valid_iso(value):
            return value
        
        if self._is_inverted(value):
            return self._convert_inverted_date(value)
        
        if self._day_is_missing(value):
            return self._add_missing_day(value)
        
        if self._is_excel_serial(value):
            return self._convert_excel_serial(value)

        if self._is_false_date(value):
            try:
                return self._correct_false_date(value)
            except Exception as e:
                self.logger.error(f"Error correcting false date {value}: {e}")
                return None

        return None

    def _is_valid_iso(self, value: str) -> bool:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except (ValueError, TypeError):
            return False
        
    def _is_inverted(self, value: str) -> bool:
        try:
            datetime.strptime(value, "%d-%m-%Y")
            return True
        except (ValueError, TypeError):
            return False
        
    def _convert_inverted_date(self, value: str) -> Union[str, None]:
        try:
            dt = datetime.strptime(value, "%d-%m-%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            self.logger.error(f"Invalid inverted date format: {value}")
            return None

    def _is_excel_serial(self, value: str) -> bool:
        try:
            date2int = int(value)
            return 1922 <= date2int <= 9999
        except (ValueError, TypeError):
            return False
        
    def _convert_excel_serial(self, value: str) -> Union[str, None]:
        serial = int(value)
        epoch = datetime(1899, 12, 30)
        dt = epoch + timedelta(days=serial)
        value_clean = dt.strftime("%Y-%m-%d")
        if self._is_valid_iso(value_clean):
            return value_clean

        self.logger.error(f"Invalid date after converting Excel serial: {value_clean}")
        return None

    def _is_false_date(self, value: str) -> bool:
        if not isinstance(value, str):
            return False
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return False
        except ValueError:
            return True

    def _correct_false_date(self, value: str) -> Union[str, None]:
        parts = value.split("-")
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        firstday = 1
        lastday = calendar.monthrange(year, month)[1]
        day = firstday if day == 0 else lastday
        value_clean = f"{year:04d}-{month:02d}-{day:02d}"
        return value_clean if self._is_valid_iso(value_clean) else self.logger.error(
            f"Invalid date after correcting false date: {value_clean}"
        )

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
                value_clean = f"{int(year):04d}-{int(month):02d}-01"
                if self._is_valid_iso(value_clean):
                    return value_clean
                self.logger.error(f"Invalid date after completing missing day: {value_clean}")
                return None

        if re.fullmatch(r"\d{2}/\d{4}", value):
            parts = value.split("/")
            value_clean = f"{int(parts[1]):04d}-{int(parts[0]):02d}-01"
            if self._is_valid_iso(value_clean):
                return value_clean
            self.logger.error(f"Invalid date after completing missing day: {value_clean}")

        return None

    def _month_is_missing(self, value: str) -> bool:
        if re.fullmatch(r"\d{4}--\d{2}", value):
            return True
        return False
    
    def _is_roto_or_ilegible(self, value: str) -> bool:
        return isinstance(value, str) and any(keyword in value for keyword in ["roto", "ilegible"])

    def _resolve_roto(self,value: str) -> Union[str, None]:
        
        value_clean = re.sub(r'[\[\]"\'?]', '', value)
        m = re.search(r"roto:\s*(?:del\s*)?(\d{1,2})\s*(?:al|o)\s*(\d{1,2})", value_clean)
        if m:
            start_day = int(m.group(1))
            end_day = int(m.group(2))
            avg_day = (start_day + end_day) // 2
            prefix = value.split('roto',1)[0].rstrip('-')
            parts = prefix.split('-')
            if len(parts) >= 2:
                year, month = parts[0], parts[1]
                value_clean = f"{int(year):04d}-{int(month):02d}-{avg_day:02d}"
                if self._is_valid_iso(value_clean):
                    return value_clean
                self.logger.error(
                    f"Invalid date after resolving roto: {value_clean}")

        if re.fullmatch(r"\d{4}-\d{2}-(xx|\.{2,3}|\D+)", value_clean):
            parts = value_clean.split("-")
            value_clean = f"{int(parts[0]):04d}-{int(parts[1]):02d}-01"
            if self._is_valid_iso(value_clean):
                return value_clean
            else:
                self.logger.error(
                    f"Invalid date after resolving roto: {value_clean}")
        
        if self._is_valid_iso(value_clean):
            return value_clean
        self.logger.error(
            f"Invalid date after resolving roto: {value_clean}")
    
    def _strip_all_brackets_and_quotes(self, value: str) -> str:
        """
        Remove all characters except digits, dashes, slashes, and lowercase 'x'.
        Both dashes and slashes are preserved because date formats may use either as separators (e.g., 'YYYY-MM-DD' or 'MM/DD/YYYY').
        """
        if not isinstance(value, str):
            return value
        value = re.sub(r'[^0-9\/\-]', '', value)
        value = value.lower()
        return value.strip()
    
    