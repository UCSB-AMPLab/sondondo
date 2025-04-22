import pandas as pd
import numpy as np

# Step 1: Read in original data
unique_conditions_df = pd.DataFrame(
    pd.read_csv("data/raw/bautismos.csv")["Condición"].dropna().unique(),
    columns=["Condición"]
)

# Lowercase everything
unique_conditions_df["Condición"] = unique_conditions_df["Condición"].astype(str).str.lower()

# Step 2: Create harmonized version
harmonized_conditions_df = unique_conditions_df.copy()

# Define keyword groups
type_conditions = [
    harmonized_conditions_df["Condición"].str.contains("hijo", na=False),
    harmonized_conditions_df["Condición"].str.contains("hija", na=False)
]
type_values = ["hijo", "hija"]

status_conditions = [
    harmonized_conditions_df["Condición"].str.contains("legítimo|legitimo", na=False),
    harmonized_conditions_df["Condición"].str.contains("legítima|legitima", na=False),
    harmonized_conditions_df["Condición"].str.contains("natural", na=False)
]
status_values = ["legítimo", "legítima", "natural"]

# Apply np.select and convert to Series
harmonized_type = pd.Series(np.select(type_conditions, type_values, default=""))
harmonized_status = pd.Series(np.select(status_conditions, status_values, default=""))

# Combine and clean
harmonized_conditions_df["Condición"] = (
    harmonized_type.str.strip() + " " + harmonized_status.str.strip()
).str.strip()

# Replace empty results with default
harmonized_conditions_df["Condición"] = harmonized_conditions_df["Condición"].replace("", "(other data)")

# Optional: save to CSV
harmonized_conditions_df.to_csv("data/testing/unique_condiciones_harmonized.csv", index=False)