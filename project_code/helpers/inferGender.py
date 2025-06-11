import os
import json
import pandas as pd

from attributeHarmonizer import load_configuration, harmonize_dataframe
from LogerHandler import setup_logger

import gender_guesser.detector as gender
d = gender.Detector(case_sensitive=False)

# Infers the gender from a name column
def guessGender(name: str) -> str:
    """
    1) Try d.get_gender(name) on the full string.
    2) If that returns 'unknown' and there's more than one token,
       try again with just the first token.
    3) Return whatever d.get_gender(...) returns (e.g. 'male','mostly_female','andy','unknown', etc.).
    """
    if not isinstance(name, str) or name.strip() == "":
        return "unknown"

    raw = d.get_gender(name)
    if raw != 'unknown':
        return raw

    tokens = name.strip().split()
    if len(tokens) > 1:
        return d.get_gender(tokens[0])
    return raw
# ───────────────────────────────────────────────────


# Infers the gender through the condiiton column
def inferFromCondition(config_path: str) -> pd.DataFrame:
    """
    1) Load genderInfer.json → get input_csv, output_csv, columns_to_harmonize, attribute_mappings,
       and gender_guesser.name_column.
    2) Read the CSV at input_csv.
    3) Harmonize all columns_to_harmonize via attributeHarmonizer → this creates <col>_gender.
    4) For any row where <col>_gender is missing or 'unknown', run guessGender(name_column).
       Log that fallback. 
    5) Produce two new columns: 
         • 'gender_guessed'   ← only non-NA where fallback occurred 
         • 'gender_final'     ← either mapped (Condición_gender) or guessed
    6) Return the modified DataFrame. (Caller will write it to output_csv.)
    """
    # 1) Load JSON
    with open(config_path, "r", encoding="utf-8") as fp:
        config = json.load(fp)

    # (A) Pull file-paths from JSON
    input_csv  = config.get("input_csv")
    output_csv = config.get("output_csv")

    # (B) Pull attributeHarmonizer settings
    #    load_configuration expects the JSON to contain:
    #      • data_path
    #      • columns_to_harmonize
    #      • attribute_mappings
    _, columns_to_harmonize, attribute_mappings = load_configuration(config_path)

    # (C) Which column holds the full name for fallback?
    gg_block   = config.get("gender_guesser", {})
    name_column = gg_block.get("name_column")

    # 2) Read the raw CSV
    df = pd.read_csv(input_csv)

    # 3) Harmonize
    #    This creates a column "<col>_gender" for each col in columns_to_harmonize
    df = harmonize_dataframe(df, columns_to_harmonize, attribute_mappings)

    # 4) Determine which "<col>_gender" was created
    mapped_gender_col = None
    for c in columns_to_harmonize:
        candidate = f"{c}_gender"
        if candidate in df.columns:
            mapped_gender_col = candidate
            break
    if mapped_gender_col is None:
        raise RuntimeError("attributeHarmonizer did not produce any '*_gender' column.")

    # 5) Add placeholders for fallback + final
    df["gender_guessed"] = pd.NA
    df["gender_final"] = pd.NA

    # 6) Row-by-row resolution
    def _resolve(row):
        mapped = row[mapped_gender_col]
        if pd.isna(mapped) or str(mapped).lower() == "unknown":
            full_name = row.get(name_column, "")
            guessed   = guessGender(full_name)
            idx = row.name
            logger.info(
                f"Row {idx}: no mapped gender (got '{mapped}'), "
                f"falling back to guessGender('{full_name}') → '{guessed}'"
            )
            row["gender_guessed"] = guessed
            row["gender_final"] = guessed
        else:
            row["gender_final"] = mapped
        return row

    df = df.apply(_resolve, axis=1)
    return df


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    config_json = "project_code/helpers/configurations/genderInfer.json"
    # Set up logging so we can see each fallback
    logger = setup_logger("InferGender")

    # Run the infer_gender pipeline
    result_df = inferFromCondition(config_json)

    # Write out to whatever output_csv you specified in JSON
    with open(config_json, "r", encoding="utf-8") as fp:
        out_path = json.load(fp).get("output_csv")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    result_df.to_csv(out_path, index=False)
    print(f"Wrote output (with gender columns) to:\n  {out_path}")