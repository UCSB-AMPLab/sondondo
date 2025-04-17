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

## Cases

This are some of the cases found in the data and some suggestions to fix them:

### "False" dates

Dates that not exist in the Gregorian calendar, for instance:

- "1790-11-31"
