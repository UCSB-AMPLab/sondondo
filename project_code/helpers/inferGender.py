import pandas as pd
import numpy as np
import json
import os
import logging
import os.path

from LogerHandler import setup_logger
from attributeHarmonizer import harmonize_dataframe, load_configuration


config_path = "code/helpers/project_code/helpers/configurations/ageInferConfig.json"

data_path, columns_to_harmonize, attribute_mappings = load_configuration(config_path)
harmonized_df = harmonize_dataframe(df, columns_to_harmonize, attribute_mappings)

output_path = os.path.splitext(data_path)[0] + "_harmonized" + file_extension
harmonized_df.to_csv(output_path, index=False)
