import pandas as pd
from utils.LoggerHandler import setup_logger
from actions.normalizers import DatesNormalizer
from typing import Union
from datetime import datetime, timedelta
import re
import unicodedata

class AgeInferrer:
    def __init__(self, date_series: pd.Series) -> None:
        self.date_series = pd.to_datetime(date_series, errors='coerce')
        self.logger = setup_logger("AgeInferrer")

    def parse_birth_age_to_timedelta(self, text: str) -> Union[timedelta, None]:
        
        if not isinstance(text, str) or text.strip() == "":
            return None

        t = self._normalize_text(text)

        if t == "del dia":
            return timedelta(days=0)
        
        # Pattern 1: "80 a 90 años"
        range_match = re.search(r"(\d+)\s+a\s+(\d+)\s*(anos?|mes(?:es)?|dias?)?", t)
        if range_match:
            lower = int(range_match.group(1))
            upper = int(range_match.group(2))
            unit = range_match.group(3) if range_match.group(3) else "anos"

            avg = (lower + upper) // 2

            if "dia" in unit:
                return timedelta(days=avg)
            elif "mes" in unit:
                return timedelta(days=avg * 30)
            elif "ano" in unit:
                return timedelta(days=avg * 365)

        # Pattern 1: "3 meses y medio"
        m = re.search(r"(\d+)\s*mes(?:es)?\s*y\s*medio", t)
        if m:
            months = int(m.group(1))
            return timedelta(days=months * 30 + 15)

        # Pattern 2: Combined years/months/days e.g. "1 año 2 meses 10 dias"
        m2 = re.fullmatch(
            r"(?:(\d+)\s*anos?)?\s*(?:y\s*)?"
            r"(?:(\d+)\s*mes(?:es)?)?\s*(?:y\s*)?"
            r"(?:(\d+)\s*dias?)?",
            t
        )
        if m2:
            years = int(m2.group(1)) if m2.group(1) else 0
            months = int(m2.group(2)) if m2.group(2) else 0
            days = int(m2.group(3)) if m2.group(3) else 0
            return timedelta(days=years * 365 + months * 30 + days)

        # Pattern 2.5: "X meses y Y días"
        m25 = re.fullmatch(r"(\d+)\s*mes(?:es)?\s*y\s*(\d+)\s*dias?", t)
        if m25:
            months = int(m25.group(1))
            days = int(m25.group(2))
            return timedelta(days=months * 30 + days)

        # Pattern 3: "8 dias", "29 ds.", "4 meses", "1 año"
        m = re.search(r"(\d+)\s*(dias?|ds(?:\s+dias?)?|mes(?:es)?|ano(?:s)?)", t)
        if m:
            num = int(m.group(1))
            unit = m.group(2)
            if "dia" in unit:
                return timedelta(days=num)
            elif "ds" in unit:
                return timedelta(days=num)
            elif "mes" in unit:
                return timedelta(days=num * 30)
            elif "ano" in unit:
                return timedelta(days=num * 365)

        # Pattern 4: "X semana(s)"
        m = re.search(r"(\d+)\s*(semana(?:s)?)", t)
        if m:
            num = int(m.group(1))
            return timedelta(days=num * 7)
        
        # Pattern 5: "p[aá]rvul[oa]"
        m = re.search(r".*[Pp][aá]rvul[oa]", t)
        if m:
            return timedelta(days=30)

        self.logger.warning(f"[AgeInferrer] Unrecognized age format: '{text}' -Normalized '{t}'")
        return None

    def infer_birthdate(self, idx: int, age_desc: str) -> Union[str, None]:
        event = self.date_series.loc[idx]
        if pd.isna(event):
            return None

        m = re.search(r"\d{4}-\d{2}-\d{2}", age_desc)
        if m:
            return datetime.strptime(m.group(0), "%Y-%m-%d").strftime("%Y-%m-%d")

        delta = self.parse_birth_age_to_timedelta(age_desc)
        if delta is None:
            return None

        return (event - delta).strftime("%Y-%m-%d")

    def _is_iso_date(self, val: str) -> bool:
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return True
        except:
            return False

    def _normalize_text(self, val: str) -> str:
        
        # Stripping accents and special characters
        text = unicodedata.normalize('NFD', val)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')

        # Lower case and strip punctuation
        text = re.sub(r"[^\w\s]", "", text.lower())

        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()

        # Handle special cases
        oforzero = r"(\d)(o)"
        replacement = r"\g<1>0"

        if re.search(oforzero, text):
            text = re.sub(oforzero, replacement, text)

        return text

    def infer_all(self, age_series: pd.Series) -> pd.Series:
        results = []

        datenormalizer = DatesNormalizer.SimpleNormalizer()
        for idx, val in age_series.items():

            result = None
            
            if isinstance(val, str) and self._is_iso_date(val):
                result = val
                self.logger.debug(
                    f"[AgeInferrer] Found ISO date at index {idx}: '{result}'"
                )

            elif isinstance(val, str) and val.strip():

                try:
                    
                    result = datenormalizer.normalize(val)

                    if result is None:
                        result = self.infer_birthdate(idx, val) # type: ignore

                    if result is not None:
                        self.logger.info(
                            f"[AgeInferrer] Inferred birthdate at index {idx}: '{result}' from age='{val}' and event_date='{self.date_series.iloc[idx]}'" # type: ignore
                        )
                    else:
                        self.logger.warning(
                            f"[AgeInferrer] Failed to infer birthdate at index {idx} from age='{val}' and event_date='{self.date_series.loc[idx]}'" # type: ignore
                        )
                except Exception as e:
                    self.logger.error(
                        f"[AgeInferrer] Error inferring birthdate at index {idx} with value '{val}': {e}"
                    )
                    
            else:
                result = val
            
            results.append(result)
        
        return pd.Series(results, index=age_series.index, dtype="object")

