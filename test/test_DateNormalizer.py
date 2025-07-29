from datetime import datetime
from helpers.DateNormalizer import DateNormalizer
from helpers.ColumnManager import ColumnManager
import pandas as pd
import pytest
import logging
from pathlib import Path


LOGS_DIR = Path(__file__).parent.parent / "logs" / "test_results"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def setup_test_logger(test_name):
    """Set up a logger for a specific test"""
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.INFO)
    
    # Create a file handler
    log_file = LOGS_DIR / f"{test_name}.log"
    fh = logging.FileHandler(log_file, mode='w')
    fh.setLevel(logging.INFO)
    
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(fh)
    
    return logger

test_cases = {
    "case_type": [
        "false date", "false date", "false date", "false date", "false date",
        "partial date", "partial date", "partial date", "partial date", "partial date",
        "partial date", "partial date", "partial date", "partial date", "partial date",
        "partial date", "partial date", "partial date",
        "invalid date", "invalid date", "invalid date",
        "excel date", "excel date"
    ],
    "case": [
        "1790-11-31", "1793-02-29", "1916-09-31", "1904-09-31", "1894-02-29",
        "1793-02-...", "1796-03-..", "17...-08-22", "1800-10-...", "1834-10-xx",
        "1834-xx-11", "1834-xx-13", "1896-07-[roto]", "1900-04-xx", "02/1800",
        "01/1800", "02/1800", "1834-xx-11",
        "-", "[ilegible]", "Sin fecha",
        "6443", "6445"
    ],
    "expected": [
        "1790-11-30", "1793-02-28", "1916-09-30", "1904-09-30", "1894-02-28",
        "1793-02-01", "1796-03-01", "1796-08-22", "1800-10-01", "1834-10-01",
        "1834-03-11", "1834-03-13", "1896-07-01", "1900-04-01", "1800-02-01",
        "1800-01-01", "1800-02-01", "1834-07-11",
        None, None, None,
        "1917-08-21", "1917-08-23"
    ]
}

def test_date_normalizer():
    """Test the DateNormalizer class with all test cases"""
    logger = setup_test_logger("test_date_normalizer")
    
    # Create a series from the test cases
    test_series = pd.Series(test_cases["case"])
    logger.info("Testing all cases at once")
    normalizer = DateNormalizer(test_series)
    results = normalizer.normalize()
    
    expected = pd.Series(test_cases["expected"])
    
    results_df = pd.DataFrame({
        'case_type': test_cases['case_type'],
        'input': test_cases['case'],
        'expected': test_cases['expected'],
        'actual': results
    })
    results_df.to_csv(LOGS_DIR / "all_cases_results.csv", index=False)
    logger.info(f"Results saved to {LOGS_DIR}/all_cases_results.csv")
    
    pd.testing.assert_series_equal(results, expected)

def test_date_normalizer_individual_cases():
    """Test individual cases to provide more detailed feedback"""
    logger = setup_test_logger("test_individual_cases")
    
    results = []
    for case_type, case, expected in zip(test_cases["case_type"], test_cases["case"], test_cases["expected"]):
        test_series = pd.Series([case])
        normalizer = DateNormalizer(test_series)
        result = normalizer.normalize().iloc[0]

        logger.info(f"Testing {case_type} case: '{case}'")
        logger.info(f"Expected: {expected}, Got: {result}")
        
        results.append({
            'case_type': case_type,
            'input': case,
            'expected': expected,
            'actual': result,
            'passed': result == expected
        })
        
        assert result == expected, f"Failed for {case_type} case '{case}': expected {expected}, got {result}"
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(LOGS_DIR / "individual_cases_results.csv", index=False)
    logger.info(f"Detailed results saved to {LOGS_DIR}/individual_cases_results.csv")

def test_false_dates():
    """Test specifically false dates normalization"""
    logger = setup_test_logger("test_false_dates")
    
    false_dates = [
        ("1790-11-31", "1790-11-30"),
        ("1793-02-29", "1793-02-28"),
        ("1916-09-31", "1916-09-30"),
        ("1904-09-31", "1904-09-30"),
        ("1894-02-29", "1894-02-28")
    ]
    
    results = []
    for input_date, expected in false_dates:
        test_series = pd.Series([input_date])
        normalizer = DateNormalizer(test_series)
        result = normalizer.normalize().iloc[0]
        
        logger.info(f"Testing false date: '{input_date}'")
        logger.info(f"Expected: {expected}, Got: {result}")
        
        results.append({
            'input': input_date,
            'expected': expected,
            'actual': result,
            'passed': result == expected
        })
        
        assert result == expected, f"Failed for false date '{input_date}': expected {expected}, got {result}"
    
    pd.DataFrame(results).to_csv(LOGS_DIR / "false_dates_results.csv", index=False)
    logger.info(f"False dates results saved to {LOGS_DIR}/false_dates_results.csv")

def test_missing_day():
    """Test this case separatelly"""
    logger = setup_test_logger("test_missing_day")

    missing_days = [
        ("1793-02-...", "1793-02-01"),
        ("1796-03-..", "1796-03-01"),
        ("1896-07-[roto]", "1896-07-01"),
        ("02/1800", "1800-02-01")
    ]

    results = []
    for input_date, expected in missing_days:
        test_series = pd.Series([input_date])
        normalizer = DateNormalizer(test_series)
        result = normalizer.normalize().iloc[0]

        logger.info(f"Testing missing day: '{input_date}'")
        logger.info(f"Expected: {expected}, Got: {result}")

        results.append({
            'input': input_date,
            'expected': expected,
            'actual': result,
            'passed': result == expected
        })

        assert result == expected, f"Failed for missing day '{input_date}': expected {expected}, got {result}"

    pd.DataFrame(results).to_csv(LOGS_DIR / "missing_days_results.csv", index=False)
    logger.info(f"Missing days results saved to {LOGS_DIR}/missing_days_results.csv")

def test_partial_dates():
    """Test specifically partial dates normalization"""
    logger = setup_test_logger("test_partial_dates")
    
    partial_dates = [
        ("1793-02-...", "1793-02-01"),
        ("1796-03-..", "1796-03-01"),
        ("17...-08-22", "1797-08-22"),
        ("1834-xx-11", "1834-10-11"),
        ("1896-07-[roto]", "1896-07-01"),
        ("02/1800", "1800-02-01")
    ]
    
    results = []
    for input_date, expected in partial_dates:
        test_series = pd.Series([input_date])
        normalizer = DateNormalizer(test_series)
        result = normalizer.normalize().iloc[0]
        
        logger.info(f"Testing partial date: '{input_date}'")
        logger.info(f"Expected: {expected}, Got: {result}")
        
        results.append({
            'input': input_date,
            'expected': expected,
            'actual': result,
            'passed': result == expected
        })
        
        assert result == expected, f"Failed for partial date '{input_date}': expected {expected}, got {result}"

    pd.DataFrame(results).to_csv(LOGS_DIR / "partial_dates_results.csv", index=False)
    logger.info(f"Partial dates results saved to {LOGS_DIR}/partial_dates_results.csv")

def test_invalid_values():
    """Test specifically invalid values normalization"""
    logger = setup_test_logger("test_invalid_values")
    
    invalid_values = ["-", "[ilegible]", "Sin fecha"]
    
    results = []
    for value in invalid_values:
        test_series = pd.Series([value])
        normalizer = DateNormalizer(test_series)
        result = normalizer.normalize().iloc[0]
        
        logger.info(f"Testing invalid value: '{value}'")
        logger.info(f"Expected: None, Got: {result}")
        
        results.append({
            'input': value,
            'expected': None,
            'actual': result,
            'passed': result is None
        })
        
        assert result is None, f"Failed for invalid value '{value}': expected None, got {result}"

    pd.DataFrame(results).to_csv(LOGS_DIR / "invalid_values_results.csv", index=False)
    logger.info(f"Invalid values results saved to {LOGS_DIR}/invalid_values_results.csv")

def test_excel_dates():
    """Test specifically Excel date values normalization"""
    logger = setup_test_logger("test_excel_dates")
    
    excel_dates = [
        ("6443", "1917-08-21"),
        ("6445", "1917-08-23")
    ]
    
    results = []
    for input_date, expected in excel_dates:
        test_series = pd.Series([input_date])
        normalizer = DateNormalizer(test_series)
        result = normalizer.normalize().iloc[0]
        
        logger.info(f"Testing Excel date: '{input_date}'")
        logger.info(f"Expected: {expected}, Got: {result}")
        
        results.append({
            'input': input_date,
            'expected': expected,
            'actual': result,
            'passed': result == expected
        })
        
        assert result == expected, f"Failed for Excel date '{input_date}': expected {expected}, got {result}"

    pd.DataFrame(results).to_csv(LOGS_DIR / "excel_dates_results.csv", index=False)
    logger.info(f"Excel dates results saved to {LOGS_DIR}/excel_dates_results.csv")


def validate_dataset_column(df, column):
    logger = setup_test_logger("validate_dataset_column")
    logger.info(f"Validating dataset column: {column}")

    date_series = df[column]
    normalizer = DateNormalizer(date_series)
    normalized = normalizer.normalize()

    def is_valid(date):
        if pd.isna(date):
            return True
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    invalid_dates = normalized[~normalized.apply(is_valid)]

    if not invalid_dates.empty:
        logger.error(f"Invalid dates found in column '{column}': {invalid_dates.tolist()}")
        logger.info(f"Saving invalid dates to {LOGS_DIR}/invalid_dates.csv")
        invalid_dates.to_csv(LOGS_DIR / "invalid_dates.csv", index=False)
    else:
        logger.info(f"All dates in column '{column}' are valid.")
    logger.info(f"Validation completed for column '{column}'.")

    assert invalid_dates.empty, f"Invalid dates found in column '{column}': {invalid_dates.tolist()}"


def test_date_normalizer_integration():
    """Test the DateNormalizer class with a sample dataset"""
    logger = setup_test_logger("test_date_normalizer_integration")
    
    datasets = ["bautismos", "entierros", "matrimonios"]
    csv_paths = [Path(__file__).parent.parent / "data" / "raw" / f"{dataset}.csv" for dataset in datasets]
    mappings_paths = [Path(__file__).parent.parent / "data" / "mappings" / f"{dataset}Mapping.json" for dataset in datasets]

    for path, mapping_path in zip(csv_paths, mappings_paths):
        logger.info(f"Testing dataset: {path}")
        columnManager = ColumnManager()
        dataset = columnManager.harmonize_columns(path, mapping_path)
        logger.info(f"Dataset {dataset.columns} prepared for validation.")

        # Assuming the date column is named 'date' in the dataset
        date_column = "date"
        if date_column in dataset.columns:
            validate_dataset_column(dataset, date_column)
        else:
            logger.error(f"Date column '{date_column}' not found in dataset {path}.")
            assert False, f"Date column '{date_column}' not found in dataset {path}."

    logger.info("Integration test completed.")
    assert True, "Integration test passed."

if __name__ == "__main__":
    print("Test cases:")
    print(pd.DataFrame(test_cases))
    print(f"\nRunning tests... Results will be saved in {LOGS_DIR}")
    pytest.main([__file__, "-v"])
