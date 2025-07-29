import numpy as np
from helpers.NamesManager import NamesManager
from helpers.LogerHandler import setup_logger
from helpers.ColumnManager import ColumnManager
import pandas as pd
from pathlib import Path
import pytest

datasets_and_columns = {
    "bautismos": {"csv_file": "data/raw/bautismos.csv",
                  "mapping_file": "data/mappings/bautismosMapping.json",
        "columns": ["baptized_name",
                  "father_name",
                  "father_lastname",
                  "mother_name",
                  "mother_lastname",
                  "godfather_name",
                  "godfather_lastname",
                  "godmother_name",
                  "godmother_lastname",]},
    "entierros": {"csv_file": "data/raw/entierros.csv",
                  "mapping_file": "data/mappings/entierrosMapping.json",
                  "columns": ["deceased_name",
                  "deceased_lastname",
                  "father_name",
                  "father_lastname",
                  "mother_name",
                  "mother_lastname",
                  "husband_name",
                  "wife_name"]},
    "matrimonios": {"csv_file": "data/raw/matrimonios.csv",
                    "mapping_file": "data/mappings/matrimoniosMapping.json",
                    "columns": ["groom_name",
                    "groom_lastname",
                    "groom_father_name",
                    "groom_father_lastname",
                    "groom_mother_name",
                    "groom_mother_lastname",
                    "bride_name",
                    "bride_lastname",
                    "bride_father_name",
                    "bride_father_lastname",
                    "bride_mother_name",
                    "bride_mother_lastname",
                    "godparent_1_name",
                    "godparent_1_lastname",
                    "godparent_2_name",
                    "godparent_2_lastname",
                    "godparent_3_name",
                    "godparent_3_lastname",
                    "witness_1_name",
                    "witness_1_lastname",
                    "witness_2_name",
                    "witness_2_lastname",
                    "witness_3_name",
                    "witness_3_lastname",
                    "witness_4_name",
                    "witness_4_lastname"]},
}

def test_name_manager():
    """
    Test the NamesManager class for different datasets.
    This test only checks that the module runs without errors.

    A simple assertion is made to ensure that the cleaned series is a pandas Series, that it has the same
    length as the original DataFrame, and that no uncleaned terms remain.
    """
    logger = setup_logger("test_name_manager")
    
    # Iterate through each dataset and its corresponding columns
    for dataset, info in datasets_and_columns.items():
        csv_file = info["csv_file"]
        mapping_file = info["mapping_file"]
        columns = info["columns"]
        
        # Create a ColumnManager instance
        column_manager = ColumnManager()
        
        # Harmonize the columns using the mapping
        df_harmonized = column_manager.harmonize_columns(csv_file, mapping_file)
        
        # Initialize NamesManager with the harmonized DataFrame
        names_manager = NamesManager()
        
        # Process each column in the dataset
        for column in columns:
            cleaned = names_manager.clean_series(df_harmonized[column], label=column)
            assert isinstance(cleaned, pd.Series)
            assert cleaned.shape[0] == df_harmonized.shape[0]

            # Optional: assert no uncleaned terms remain
            assert not cleaned.dropna().str.contains(r"sic|ilegible", case=False, regex=True).any()

@pytest.fixture
def manager():
    return NamesManager()

@pytest.mark.parametrize("input_name,expected", [
    ("(sic)", None),
    ("[ilegible]", None),
    ("N. de la Cruz", "de la cruz"),
    ('"no conocido"', None),
    ("Condori, Ynes", "ynes condori"),
    ("Pablo Ilegible", "pablo"),
    ("Pedro [Ilegible]", "pedro"),
    ("Ynes N/A", "ynes"),
    ("Alfredo {sic}", "alfredo"),
    ("Arango, Juan Francisco Rejis", "juan francisco rejis arango"),
    ("Huallapatuiro, Maria Natibida", "maria natibida huallapatuiro"),
])
def test_clean_name(manager, input_name, expected):
    """
    Validate the clean_name function with various test cases.
    """
    assert manager.clean_name(input_name) == expected

def test_clean_series_basic(manager):
    """
    Test the clean_series method with a basic example.
    """
    series = pd.Series(["Condori, Ynes", "Pedro [ilegible]", None, "N. Maria"])
    cleaned = manager.clean_series(series)

    expected = pd.Series(["ynes condori", "pedro", None, "maria"])
    pd.testing.assert_series_equal(cleaned, expected)
    

def test_clean_name_non_string(manager):
    """
    Test the clean_name method with non-string inputs.
    """
    assert manager.clean_name("") is None
    assert manager.clean_name(None) is None
    assert manager.clean_name(123) is None
    assert manager.clean_name(np.nan) is None

def test_clean_name_format(manager):
    """
    Test the clean_name method with various formats.
    """

    name = manager.clean_name("González, María (sic)")
    assert name == "maría gonzález"
    assert name.islower()
    assert "sic" not in name
    assert "ilegible" not in name