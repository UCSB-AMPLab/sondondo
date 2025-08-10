import numpy as np
import pandas as pd
import re
from typing import Union, List

from actions.generators import GenderInferrer, InferCondition


class PersonaExtractor:
    def __init__(self, dataframes: List[pd.DataFrame], destination_dir: str = "../data/interim"):
        self.dataframes = dataframes
        self.destination_dir = destination_dir

    def extract_personas(self, person_element_pattern: Union[str, re.Pattern] = r"(^[A-Za-z]*_[\d]?_?)([A-Za-z]*_?[\w\d]*)"):

        person_element_pattern = re.compile(person_element_pattern)

        persona_entities_prefixes = [
            'baptized',
            'bride',
            'deceased',
            'father',
            'godfather',
            'godmother',
            'godparent',
            'groom',
            'husband',
            'mother',
            'wife',
            'witness'
        ]

        personas = []
        persona_counter = 1

        for df in self.dataframes:
            
            event_type = self._get_event_type(df)

            for index, row in df.iterrows():

                if row['event_type'] == event_type:
                    event_idno = f"{event_type.lower()}-{int(index) + 1}"
                    
                    personas_data = {}

                    for column_name in row.index:
                        match = re.search(person_element_pattern, column_name)
                        if match:

                            prefix = match.group(1)
                            attribute = match.group(2)

                            remove_pattern = re.compile(r"\d")
                            prefix = remove_pattern.sub("", prefix).strip("_")

                            if prefix in persona_entities_prefixes:
                                if prefix not in personas_data:
                                    personas_data[prefix] = {
                                        'event_idno': event_idno,
                                        'persona_type': prefix
                                    }

                                attribute_clean = attribute.strip("_")
                                personas_data[prefix][attribute_clean] = row[column_name]

                    if event_type and event_type.lower() == 'matrimonio':
                        personas_data = self._extract_embedded_parents(
                            personas_data,
                            event_idno
                        )


                    for persona in personas_data.values():
                        if pd.notna(persona.get('name')) and pd.notna(persona.get('lastname')):
                            persona['persona_idno'] = f"persona-{persona_counter}"
                            persona_counter += 1
    
                            personas.append(persona)

        personas_dataframe = pd.DataFrame.from_records(personas)

        # bulk inferences
        personas_dataframe['gender'] = GenderInferrer.GenderInferrer(personas_dataframe['name']).infer_from_names()
        personas_dataframe[['social_condition', 'legitimacy_status', 'marital_status']] = InferCondition.AttributeNormalizer(mapping_file="../data/mappings/conditionMapping.json").extract_all_attributes(personas_dataframe['social_condition'])
        personas_dataframe[['social_condition', 'legitimacy_status', 'marital_status']] = InferCondition.AttributeNormalizer(mapping_file="../data/mappings/conditionMapping.json").extract_all_attributes(personas_dataframe['legitimacy_status'])
        personas_dataframe[['social_condition', 'legitimacy_status', 'marital_status']] = InferCondition.AttributeNormalizer(mapping_file="../data/mappings/conditionMapping.json").extract_all_attributes(personas_dataframe['marital_status'])

        # remove empty columns
        personas_dataframe = personas_dataframe.dropna(axis=1, how='all')

        return personas_dataframe


    def _get_event_type(self, df):
        # Logic to extract event type from the DataFrame
        return df['event_type'].iloc[0] if 'event_type' in df.columns else None

    def _extract_embedded_parents(self, personas_data, event_idno):

        for persona_type in ['groom', 'bride']:
            if persona_type in personas_data:
                persona = personas_data[persona_type]

                father_data = {}
                mother_data = {}

                for attr in list(persona.keys()):
                    if attr.startswith('father_'):
                        clean_attr = attr.replace('father_', '')
                        father_data[clean_attr] = persona.pop(attr)
                    elif attr.startswith('mother_'):
                        clean_attr = attr.replace('mother_', '')
                        mother_data[clean_attr] = persona.pop(attr)

                if any(pd.notna(value) for value in father_data.values()):
                    father_key = f"father_of_{persona_type}"
                    personas_data[father_key] = {
                        'event_idno': event_idno,
                        'persona_type': father_key,
                        **father_data
                    }

                if any(pd.notna(value) for value in mother_data.values()):
                    mother_key = f"mother_of_{persona_type}"
                    personas_data[mother_key] = {
                        'event_idno': event_idno,
                        'persona_type': mother_key,
                        **mother_data
                    }

        return personas_data

if __name__ == "__main__":
    bautismos = pd.read_csv("data/clean/bautismos_clean.csv")
    matrimonios = pd.read_csv("data/clean/matrimonios_clean.csv")
    entierros = pd.read_csv("data/clean/entierros_clean.csv")

    extractor = PersonaExtractor([bautismos, matrimonios, entierros])
    personas = extractor.extract_personas()

    personas.to_csv("data/interim/personas_extracted.csv", index=False)