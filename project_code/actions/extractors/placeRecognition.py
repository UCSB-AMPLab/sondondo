import spacy
import pandas as pd
import numpy as np
from typing import List, Union, Optional
import re
import georesolver

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
    def __init__(self, dataframes: List[pd.DataFrame], places_map: Optional[str] = None):
        self.dataframes = dataframes
        self.places_map = places_map

    def get_all_unique_places(self) -> np.ndarray:
        all_places = pd.concat(self.dataframes, ignore_index=True)

        all_unique_places = all_places.stack().unique() # type: ignore
        all_unique_places = all_unique_places[~pd.isna(all_unique_places)]

        # split places by '|' and flatten the list
        all_unique_places = [place.strip() for sublist in all_unique_places 
                    for place in str(sublist).split('|') if place.strip()]
        all_unique_places = np.unique(all_unique_places)

        return all_unique_places
    
    def resolve_places(self) -> pd.DataFrame:
        """Resolve places using the PlaceResolver"""
        
        params = {
            "verbose": False,
            "flexible_threshold": True,
            "flexible_threshold_value": 70,
            "lang": 'es'
        }
        if self.places_map:
            params["places_map_json"] = self.places_map

        services = [
            georesolver.WHGQuery(dataset="lugares13k_rel"), # Using `lugares13k_rel` dataset as first priority
            georesolver.GeoNamesQuery(),
            georesolver.TGNQuery(),
            georesolver.WikidataQuery()
        ]

        params["services"] = services
        resolver = georesolver.PlaceResolver(**params)
        
        all_unique_places = self.get_all_unique_places()

        map_places = pd.DataFrame({'place': all_unique_places})
        map_places['country'] = 'PE'
        map_places['place_type'] = 'city'
        results = resolver.resolve_batch(map_places, 'place', 'country', 'place_type', use_default_filter=True,
                                                        show_progress=True)

        map_places = pd.merge(map_places, results, how='left', on='place', suffixes=('', '_resolved'))

        return map_places
    

class AuthoritativePlaceResolver:
    def __init__(self, data: pd.DataFrame, places_map: Optional[str] = None):
        """
        data: a DataFrame with at least 'place' and 'manually_normalized_place' columns
        places_map: path to the JSON file containing the customized place types
        """
        self.data = data
        params = {
            "verbose": False,
            "flexible_threshold": True,
            "flexible_threshold_value": 70,
            "lang": 'es'
        }
        if places_map:
            params["places_map_json"] = places_map

        services = [
            georesolver.GeoNamesQuery(),
            georesolver.TGNQuery(),
            georesolver.WHGQuery(dataset="lugares13k_rel"),
            georesolver.WikidataQuery()
        ]

        params["services"] = services

        self.resolver = georesolver.PlaceResolver(**params)

    def resolve_places(self) -> pd.DataFrame:
        """Resolve authoritative places and add mentioned_as list"""

        mentions = self.data.groupby("manually_normalized_place")["place"] \
            .apply(lambda x: sorted(set(x.dropna()))) \
            .reset_index(name="mentioned_as")

        authoritative_places = self.data[["manually_normalized_place", "country", "place_type"]].drop_duplicates()

        resolved = self.resolver.resolve_batch(
            authoritative_places.rename(columns={"manually_normalized_place": "place"}),
            place_column="place",
            country_column="country",
            place_type_column="place_type",
            use_default_filter=True,
            show_progress=True,
            return_df=True
        )

        resolved = resolved.rename(columns={"place": "manually_normalized_place"}) # type: ignore
        resolved = pd.merge(resolved, mentions, on="manually_normalized_place", how="left")

        resolved = resolved.dropna(subset=["manually_normalized_place"])

        return resolved
