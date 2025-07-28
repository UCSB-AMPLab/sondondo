import spacy
import pandas as pd
import numpy as np
from typing import List, Union
import re

class PlaceExtractor:
    def __init__(self):
        """Initialize the PlaceExtractor with the Spanish NLP model"""
        self.nlp = spacy.load("es_core_news_md")
        
    def extract_places_from_text(self, text: str) -> Union[str, float]:
        """Extract place names from a single text string"""
        if pd.isna(text) or not isinstance(text, str) or not text.strip():
            return np.nan

        text = re.sub(r'[\[\]\.]', '', text)

        try:
            doc = self.nlp(text)
            places = []
            for ent in doc.ents:
                if ent.label_ in ["LOC"]:  # LOC = location
                    places.append(ent.text.strip())
            return '|'.join(places) if places else np.nan
        except Exception as e:
            print(f"Error processing text '{text}': {e}")
            return np.nan

    def extract_places_per_row(self, series: pd.Series) -> pd.Series:
        """Extract places for each row, returning a Series of lists"""
        return series.apply(self.extract_places_from_text)


