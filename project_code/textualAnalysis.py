import pandas as pd

# 1) Load the CSV
csv_path = "project_code/helpers/missingConfig_with_unmapped.csv"
df = pd.read_csv(csv_path, encoding="utf-8")

# 2) Extract unique non-null values from "Condición_unmapped"
unique_vals = df["Condición_unmapped"].dropna().unique()

# 3) Create a DataFrame from the unique values
unique_df = pd.DataFrame({"Condición_unmapped": unique_vals})

# 4) (Optional) Sort for readability
unique_df = unique_df.sort_values(by="Condición_unmapped").reset_index(drop=True)

# 5) Export to a new CSV
output_path = "project_code/helpers/unique_unmapped_conditions.csv"
unique_df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Wrote unique values to: {output_path}")