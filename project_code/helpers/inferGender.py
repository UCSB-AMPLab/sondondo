import pandas as pd
import numpy as np
import json
import os
import logging
import os.path


# Setting up Logger
from LogerHandler import setup_logger
from attributeHarmonizer import harmonize_dataframe, load_configuration

# Configuration Path
config_path = "project_code/helpers/configurations/genderInfer.json"

# Setting up the variables in order to harmonzie the data
# data_path: Where the data is located (ex. bautismos.csv)
# columns_to_harmonize: what columns in the dataframe should be harmonized (ex. condicion)
# attribute_mappins: what words should be mapped to what (ex. hijo -> hijo)
data_path, columns_to_harmonize, attribute_mappings = load_configuration(config_path)
# Reads in the dataframe
df = pd.read_csv(data_path)
# what format should the harmonized data be saved in
file_extension = ".csv"
# where should the harmonized be saved?
output_path = os.path.splitext(data_path)[0] + str(columns_to_harmonize) + file_extension


# Harmonizing the data and saving only the needed columns
# Harmonize the DataFrame
harmonized_df = harmonize_dataframe(df, columns_to_harmonize, attribute_mappings)

# Get only new columns (not in original df)
new_columns = [col for col in harmonized_df.columns if col not in df.columns]

# Create a DataFrame with only the new columns
new_data = harmonized_df[new_columns]

# Save only new columns
new_data.to_csv(output_path, index=False)


