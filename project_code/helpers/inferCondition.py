import os
import json
import pandas as pd

from attributeHarmonizer import load_configuration, harmonize_dataframe
from LogerHandler import setup_logger

# Set up logger using the custom logger function
logger = setup_logger("InitialCondition")

def main(config_path: str) -> pd.DataFrame:
    """
    Main function that orchestrates the data harmonization process.
    Loads the input file, runs harmonize_dataframe, then returns only the newly created columns.
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
        
        # Identify which columns are newly created
        original_cols = set(df.columns)
        all_cols = list(harmonized_df.columns)
        new_cols = [col for col in all_cols if col not in original_cols]
        
        # Keep only the newly created columns
        result_df = harmonized_df[new_cols]
        
        # Save those new columns to an output file
        output_path = os.path.splitext(data_path)[0] + "_harmonized" + file_extension
        if file_extension == '.csv':
            result_df.to_csv(output_path, index=False)
        else:
            result_df.to_excel(output_path, index=False)
            
        logger.info(f"Newly created columns saved to: {output_path}")
        return result_df
        
    except Exception as e:
        logger.error(f"Error in data harmonization process: {str(e)}")
        return None

if __name__ == "__main__":
    # Defines the config file path and then calls main function
    config_path = "project_code/helpers/config.json"
    logger.info(f"Using configuration file: {config_path}")
        
    result = main(config_path)
    if result is not None:
        logger.info("Data harmonization completed successfully")
    else:
        logger.error("Data harmonization failed")