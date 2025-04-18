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

A `standardized` parameter can be set to `True` to try to transform dates written in different formats to a valid date. If this parameter is used, it's not necessary to use the `cleaning` parameter as the method will apply both actions.

> ⚠️ Applying this method slightly increases the number of valid dates. However, it also removes all textual clues that could be used to infer a birth date.

## Cases

These are some of the cases found in the data and some suggestions to fix them:

### "False" dates

Dates that not exist in the Gregorian calendar, for instance:

- "1790-11-31"
- "1793-02-29"
- "1916-09-31"
- "1904-09-31"
- "1894-02-29"

Due to the impossibility to known if the mistaked date comes from a transcription error or from the original document, this case will be handled by replacing the date for its nearest past valid date. For example:

- "1790-11-31" -> "1790-11-30"
- "1793-02-29" -> "1793-02-28"
- "1916-09-31" -> "1916-09-30"
- "1904-09-31" -> "1904-09-30"
- "1894-02-29" -> "1894-02-28"

### Partial dates

Dates that are missing one or more components, for instance:

- "1793-02-..."
- "1796-03-.."
- "17...-08-22"
- "1800-10-..."
- 1834-10-xx
- "1834-xx-11"
- "1834-xx-11"
- "1834-xx-13"
- "1896-07-[roto]"
- "1900-04-xx"
- "02/1800"
- "01/1800"
- "02/1800"

Based on the report, the following strategies can be applied to standardize partial or malformed date values:

- Use inferred placeholders when possible

    If the year and month are present but the day is missing, assume the day to be the first of the month.

    Example: "1800-10-..." → "1800-10-01"

- If the month or year is missing, use the nearest valid value

    For example:

    "17...-08-22" → "1797-08-22" (from the previous date available "1797-08-28")

    "1834-xx-11" → "1834-10-11" (from the previous date available "1834-10-20")

- If the format is `%m/%Y`, reverse the order and fill the day with the first of the month

    Example: "02/1800" → "1800-02-01"

### Invalid values

All values (textual or numeric) that do not contribute to infer a valid date will be converted to `NULL`.

For example:

- "-"
- "[ilegible]"
- "Sin fecha"

### Excel date values

We have found some cases where the date is represented as an Excel serial number (`matrimonios.csv`):

- 6443
- 6445

Date values can be converted to a valid date using the following script:

```python
from datetime import datetime, timedelta

excel_origin = datetime(1899, 12, 30)
serials = [6443, 6445]
dates = [excel_origin + timedelta(days=s) for s in serials]
print(dates)
```

This will return the following dates:

- "1917-08-21"
- "1917-08-23"

Which are totally consistent with the previous and following dates in the dataset.

