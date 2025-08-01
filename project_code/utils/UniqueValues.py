"""
This helper module provides a utility class to
extract unique values from multiple columns in multiple DataFrames.

"""

from typing import List, Optional, Union
import pandas as pd
import numpy as np

class UniqueValuesExtractor:
    """
    
    """

    def __init__(self, dataframes: List[pd.DataFrame]):
        """
        Initialize with a list of DataFrames.
        
        :param dataframes: List of pandas DataFrames
        """
        self.dataframes = dataframes

    def get_unique_values(self, return_dataframe: bool = False) -> Union[np.ndarray, pd.DataFrame]:
        """
        Get unique values from the specified column across all DataFrames.

        :param column: The column name to extract unique values from
        :return: Numpy array of unique values
        """
        all_columns = pd.concat(self.dataframes, ignore_index=True)

        all_unique_values = all_columns.stack().unique() # type: ignore
        all_unique_values = all_unique_values[~pd.isna(all_unique_values)]

        all_unique_values = np.unique(all_unique_values)
        
        if return_dataframe:
            return pd.DataFrame({'original_place': all_unique_values})
        else:
            return all_unique_values
        