import pandas as pd
import numpy as np

"""
New proposed structure

1. Function that harmonizes the data
2. Function that takes in the data frame and the attributes associatted 
as well as the columns that need to be harmonized. 
Which then afterwards calls the first function
3. Call the second function with the location of a file that tells the program 
what file to look at, what column to look at, and the attributes to look for.
"""

def harmonize_text(mapping_dictionary: dict, data_to_transform: pd.Series) -> pd.Series:
    
    # Handle None values
    if data_to_transform is None:
        return pd.Series([pd.NA])
    
    # Create a copy to avoid modifying the original
    transformed = data_to_transform.copy()
    
    # Lowercase the entire column
    transformed = transformed.str.lower()
    
    # Make sure mapping keys are lowercase too
    lowercased_mapping = {k.lower(): v for k, v in mapping_dictionary.items()}
    
    # Define the transformation function with improved matching
    def transform_value(value):
        if pd.isna(value) or value == '':
            return pd.NA
        
        # Check if the value is already a standard value (exists as a value in the mapping)
        if value in lowercased_mapping.values():
            return value
            
        # Split the value into words for better matching
        words = value.split()
        
        # Look for exact word matches first
        for word in words:
            if word in lowercased_mapping:
                return lowercased_mapping[word]
        
        # If no exact word match, try substring matching
        for key in lowercased_mapping:
            if key in value:
                return lowercased_mapping[key]
                
        # If no matches are found, return NA
        return pd.NA
    
    # Apply the function to the Series
    return transformed.apply(transform_value)


# Read in data sets

baptism_df = pd.read_csv("data/raw/bautismos.csv")
marriage_df =pd.read_csv("data/raw/matrimonios.csv")
death_df = pd.read_csv("data/raw/entierros.csv")


""""
TESTING
firstAttribute = {"hija": "hija", "hijo": "hijo"}
secondAttribute = {"legitimo": "legítimo", 
                   "legitima": "legítima",
                   "legítimo" : "legítimo",
                   "legítima": "legítima",
                   "natural": "natural"
                   }


# Step 1: Read in original data
unique_conditions_df = pd.DataFrame(
    pd.read_csv("data/raw/bautismos.csv")["Condición"],
    columns=["Condición"]
)

firstAttributeFrame = harmonize_text(firstAttribute, unique_conditions_df["Condición"])
secondAttributeFrame = harmonize_text(secondAttribute, unique_conditions_df["Condición"])

combinedAttributeFrame = firstAttributeFrame.str.strip() + " " + secondAttributeFrame.str.strip()

combinedAttributeFrame.to_csv("data/testing/unique_condiciones_harmonized.csv", index=False)
"""
