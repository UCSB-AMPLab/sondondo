import pandas as pd
from datetime import datetime, timedelta
import calendar
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs/date_normalizer.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        logger.info(f"Initialized DateNormalizer with {len(date_series)} entries.")

    def normalize(self) -> pd.Series:
        for idx, value in self.original_series.items():
            try:
                norm_value = self._normalize_single_value(value, idx)

                if norm_value is None:
                    logger.warning(f"Failed to normalize '{value}' at index {idx}.")
                elif norm_value != value and not self._is_valid_iso(value):
                    # Only log if value was changed AND original was not valid ISO
                    logger.info(f"Harmonized '{value}' to '{norm_value}' at index {idx}.")

                self.normalized_series[idx] = norm_value

            except Exception as e:
                logger.error(f"Error normalizing '{value}' at index {idx}: {e}")
                self.normalized_series[idx] = None

        return self.normalized_series

    def _normalize_single_value(self, value: str,idx: int):

        value = self._strip_all_brackets_and_quotes(value)

        if self._is_valid_iso(value):
            return value

        if self._is_excel_serial(value):
            return self._convert_excel_serial(value)

        if self._is_roto_or_ilegible(value):
            return self._resolve_roto(value)

        if self._is_partial_date(value):
            return self._complete_partial_date(value, self.original_series, idx)

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

    def _is_partial_date(self, value: str) -> bool:
        return isinstance(value, str) and any(keyword in value for keyword in ["x", "xx", "...", "..", "/", "roto",
                                                                               "ilegible","primeros",
                                                                                          "a los dias"])


    def _complete_partial_date(self, value: str, original_series: pd.Series, idx: int) -> str:
        # 1. Missing day
        if re.fullmatch(r"\d{4}-\d{2}-(xx|\.{2,3}|\D+)", value):
            parts = value.split("-")
            return f"{int(parts[0]):04d}-{int(parts[1]):02d}-01"

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

    def _strip_all_brackets_and_quotes(self, value: str) -> str:
        if not isinstance(value, str):
            return value
        return re.sub(r'[\[\]"\'?]', '', value)


    def _is_roto_or_ilegible(self, value: str) -> bool:
        return isinstance(value, str) and any(keyword in value for keyword in ["roto", "ilegible"])

    def _resolve_roto(self,value: str) -> str:
        m = re.search(r"roto:\s*(?:del\s*)?(\d{1,2})\s*(?:al|o)\s*(\d{1,2})", value)
        if m:
            start_day = int(m.group(1))
            end_day = int(m.group(2))
            avg_day = (start_day + end_day) // 2
            prefix = value.split('[')[0].rstrip('-')
            parts = prefix.split('-')
            if len(parts) >= 2:
                year, month = parts[0], parts[1]
                return f"{int(year):04d}-{int(month):02d}-{avg_day:02d}"
        return value

ageinferrer_logger = logging.getLogger("AgeInferrer")
ageinferrer_logger.setLevel(logging.INFO)

ageinferrer_handler = logging.FileHandler("logs/age_inferrer.log", mode='w', encoding='utf-8')
ageinferrer_handler.setLevel(logging.INFO)
ageinferrer_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ageinferrer_handler.setFormatter(ageinferrer_formatter)

if not ageinferrer_logger.handlers:
    ageinferrer_logger.addHandler(ageinferrer_handler)


ageinferrer_logger.propagate = False

if not ageinferrer_logger.handlers:
    ageinferrer_logger.addHandler(ageinferrer_handler)

class AgeInferrer:
    def __init__(self, date_series: pd.Series) -> None:
        self.date_series = pd.to_datetime(date_series)

    def parse_birth_age_to_timedelta(self, text: str) -> timedelta | None:
        t = text.lower().strip()

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
            num = int(re.search(r"(\d+)", t).group(1))
            return timedelta(days=num * 30)
        if "año" in t or "ano" in t:
            num = int(re.search(r"(\d+)", t).group(1))
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
                    result = self.infer_birthdate(idx, val)

                    if result is not None:
                        ageinferrer_logger.info(
                            f"[AgeInferrer] Inferred birthdate at index {idx}: '{result}' from age='{val}' and baptism_date='{self.date_series.loc[idx]}'"
                        )
                    else:
                        ageinferrer_logger.warning(
                            f"[AgeInferrer] Failed to infer birthdate at index {idx} from age='{val}' and baptism_date='{self.date_series.loc[idx]}'"
                        )
                except Exception as e:
                    ageinferrer_logger.error(
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










