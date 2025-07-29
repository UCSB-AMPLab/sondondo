import json
from pathlib import Path
from typing import Optional, Union
import numpy as np
import pandas as pd
import re
from rapidfuzz import process

from utils.LoggerHandler import setup_logger

# Set up logger using the custom logger function
logger = setup_logger("InferCondition")

class AttributeNormalizer:
    """
    A class for normalizing and harmonizing attribute values in pandas DataFrames.
    
    This class provides methods to standardize text values across different categories
    (social condition, legitimacy status, marital status) using predefined mapping dictionaries.
    It handles case-insensitive matching through exact matches, word-level matches, and substring matches.
    """

    def __init__(self, mapping_file: Union[str, Path], fuzzy_threshold: int = 80):
        """
        Initializes the AttributeNormalizer with a mapping file.
        
        Parameters
        ----------
        mapping_file : Union[str, Path]
            Path to the JSON file containing the mapping dictionary.
        """
        self.mapping_dictionary = self.load_mapping(mapping_file)
        self.fuzzy_threshold = fuzzy_threshold

    def load_mapping(self, mapping_path: Union[str, Path]) -> dict:
        """
        Load a mapping from a JSON file.
        """
        with open(mapping_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def extract_social_condition(self, social_condition_series: pd.Series) -> pd.Series:
        """
        Extracts and harmonizes social condition values from a pandas Series.
        
        Parameters
        ----------
        social_condition_series : pd.Series
            Series containing the social condition data to be harmonized
            
        Returns
        -------
        pd.Series
            A new Series with harmonized social condition values. Unmatched values are replaced with pandas.NA.
        """
        logger.info("Extracting social condition attributes")
        return self.harmonize_text(social_condition_series, self.mapping_dictionary['attribute_mappings']['social_condition'])

    def extract_legitimacy_status(self, legitimacy_series: pd.Series) -> pd.Series:
        """
        Extracts and harmonizes legitimacy status values from a pandas Series.
        
        Parameters
        ----------
        legitimacy_series : pd.Series
            Series containing the legitimacy status data to be harmonized
            
        Returns
        -------
        pd.Series
            A new Series with harmonized legitimacy status values. Unmatched values are replaced with pandas.NA.
        """
        logger.info("Extracting legitimacy status attributes")
        return self.harmonize_text(legitimacy_series, self.mapping_dictionary['attribute_mappings']['legitimacy_status'])

    def extract_marital_status(self, marital_status_series: pd.Series) -> pd.Series:
        """
        Extracts and harmonizes marital status values from a pandas Series.
        
        Parameters
        ----------
        marital_status_series : pd.Series
            Series containing the marital status data to be harmonized
            
        Returns
        -------
        pd.Series
            A new Series with harmonized marital status values. Unmatched values are replaced with pandas.NA.
        """
        logger.info("Extracting marital status attributes")
        return self.harmonize_text(marital_status_series, self.mapping_dictionary['attribute_mappings']['marital_status'])
    
    def extract_all_attributes(self, series: pd.Series, prefix: str = "attr") -> pd.DataFrame:
        """
        Extracts all attributes (social condition, legitimacy status, marital status) from a Series.
        """
        return pd.DataFrame({
            f"{prefix}_social_condition": self.extract_social_condition(series),
            f"{prefix}_legitimacy_status": self.extract_legitimacy_status(series),
            f"{prefix}_marital_status": self.extract_marital_status(series),
        })


    def transform_value(self, value, map_dict: dict) -> Union[str, float]:
        """
        Transforms a single value using a mapping dictionary with multi-level matching.
        
        Applies case-insensitive matching in this order:
        1. Checks if value is already a mapped target value
        2. Tries exact word matches within the value
        3. Falls back to substring matching
        
        Parameters
        ----------
        value : str
            The value to transform
        map_dict : dict
            Dictionary mapping source values to target values
            
        Returns
        -------
        Union[str, float]
            The mapped value if found, otherwise np.nan
        """

        if pd.isna(value) or value == '':
            return np.nan
        
        lowercased_mapping = {k.lower(): v for k, v in map_dict.items()}
        value = value.lower()

        # Check if the value is already a value in mapping_dictionary
        if value in lowercased_mapping.values():
            return value
            
        # Word level matching
        words = value.split()
        for word in words:
            if word in lowercased_mapping:
                return lowercased_mapping[word]
        
        # Substring matching
        for key in lowercased_mapping:
            if key in value:
                return lowercased_mapping[key]
            
        # Fuzzy matching
        match, score, _ = process.extractOne(value, lowercased_mapping.keys())
        if score > self.fuzzy_threshold:
            return lowercased_mapping[match]
                
        # If no matches are found, log it and return na
        logger.warning(f"Unmapped value in column '{value}'")
        return np.nan

    def harmonize_text(self, data_to_transform: pd.Series, map_dict: dict) -> pd.Series:
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
        data_to_transform : pd.Series
            Series containing the text data to be harmonized
        map_dict : dict
            Dictionary where keys are source values to be transformed and values are 
            the standardized target values. 
            
        Returns
        -------
        pd.Series
            A new Series with harmonized values. Values that couldn't be matched
            are replaced with pandas.NA
        """
        # Copies dataframe and lowercases column & mapping dictionary
        transformed = data_to_transform.copy()
        transformed = transformed.str.lower()
        
        # Apply the function to the Series
        return transformed.apply(self.transform_value, map_dict=map_dict)
    
    def harmonize_dataframe(self, df: pd.DataFrame,
                            columns_to_harmonize: list) -> pd.DataFrame:
        """
        Harmonizes multiple columns in a DataFrame based on the instance's mapping dictionary.
        
        This function processes a DataFrame by standardizing values in specified columns
        according to the mapping dictionaries loaded during initialization. For each column 
        to harmonize, it creates one or more new columns with standardized values while 
        preserving the original data.
        
        Parameters
        ----------
        df : pd.DataFrame
            The input DataFrame containing columns to be harmonized
            
        columns_to_harmonize : list
            List of column names to process. Each column must exist in the DataFrame
            and have a corresponding entry in the instance's mapping dictionary
            
        Returns
        -------
        pd.DataFrame
            A new DataFrame that includes all original columns plus newly created
            harmonized columns. For each column in columns_to_harmonize and each
            aspect in the mapping dictionary, a new column is created with the naming
            pattern: "{original_column}_{aspect_name}"
        """
        # Makes a copy to not change original dataframe
        harmonized_df = df.copy()
        
        for column in columns_to_harmonize:
            if column not in df.columns:
                logger.warning(f"Column '{column}' not found; skipping.")
                continue

            mappings_for_col = self.mapping_dictionary.get(column, {})
            # mappings_for_col is now a dict like {"role": {...}, "status": {...}}
            for aspect_name, mapping_dict in mappings_for_col.items():
                new_col = f"{column}_{aspect_name}"
                harmonized_df[new_col] = self.harmonize_text(df[column], mapping_dict)
                logger.debug(f"Created harmonized column: {new_col}")

        return harmonized_df


    def extract_unmapped_tokens(self, df: pd.DataFrame, original_column: str, new_col_name: Optional[str] = None) -> pd.DataFrame:
        """
        Identifies and extracts unmapped content by removing all known tokens from the original column.
        
        This method creates a new column containing only the text that wasn't matched by any 
        of the mapping dictionaries for the specified column. It uses regex to remove all 
        known mapped tokens, leaving behind potentially valuable unmapped content.
        
        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame containing the column to process
        original_column : str
            The name of the column from which to extract unmapped tokens
        new_col_name : Optional[str], default None
            Name for the new column. If None, defaults to "{original_column}_unmapped"
            
        Returns
        -------
        pd.DataFrame
            The original DataFrame with an additional column containing unmapped tokens
        """

        if new_col_name is None:
            new_col_name = f"{original_column}_unmapped"

        # Gather all keys from all sub-mappings under the original column
        mapping_dicts = self.mapping_dictionary.get(original_column, {})
        all_keys = [re.escape(k) for d in mapping_dicts.values() for k in d.keys()]
        pattern = re.compile(r"\b(" + "|".join(all_keys) + r")\b", flags=re.IGNORECASE)

        def strip_mapped(value: str) -> str:
            if not isinstance(value, str):
                return ""
            cleaned = re.sub(pattern, "", value)
            return re.sub(r"\s+", " ", cleaned).strip()

        df[new_col_name] = df[original_column].apply(strip_mapped)
        return df



