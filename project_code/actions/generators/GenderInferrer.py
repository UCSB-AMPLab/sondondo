import pandas as pd
import numpy as np
from typing import Union, Dict, Optional, List
import gender_guesser.detector as gender
from utils.LoggerHandler import setup_logger

class GenderInferrer:
    """
    A class to infer gender from name values in a pandas Series.
    
    This class provides methods to:
    1. Infer gender directly from names using gender_guesser
    2. Infer gender from condition/attribute mappings with name-based fallback
    3. Return normalized gender values as a new Series
    """
    
    def __init__(self, name_series: pd.Series = None, mappings: Dict = None) -> None:
        """
        Initialize the GenderInferrer with optional name Series and mappings.
        
        Args:
            name_series: Optional Series containing names to infer gender from
            mappings: Optional dictionary mapping condition values to gender values
        """
        self.name_series = name_series
        self.mappings = mappings
        self.detector = gender.Detector(case_sensitive=False)
        self.logger = setup_logger("GenderInferrer")
        self.logger.info(f"Initialized GenderInferrer with {len(name_series) if name_series is not None else 0} entries.")
    
    def infer_from_names(self, name_series: Optional[pd.Series] = None) -> pd.Series:
        """
        Infer gender directly from names using gender_guesser.
        
        Args:
            name_series: Optional Series of names to process (uses instance series if None)
            
        Returns:
            A Series with inferred gender values
        """
        if name_series is not None:
            self.name_series = name_series
        
        if self.name_series is None:
            raise ValueError("No name series provided to infer genders from")
            
        result_series = pd.Series([None] * len(self.name_series), dtype=object)
        
        for idx, name in self.name_series.items():
            try:
                gender_value = self._infer_gender_from_name(name)
                result_series[idx] = gender_value
                
                if gender_value != 'unknown':
                    self.logger.info(f"Inferred gender '{gender_value}' from name '{name}' at index {idx}")
                
            except Exception as e:
                self.logger.error(f"Error inferring gender for '{name}' at index {idx}: {e}")
                result_series[idx] = 'unknown'
                
        return result_series
    
    def _infer_gender_from_name(self, name: str) -> str:
        """
        Infer gender from a single name string.
        
        1) Try detector.get_gender(name) on the full string.
        2) If that returns 'unknown' and there's more than one token,
           try again with just the first token.
        3) Return whatever detector.get_gender(...) returns 
           (e.g. 'male','mostly_female','andy','unknown', etc.).
        
        Args:
            name: The name string to infer gender from
            
        Returns:
            Inferred gender as string
        """
        if not isinstance(name, str) or name.strip() == "":
            return "unknown"

        raw = self.detector.get_gender(name)
        if raw != 'unknown':
            return raw

        tokens = name.strip().split()
        if len(tokens) > 1:
            return self.detector.get_gender(tokens[0])
        return raw
    
    def infer_from_condition(self, 
                            condition_series: pd.Series, 
                            name_series: Optional[pd.Series] = None,
                            mappings: Optional[Dict] = None) -> pd.Series:
        """
        Infer gender from a condition Series with fallback to names.
        
        Args:
            condition_series: Series containing condition values to map to gender
            name_series: Optional Series of names for fallback (uses instance series if None)
            mappings: Optional mapping dictionary (uses instance mappings if None)
            
        Returns:
            A Series with inferred gender values and a Series with source info
        """
        if name_series is not None:
            self.name_series = name_series
            
        if mappings is not None:
            self.mappings = mappings
            
        if self.name_series is None:
            raise ValueError("No name series provided for fallback gender inference")
            
        if self.mappings is None:
            raise ValueError("No mappings provided for condition-to-gender mapping")
            
        result_series = pd.Series([None] * len(condition_series), dtype=object)
        source_series = pd.Series([None] * len(condition_series), dtype=object)
        
        for idx, condition in condition_series.items():
            try:
                # Try to get gender from condition mapping
                if condition in self.mappings and not pd.isna(self.mappings[condition]):
                    mapped_gender = self.mappings[condition]
                    result_series[idx] = mapped_gender
                    source_series[idx] = 'mapped'
                    self.logger.info(f"Mapped condition '{condition}' to gender '{mapped_gender}' at index {idx}")
                else:
                    # Fallback to name-based inference
                    name = self.name_series.iloc[idx] if idx < len(self.name_series) else ""
                    gender_value = self._infer_gender_from_name(name)
                    result_series[idx] = gender_value
                    source_series[idx] = 'guessed'
                    self.logger.info(
                        f"Row {idx}: no mapped gender for condition '{condition}', "
                        f"falling back to name-based inference: '{name}' → '{gender_value}'"
                    )
            except Exception as e:
                self.logger.error(f"Error inferring gender at index {idx}: {e}")
                result_series[idx] = 'unknown'
                source_series[idx] = 'error'
                
        return result_series, source_series

    def get_gender_categories(self) -> List[str]:
        """
        Returns a list of possible gender categories from the detector.
        
        Returns:
            List of gender categories
        """
        return ['male', 'female', 'mostly_male', 'mostly_female', 'andy', 'unknown']
        
    def simplify_gender(self, gender_series: pd.Series) -> pd.Series:
        """
        Simplify gender values to just 'male', 'female', or 'unknown'.
        
        Args:
            gender_series: Series with gender values to simplify
            
        Returns:
            Series with simplified gender values
        """
        result = gender_series.copy()
        
        # Map mostly_male to male and mostly_female to female
        result = result.replace('mostly_male', 'male')
        result = result.replace('mostly_female', 'female')
        
        # Map andy to unknown
        result = result.replace('andy', 'unknown')
        
        return result

# Example usage in a script:
if __name__ == "__main__":
    import os
    import json
    
    # Example with a DataFrame and configuration
    config_path = "project_code/helpers/configurations/genderInfer.json"
    
    # Set up logging
    logger = setup_logger("GenderInferrer")
    
    # Load configuration
    with open(config_path, "r", encoding="utf-8") as fp:
        config = json.load(fp)
    
    # Get paths from config
    input_csv = config.get("input_csv")
    output_csv = config.get("output_csv")
    
    # Get mapping from config
    attribute_mappings = config.get("attribute_mappings", {})
    
    # Get name column
    name_column = config.get("gender_guesser", {}).get("name_column")
    condition_column = config.get("columns_to_harmonize", [])[0] if config.get("columns_to_harmonize") else None
    
    # Load the data
    df = pd.read_csv(input_csv)
    
    # Create GenderInferrer instance
    inferrer = GenderInferrer(df[name_column], attribute_mappings)
    
    # Infer gender
    if condition_column:
        gender_series, source_series = inferrer.infer_from_condition(df[condition_column])
        df["gender_final"] = gender_series
        df["gender_source"] = source_series
    else:
        # Direct inference from names
        gender_series = inferrer.infer_from_names()
        df["gender_final"] = gender_series
    
    # Save results
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    logger.info(f"Wrote output (with gender columns) to: {output_csv}")
    print(f"Wrote output (with gender columns) to:\n  {output_csv}")
