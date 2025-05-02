import pandas as pd
import numpy as np
import json
import os

"""
New proposed structure

1. Function that harmonizes the data
2. Function that takes in the data frame and the attributes associatted 
as well as the columns that need to be harmonized. 
Which then afterwards calls the first function
3. Call the second function with the location of a file that tells the program 
what file to look at, what column to look at, and the attributes to look for.
"""
# Harmonizes the text in datasets
def harmonize_text(mapping_dictionary: dict, data_to_transform: pd.Series) -> pd.Series:
        
    # Copies dataframe and lowercases column & mapping dictionary
    transformed = data_to_transform.copy()
    transformed = transformed.str.lower()
    lowercased_mapping = {k.lower(): v for k, v in mapping_dictionary.items()}
    
    # Define the transformation function with improved matching
    def transform_value(value):
        # Check to see if null value
        if pd.isna(value) or value == '':
            return pd.NA
        
        # Check if the value is already a value in mapping_dictionary
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

# Harmonizes the dataframe by caling harmonize_text()
def harmonize_dataframe(df: pd.DataFrame,
                        columns_to_harmonize: list,
                        attribute_mappings: dict) -> pd.DataFrame:
    harmonized_df = df.copy()
    for column in columns_to_harmonize:
        if column not in df.columns:
            print(f"Warning: Column '{column}' not found; skipping.")
            continue

        mappings_for_col = attribute_mappings.get(column, {})
        # mappings_for_col is now a dict like {"role": {...}, "status": {...}}
        for aspect_name, mapping_dict in mappings_for_col.items():
            new_col = f"{column}_{aspect_name}"
            harmonized_df[new_col] = harmonize_text(mapping_dict, df[column])

    return harmonized_df

def load_configuration(config_path: str) -> tuple:
    """
    Loads configuration from a JSON file.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        tuple: (data_path, columns_to_harmonize, attribute_mappings)
    """
    try:
        # Check if file exists
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
            
        # Read and parse the JSON file
        with open(config_path, 'r') as file:
            config = json.load(file)
            
        # Extract the data file path
        data_path = config.get('data_path', '')
        if not data_path:
            raise ValueError("Data file path not specified in configuration")
            
        # Extract the columns to harmonize
        columns_to_harmonize = config.get('columns_to_harmonize', [])
        if not columns_to_harmonize:
            raise ValueError("No columns specified for harmonization")
            
        # Extract the attribute mappings
        attribute_mappings = config.get('attribute_mappings', {})
        if not attribute_mappings:
            raise ValueError("No attribute mappings found in configuration")
            
        return data_path, columns_to_harmonize, attribute_mappings
        
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {config_path}")
    except Exception as e:
        raise Exception(f"Error loading configuration: {str(e)}")

def main(config_path: str):
    """
    Main function that orchestrates the data harmonization process.
    
    Args:
        config_path (str): Path to the configuration file
    """
    try:
        # Load configuration
        data_path, columns_to_harmonize, attribute_mappings = load_configuration(config_path)
        
        print(f"Processing data file: {data_path}")
        print(f"Columns to harmonize: {columns_to_harmonize}")
        
        # Check if data file exists
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found at {data_path}")
            
        # Load the data
        file_extension = os.path.splitext(data_path)[1].lower()
        if file_extension == '.csv':
            df = pd.read_csv(data_path)
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(data_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}. Only CSV and Excel files are supported.")
            
        # Harmonize the data
        harmonized_df = harmonize_dataframe(df, columns_to_harmonize, attribute_mappings)
        
        # Save the harmonized data
        output_path = os.path.splitext(data_path)[0] + "_harmonized" + file_extension
        if file_extension == '.csv':
            harmonized_df.to_csv(output_path, index=False)
        else:
            harmonized_df.to_excel(output_path, index=False)
            
        print(f"Harmonized data saved to: {output_path}")
        
        return harmonized_df
        
    except Exception as e:
        print(f"Error in data harmonization process: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    
    config_path = "sondondo/code/helpers/config.json"
        
    main(config_path)