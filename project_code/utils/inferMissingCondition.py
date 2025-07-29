import os
import json
import re

import pandas as pd
from attributeHarmonizer import load_configuration, harmonize_dataframe
from LogerHandler import setup_logger

logger = setup_logger("FindUnmappedCondition")

def build_unmapped_column(df: pd.DataFrame,
                          orig_col: str,
                          all_mapping_keys: list[str],
                          new_col_name: str) -> pd.DataFrame:
    """
    For each row in df, take df[orig_col] (a string), remove every substring
    that matches one of the mapping‐keys (case‐insensitive, word‐based),
    and write what remains into new_col_name.
    
    If nothing remains, new_col_name will be an empty string.
    """
    # Precompile a single regex that matches ANY of the mapping keys as whole words:
    #   e.g. r"\b(legítimo|legitima|…|doña)\b"
    escaped_keys = [re.escape(k) for k in all_mapping_keys]
    pattern = re.compile(r"\b(" + "|".join(escaped_keys) + r")\b", flags=re.IGNORECASE)
    
    def _extract_unmapped(text: str) -> str:
        if not isinstance(text, str):
            return ""
        # 1) Remove each mapped key (case‐insensitive) by replacing it with ""
        without_mapped = pattern.sub("", text)
        # 2) Collapse any leftover extra whitespace
        cleaned = re.sub(r"\s+", " ", without_mapped).strip()
        return cleaned
    
    df[new_col_name] = df[orig_col].apply(_extract_unmapped)
    return df


def main(config_path: str) -> pd.DataFrame:
    # 1) Load our JSON
    with open(config_path, "r", encoding="utf-8") as fp:
        config = json.load(fp)

    data_path, columns_to_harmonize, attribute_mappings = load_configuration(config_path)
    # We assume columns_to_harmonize == ["Condición"]
    orig_col = columns_to_harmonize[0]  # "Condición"

    # 2) Read the raw data
    df = pd.read_csv(data_path)

    # 3) Run harmonization (so that any mapped columns are already in place)
    df_h = harmonize_dataframe(df, columns_to_harmonize, attribute_mappings)

    # 4) Gather all individual mapping‐keys under "Condición" (from all sub‐dicts)
    mapping_dicts = attribute_mappings[orig_col]  # e.g. a dict with keys "legitimacy_status", etc.
    all_keys = []
    for sub_dict in mapping_dicts.values():
        all_keys.extend(sub_dict.keys())
    # all_keys now contains every string that attributeHarmonizer would match (e.g. "legítimo", "soltero", "indio", ...)

    # 5) Build a new column "Condición_unmapped" by stripping out any of those keys
    #    from the original "Condición" text.
    df_result = build_unmapped_column(
        df_h,
        orig_col,
        all_keys,
        new_col_name=f"{orig_col}_unmapped"
    )

    # 6) (Optional) If you only want the unmapped column in the final output:
    #    keep_cols = [f"{orig_col}_unmapped"]
    #    return df_result[keep_cols]

    return df_result


if __name__ == "__main__":
    logger.info("Finding unmapped fragments in 'Condición' …")
    config_json = os.path.join(
        os.path.dirname(__file__),
        "missingConfig.json"
    )
    result_df = main(config_json)

    # Example: save everything so you can inspect both the mapped columns and the new "_unmapped" column
    out_path = os.path.splitext(config_json)[0] + "_with_unmapped.csv"
    result_df.to_csv(out_path, index=False)
    print(f"Wrote results (including Condición_unmapped) to\n  {out_path}")