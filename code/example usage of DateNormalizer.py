import pandas as pd
from DateNormalizer import DateNormalizer, AgeInferrer
from pathlib import Path
"""
1.example: Normalize dates and birth_dates in Bautismos
"""
BASE_DIR = Path(__file__).resolve().parent.parent.parent
bautismos_path = BASE_DIR/"data"/"raw"/"bautismos.csv"

df = pd.read_csv(bautismos_path)

date_series = df["Fecha aaaa-mm-dd"]

normalizer = DateNormalizer(date_series)
normalized_dates = normalizer.normalize()
df["Fecha aaaa-mm-dd"] = normalized_dates

birth_date_series = df["Fecha Nacimiento aaaa-mm-dd / número de días, meses, etc."]
inferrer = AgeInferrer(df["Fecha aaaa-mm-dd"])
birth_date_cleaned = inferrer.infer_all(birth_date_series)





