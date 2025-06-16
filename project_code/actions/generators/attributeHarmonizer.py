import pandas as pd
import numpy as np
import json
import os
import logging
import os.path
from helpers.handlers.LogerHandler import setup_logger

# Set up logger using the centralized logging function
logger = setup_logger("AttributeNormalizer")


def harmonize_text(mapping_dictionary: dict, data_to_transform: pd.Series) -> pd.Series:
    """
    Harmonizes textual data by standardizing values according to a mapping dictionary.
    
    This function normalizes text values in a pandas Series by applying a multi-step
    matching process against a provided mapping dictionary. The harmonization process:
    1. Converts all text to lowercase for case-insensitive matching
    2. Checks if the value is already a standard value in the mapping
    3. Tries to match individual words within the value
    4. Falls back to substring matching if word matching fails
    
    Parameters
    ----------
    mapping_dictionary : dict
        Dictionary where keys are source values to be transformed and values are 
        the standardized target values. For example: {'hr': 'Human Resources'}
    
    data_to_transform : pd.Series
        Series containing the text data to be harmonized
        
    Returns
    -------
    pd.Series
        A new Series with harmonized values. Values that couldn't be matched
        are replaced with pandas.NA
    """
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
                
        # If no matches are found, log it and return the original
        logger.warning(f"Unmapped value in column '{value}'")
        return "unknown"
    
    # Apply the function to the Series
    return transformed.apply(transform_value)

def harmonize_dataframe(df: pd.DataFrame,
                        columns_to_harmonize: list,
                        attribute_mappings: dict) -> pd.DataFrame:
    """
    Harmonizes multiple columns in a DataFrame based on provided attribute mappings.
    
    This function processes a DataFrame by standardizing values in specified columns
    according to mapping dictionaries. For each column to harmonize, it creates one or more
    new columns with standardized values while preserving the original data.
    
    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing columns to be harmonized
        
    columns_to_harmonize : list
        List of column names to process. Each column must exist in the DataFrame
        and have a corresponding entry in attribute_mappings
        
    attribute_mappings : dict
        A nested dictionary structure where:
        - First level keys are column names from columns_to_harmonize
        - Second level keys are aspect names that become part of new column names
        - Third level contains the mapping dictionaries used for harmonization
        
    Returns
    -------
    pd.DataFrame
        A new DataFrame that includes all original columns plus newly created
        harmonized columns. For each column in columns_to_harmonize and each
        aspect in attribute_mappings, a new column is created with the naming
        pattern: "{original_column}_{aspect_name}"
    """
    # Makes a copy to not change original dataframe
    harmonized_df = df.copy()
    
    for column in columns_to_harmonize:
        if column not in df.columns:
            logger.warning(f"Column '{column}' not found; skipping.")
            continue

        mappings_for_col = attribute_mappings.get(column, {})
        # mappings_for_col is now a dict like {"role": {...}, "status": {...}}
        for aspect_name, mapping_dict in mappings_for_col.items():
            new_col = f"{column}_{aspect_name}"
            harmonized_df[new_col] = harmonize_text(mapping_dict, df[column])
            logger.debug(f"Created harmonized column: {new_col}")

    return harmonized_df

def load_configuration(config_path: str) -> tuple:
    """
    Loads and validates configuration settings from a JSON file.
    
    This function reads a JSON configuration file and extracts the required settings
    for data harmonization: the data file path, columns to harmonize, and attribute
    mappings. It performs validation on the configuration to ensure all required
    elements are present and properly formatted.
    
    Parameters
    ----------
    config_path : str
        Path to the JSON configuration file
        
    Returns
    -------
    tuple
        A tuple containing three elements:
        - data_path (str): Path to the data file to be processed
        - columns_to_harmonize (list): List of column names to harmonize
        - attribute_mappings (dict): Nested dictionary of mapping configurations
    """
    try:
        # Check if file exists
        if not os.path.exists(config_path):
            logger.error(f"Configuration file not found at {config_path}")
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
            
        # Read and parse the JSON file
        with open(config_path, 'r') as file:
            config = json.load(file)
            
        # Extract the data file path
        data_path = config.get('data_path', '')
        if not data_path:
            logger.error("Data file path not specified in configuration")
            raise ValueError("Data file path not specified in configuration")
            
        # Extract the columns to harmonize
        columns_to_harmonize = config.get('columns_to_harmonize', [])
        if not columns_to_harmonize:
            logger.error("No columns specified for harmonization")
            raise ValueError("No columns specified for harmonization")
            
        # Extract the attribute mappings
        attribute_mappings = config.get('attribute_mappings', {})
        if not attribute_mappings:
            logger.error("No attribute mappings found in configuration")
            raise ValueError("No attribute mappings found in configuration")
            
        logger.info(f"Configuration loaded successfully from {config_path}")
        return data_path, columns_to_harmonize, attribute_mappings
        
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in {config_path}")
        raise ValueError(f"Invalid JSON format in {config_path}")
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        raise Exception(f"Error loading configuration: {str(e)}")

def main(config_path: str):
    """
    Main function that orchestrates the data harmonization process.
    The function does this by loading the configuration file and then saving the harmonized
    data as a new column in the dataframe.
    
    Args:
        config_path (str): Path to the configuration file
    """
    try:
        logger.info(f"Starting data harmonization process with config: {config_path}")
        
        # Load configuration
        data_path, columns_to_harmonize, attribute_mappings = load_configuration(config_path)
        
        logger.info(f"Processing data file: {data_path}")
        logger.info(f"Columns to harmonize: {columns_to_harmonize}")
        
        if not os.path.exists(data_path):
            logger.error(f"Data file not found at {data_path}")
            raise FileNotFoundError(f"Data file not found at {data_path}")
            
        # Load the data
        file_extension = os.path.splitext(data_path)[1].lower()
        if file_extension == '.csv':
            logger.info(f"Loading CSV file: {data_path}")
            df = pd.read_csv(data_path)
        elif file_extension in ['.xls', '.xlsx']:
            logger.info(f"Loading Excel file: {data_path}")
            df = pd.read_excel(data_path)
        else:
            error_msg = f"Unsupported file type: {file_extension}. Only CSV and Excel files are supported."
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"Data loaded successfully with {len(df)} rows and {len(df.columns)} columns")
            
        # Harmonize the data
        logger.info("Starting data harmonization...")
        harmonized_df = harmonize_dataframe(df, columns_to_harmonize, attribute_mappings)
        logger.info("Data harmonization completed successfully")
        
        # Save the harmonized data
        output_path = os.path.splitext(data_path)[0] + "_harmonized" + file_extension
        if file_extension == '.csv':
            harmonized_df.to_csv(output_path, index=False)
        else:
            harmonized_df.to_excel(output_path, index=False)
            
        logger.info(f"Harmonized data saved to: {output_path}")
        
        return harmonized_df
        
    except Exception as e:
        logger.error(f"Error in data harmonization process: {str(e)}")
        return None

if __name__ == "__main__":
    import sys
    
    #Defines the config file path and then calls main function
    config_path = "code/helpers/config.json"
    logger.info(f"Using configuration file: {config_path}")
        
    result = main(config_path)
    
    if result is not None:
        logger.info("Data harmonization completed successfully")
    else:
        logger.error("Data harmonization failed")