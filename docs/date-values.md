# Date Values

Date value standard must be in the format `YYYY-MM-DD` [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html). All dates that do not follow this format will be processed to try to convert them to a valid date or will be converted to `NULL`.

## Validate Dates Values

Use the method `report_column_dates` from `DatesManager` class to validate the dates in the column.

```python
from helpers.DatesManager import DatesExplorer

dates_explorer = DatesExplorer(baptismsdframe, "bautismos") # `DatesExplorer` is initialized with the dataframe and the name of the dataframe
dates_explorer.report_column_dates("birth_date", save_report=True) # Declare the column to validate and optionally save the report
```

If `save_report` is `True`, it will be saved in the `reports` folder with the name of the dataframe and the column name. A separate report will be saved for valid and invalid dates.

## Columns with date values

- `bautismos.csv` -> `date` and `birth_date`
- `entierros.csv` -> `date`
- `matrimonios.csv` -> `date`

## Preprocessing methods

`DatesExplorer.report_column_dates` method validates the dates as is in the original dataframe. A `cleaning` parameter can be set to `True` to apply some basic cleaning to the values before validation.

This action will:

- Replace all `/` characters with `-`
- Remove all non-numeric characters (except for the `-` character)
- Replace all multiple spaces with a single space
- Trim spaces at the beginning and end of the string

A `normalization` parameter can be set to `True` to try to transform dates written in different formats to a valid date. Both parameters can be set to `True` at the same time and the report will be saved with the suffix `_cleaned` and `_normalized` respectively.

## Cases

This are some of the cases found in the data and some suggestions to fix them:

### "False" dates

Dates that not exist in the Gregorian calendar, for instance:

- "1790-11-31"
- "1793-02-29"
- "1916-09-31"
- "1904-09-31"
- "1894-02-29"

Due to the impossibility to known with certainty if the mistaked date comes from a transcription error or from the original document, this case will be handled by replacing the date for its nearest past valid date. For example:

- "1790-11-31" -> "1790-11-30"
- "1793-02-29" -> "1793-02-28"
- "1916-09-31" -> "1916-09-30"
- "1904-09-31" -> "1904-09-30"
- "1894-02-29" -> "1894-02-28"

