from pathlib import Path
import json
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent #Use relative paths and Path objects

def load_mapping(mapping_path):  #return dictionary that used for mapping
    with open(mapping_path, "r", encoding="utf-8") as f:
        return json.load(f)

def harmonize_columns(csv_file, mapping_file):
    df = pd.read_csv(csv_file, encoding="utf-8")
    mapping = load_mapping(mapping_file)
    return df.rename(columns=mapping)


def main():
    events = ["bautismos", "entierros", "matrimonios"] #DRY

    raw_dir = BASE_DIR / "data" / "raw"
    mappings_dir = BASE_DIR / "data" / "mappings"
    harmonized_dir = BASE_DIR / "data" / "harmonized"
    harmonized_dir.mkdir(exist_ok=True)

    for event in events:
        csv_path = raw_dir / f"{event}.csv"
        mapping_path = mappings_dir / f"{event}Mapping.json"

        df_harmonized = harmonize_columns(csv_path, mapping_path)

        print(df_harmonized.head(3)) #test the result by looking at first three rows
        output_path = harmonized_dir / f"{event}Harmonized.csv"
        df_harmonized.to_csv(output_path, index = False, encoding = "utf-8")
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()
