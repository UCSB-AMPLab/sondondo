import pandas as pd
import numpy as np

# Step 1: Read in original data
unique_conditions_df = pd.DataFrame(
    pd.read_csv("data/raw/bautismos.csv")["Condición"],
    columns=["Condición"]
)

# Lowercase everything
unique_conditions_df["Condición"] = unique_conditions_df["Condición"].astype(str).str.lower()

def harmonize_text(mapping_dictionary, data_to_transform):
    def transform_value(value):
        # Loop through each key in the mapping dictionary
        for key in mapping_dictionary:
            # If the key is contained within the value, return the mapped value
            if key in value:
                return mapping_dictionary[key]
        # If no matches found, return the original value
        return "default"
    
    # Apply the function to the Series
    return data_to_transform.apply(transform_value)

firstAttribute = {"hija": "hija", "hijo": "hijo"}
secondAttribute = {"legitimo": "legítimo", 
                   "legitima": "legítima",
                   "legítimo" : "legítimo",
                   "legítima": "legítima",
                   "natural": "natural"
                   }
# Apply the function to the "Condición" column
firstAttributeFrame = harmonize_text(firstAttribute, unique_conditions_df["Condición"])
secondAttributeFrame = harmonize_text(secondAttribute, unique_conditions_df["Condición"])

combinedAttributeFrame = firstAttributeFrame.str.strip() + " " + secondAttributeFrame.str.strip()

combinedAttributeFrame.to_csv("data/testing/unique_condiciones_harmonized.csv", index=False)
