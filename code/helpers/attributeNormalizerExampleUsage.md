# Data Harmonization Example

## Sample Configuration File (config.json)
```json
{
  "data_path": "sample_data/employees.csv",
  "columns_to_harmonize": ["department", "job_title"],
  "attribute_mappings": {
    "department": {
      "category": {
        "it": "Technology",
        "information technology": "Technology",
        "tech": "Technology",
        "engineering": "Technology",
        "hr": "Human Resources",
        "human resources": "Human Resources",
        "finance": "Finance",
        "accounting": "Finance",
        "marketing": "Marketing",
        "sales": "Sales"
      }
    },
    "job_title": {
      "level": {
        "senior": "Senior",
        "sr": "Senior",
        "lead": "Senior",
        "junior": "Junior",
        "jr": "Junior",
        "associate": "Junior",
        "manager": "Manager",
        "director": "Director",
        "vp": "Executive",
        "chief": "Executive",
        "president": "Executive"
      }
    }
  }
}
```

## Sample Data (employees.csv)
```
id,name,department,job_title,hire_date
1,John Smith,IT,Senior Developer,2020-01-15
2,Jane Doe,human resources,HR Manager,2019-05-22
3,Bob Johnson,Finance,jr accountant,2021-03-10
4,Alice Williams,Marketing,Director of Marketing,2018-11-30
5,Charlie Brown,tech,Lead Engineer,2022-02-05
6,Diana Prince,SALES,VP of Sales,2017-08-17
7,Edward Jones,accounting,Chief Financial Officer,2016-04-21
8,Fiona Miller,information technology,associate developer,2023-01-03
```

## Running the Script
```python
# Assuming your script is named harmonize_data.py
import harmonize_data

# Run with the configuration file
result = harmonize_data.main("config.json")
```

## Expected Log Output
The script will generate a log file at `logs/date_normalizer.log` with content similar to:

```
2025-05-07 14:30:22,156 - __main__ - INFO - Starting data harmonization process with config: config.json
2025-05-07 14:30:22,158 - __main__ - INFO - Configuration loaded successfully from config.json
2025-05-07 14:30:22,159 - __main__ - INFO - Processing data file: sample_data/employees.csv
2025-05-07 14:30:22,160 - __main__ - INFO - Columns to harmonize: ['department', 'job_title']
2025-05-07 14:30:22,245 - __main__ - INFO - Loading CSV file: sample_data/employees.csv
2025-05-07 14:30:22,302 - __main__ - INFO - Data loaded successfully with 8 rows and 5 columns
2025-05-07 14:30:22,303 - __main__ - INFO - Starting data harmonization...
2025-05-07 14:30:22,432 - __main__ - INFO - Data harmonization completed successfully
2025-05-07 14:30:22,512 - __main__ - INFO - Harmonized data saved to: sample_data/employees_harmonized.csv
2025-05-07 14:30:22,513 - __main__ - INFO - Data harmonization completed successfully
```

## Expected Output File (employees_harmonized.csv)
The script would generate a new file with the original data plus the harmonized columns:

```
id,name,department,job_title,hire_date,department_category,job_title_level
1,John Smith,IT,Senior Developer,2020-01-15,Technology,Senior
2,Jane Doe,human resources,HR Manager,2019-05-22,Human Resources,Manager
3,Bob Johnson,Finance,jr accountant,2021-03-10,Finance,Junior
4,Alice Williams,Marketing,Director of Marketing,2018-11-30,Marketing,Director
5,Charlie Brown,tech,Lead Engineer,2022-02-05,Technology,Senior
6,Diana Prince,SALES,VP of Sales,2017-08-17,Sales,Executive
7,Edward Jones,accounting,Chief Financial Officer,2016-04-21,Finance,Executive
8,Fiona Miller,information technology,associate developer,2023-01-03,Technology,Junior
```

## What's Happening Behind the Scenes

1. **Initialization**: The script sets up logging to write to `logs/date_normalizer.log`

2. **Configuration Loading**: 
   - The script reads the JSON configuration file
   - Logs successful loading of configuration with file path

3. **Data Processing**:
   - Validates that the data file exists
   - Loads the CSV file based on file extension
   - Logs data loading with row and column counts

4. **Harmonization**:
   - For each specified column, creates new columns with standardized values
   - For example:
     - "IT", "tech", "information technology" → "Technology"
     - "Senior", "Lead", "sr" → "Senior"
   - Logs the start and completion of harmonization

5. **Output**:
   - Saves the harmonized data to a new file with "_harmonized" suffix
   - Logs the successful saving of the file with path

If any errors occur during processing (like missing files or incorrect JSON format), they would be logged with ERROR level and include details about the problem.
