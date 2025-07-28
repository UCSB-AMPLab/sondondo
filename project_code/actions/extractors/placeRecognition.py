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


class MapPlaces:
    def __init__(self, dataframes: List[pd.DataFrame]):
        self.dataframes = dataframes

    def get_all_unique_places(self) -> np.ndarray:
        all_places = pd.concat(self.dataframes, ignore_index=True)

        all_unique_places = all_places.stack().unique() # type: ignore
        all_unique_places = all_unique_places[~pd.isna(all_unique_places)]

        # split places by '|' and flatten the list
        all_unique_places = [place.strip() for sublist in all_unique_places 
                    for place in str(sublist).split('|') if place.strip()]
        all_unique_places = np.unique(all_unique_places)

        return all_unique_places