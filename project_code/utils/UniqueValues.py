"""
This helper module provides a utility class to
extract unique values from multiple columns in multiple DataFrames.

"""

from typing import List, Optional, Union
import pandas as pd
import numpy as np

class UniqueValuesExtractor:
    """
    UniqueValuesExtractor extracts unique values from all columns across multiple pandas DataFrames.
+
+    This class is useful for aggregating unique values from several DataFrames, regardless of column names.
+    It provides a method to return the unique values either as a NumPy array or as a pandas DataFrame.
+
+    Example usage:
+        >>> import pandas as pd
+        >>> from UniqueValues import UniqueValuesExtractor
+        >>> df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
+        >>> df2 = pd.DataFrame({'A': [2, 5], 'B': [4, 6]})
+        >>> extractor = UniqueValuesExtractor([df1, df2])
+        >>> unique_values = extractor.get_unique_values()
+        >>> print(unique_values)
+        [1 2 3 4 5 6]
+        >>> unique_df = extractor.get_unique_values(return_dataframe=True)
+        >>> print(unique_df)
+           original_place
+        0              1
+        1              2
+        2              3
+        3              4
+        4              5
+        5              6
    
    """

    def __init__(self, dataframes: List[pd.DataFrame]):
        """
        Initialize with a list of DataFrames.
        
        :param dataframes: List of pandas DataFrames
        """
        self.dataframes = dataframes

    def get_unique_values(self, return_dataframe: bool = False) -> Union[np.ndarray, pd.DataFrame]:
        """
        Get unique values from all columns across all DataFrames.

        :return: Numpy array of unique values if return_dataframe is False, otherwise a pandas DataFrame of unique values.
        """
        all_columns = pd.concat(self.dataframes, ignore_index=True)

        all_unique_values = all_columns.stack().unique() # type: ignore
        all_unique_values = all_unique_values[~pd.isna(all_unique_values)]

        all_unique_values = np.unique(all_unique_values)
        
        if return_dataframe:
            return pd.DataFrame({'original_place': all_unique_values})
        else:
            return all_unique_values
        