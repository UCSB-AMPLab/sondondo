import pandas as pd
import json

files = ["bautismos", "entierros", "matrimonios"]

for file in files:
    csvfile = f"data/raw/{file}.csv"
    jsonfile = f"data/mappings/{file}Mapping.json"

    df = pd.read_csv(csvfile)

    # Transform the columns list into a dictionary
    columns = df.columns.to_series().to_dict()

    with open(jsonfile, "w") as f:
        json.dump(columns, f, indent=4, ensure_ascii=False)

    print(f"Columns for {file} saved to {jsonfile}")

