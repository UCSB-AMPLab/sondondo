# The People of Aucará (1760–1921)  
### A Dataset of Individuals Reconstructed from Parish Records of the Sondondo Valley, Peru

## Summary

This repository contains a structured dataset derived from sacramental records preserved in the parish archive of Aucará in the Sondondo Valley (Ayacucho, Peru). The dataset covers the period 1760–1921 and contains 10,251 event records, consisting of:

- **6,340 baptisms** (1790–1902)  
- **1,719 marriages** (1760–1921)  
- **2,192 burials** (1846–1921)

The original records were transcribed from digitized images of parish registers, collected directly from the archive holdings. The artifacts are not publicly available. These records were subsequently processed through a series of cleaning, normalization, and harmonization procedures. These transformations can be reproduced by running the Jupyter notebooks included in the `project_code/` directory, which document the data transformation workflow. The resulting dataset is structured to facilitate probabilistic record linkage and prosopographical analysis of individuals mentioned across the sacramental records.

Beyond the sacramental records themselves, the dataset also includes derived person-level entities, enabling person-centered analysis and future reconstruction of individuals across multiple records.

---

# Repository Structure

The repository is organized to reflect the different stages of the data transformation workflow.

```
data/
├── raw/        # Original structured transcriptions of parish records
├── interim/    # Intermediate datasets generated during normalization
├── clean/      # Final cleaned datasets used for analysis
└── mappings/   # Mapping files used for harmonization and normalization
```

### Raw Data

The `raw/` directory contains the initial structured transcriptions of the parish records. These were exported from the spreadsheets used during data capture and represent the unprocessed form of the data directly taken from the parish registers:

- `bautismos.csv`
- `matrimonios.csv`
- `entierros.csv`
- `raw_places.csv`

---

### Interim Data

The `interim/` directory contains datasets generated during the normalization process. These files document intermediate transformations applied during data cleaning, term extraction, and place standardization.

Examples include:

- normalized versions of the sacramental tables  
- extracted person references  
- standardized geographic descriptors  
- diagnostic outputs from extraction procedures  

---

### Clean Data

The primary dataset for reuse is located in the `data/clean/` directory:

- `bautismos_clean.csv`
- `matrimonios_clean.csv`
- `entierros_clean.csv`
- `personas.csv`
- `unique_places.csv`

These tables represent the normalized and analysis-ready version of the dataset.

The `personas.csv` file contains **individual entities extracted from the sacramental records**, with contextual information about their roles within each record (e.g., baptized child, parent, witness).

The `unique_places.csv` file contains standardized geographic locations mentioned in the records, along with their geocoded coordinates and links to external gazetteers.

---

### Mapping Files

The `mappings/` directory contains configuration files used during the normalization process. These mappings standardize column names, social status categories, and geographic references across the three record types.

Examples include:

- `bautismosMapping.json`
- `matrimoniosMapping.json`
- `entierrosMapping.json`
- `conditionMapping.json`
- `places_types.json`

---

## Metadata Dictionary

This metadata dictionary provides comprehensive documentation for all datasets in the `data/clean/` folder. Each section includes the dataset structure, a description of the table's purpose, and detailed field-level documentation with expected data types and descriptions.

The datasets represent historical parish records from Sondondo, Peru, covering vital events (baptisms, marriages, and burials) as well as derived entities (places and personas). All records have been cleaned, normalized, and harmonized to facilitate analysis and integration.

**Missing values:** Fields with no recorded information are represented as empty cells in all tables. No explicit placeholder code (e.g., `NA`, `null`) is used.

### Baptisms (`bautismos_clean.csv`)

| Property     | Expected Type | Description |
|--------------|---------------|-------------|
| file      | Text          | Source file name from which the record was extracted |
| identifier | Text          | Sequential identifier for the baptism event |
| event_type | Text          | Type of event (`Bautizo`) |
| event_date | Date          | Date of the baptism event in ISO 8601 format |
| baptized_name | Text       | Normalized first and middle name(s) of the baptized individual |
| baptized_lastname | Text   | Normalized or inferred surname(s) of the baptized individual |
| baptized_birth_place | Text   | Place of birth of the baptized individual |
| baptized_birth_date | Date    | Date of birth of the baptized individual in ISO 8601 format |
| baptized_legitimacy_status | Text | Legitimacy status at birth (`legitimo`, `ilegitimo`) |
| father_name | Text         | Normalized name of the father |
| father_lastname | Text     | Normalized or inferred surname(s) of the father |
| father_social_condition | Text  | Social, ethnical, or political marker of the father (`mestizo`, `indio`, `tributario`, `vecino`) |
| mother_name | Text         | Normalized name of the mother |
| mother_lastname | Text     | Normalized or inferred surname(s) of the mother |
| mother_social_condition | Text  | Social, ethnical, or political marker of the mother (`mestizo`, `indio`, `tributario`, `vecino`) |
| parents_social_condition | Text | Combined social condition of both parents |
| godfather_name | Text     | Normalized name of the godfather |
| godfather_lastname | Text | Normalized or inferred surname(s) of the godfather |
| godfather_social_condition | Text | Social, ethnical, or political marker of the godfather (`mestizo`, `indio`, `tributario`, `vecino`) |
| godmother_name | Text     | Normalized name of the godmother |
| godmother_lastname | Text | Normalized or inferred surname(s) of the godmother |
| godmother_social_condition | Text | Social, ethnical, or political marker of the godmother (`mestizo`, `indio`, `tributario`, `vecino`) |
| event_place | Text        | Place where the baptism event took place |
| event_geographic_descriptor_1 | Text | Place or location mentioned in the record |
| event_geographic_descriptor_2 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_3 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_4 | Text | Additional place or location mentioned in the record |

### Marriages (`matrimonios_clean.csv`)

The `marriages` table contains cleaned and standardized records of marriage events extracted from parish registers. Each row represents a unique marriage event with associated attributes for both spouses, their families, witnesses, and godparents.

| Property     | Expected Type | Description |
|--------------|---------------|-------------|
| file      | Text          | Source file name from which the record was extracted |
| identifier | Text          | Sequential identifier for the marriage event |
| event_type | Text          | Type of event (`Matrimonio`) |
| event_date | Date          | Date of the marriage event in ISO 8601 format |
| husband_name | Text       | Normalized first and middle name(s) of the husband |
| husband_lastname | Text   | Normalized or inferred surname(s) of the husband |
| husband_social_condition | Text  | Social, ethnical, or political marker of the husband (`mestizo`, `indio`, `tributario`, `vecino`, `don`) |
| husband_marital_status | Text | Marital status of the husband at the time of marriage (`soltero`, `viudo`) |
| husband_birth_date | Date    | Date of birth of the husband in ISO 8601 format |
| husband_birth_place | Text   | Place of birth of the husband |
| husband_resident_in | Text   | Recorded place of residence of the husband at the time of the event |
| husband_legitimacy_status | Text | Legitimacy status of the husband at birth (`legítimo`, `ilegitimo`, `natural`) |
| husband_father_name | Text  | Normalized name of the husband's father |
| husband_father_lastname | Text | Normalized or inferred surname(s) of the husband's father |
| husband_father_social_condition | Text | Social, ethnical, or political marker of the husband's father (`mestizo`, `indio`, `tributario`, `vecino`, `don`) |
| husband_mother_name | Text  | Normalized name of the husband's mother |
| husband_mother_lastname | Text | Normalized or inferred surname(s) of the husband's mother |
| husband_mother_social_condition | Text | Social, ethnical, or political marker of the husband's mother (`mestizo`, `indio`, `tributario`, `vecino`, `doña`) |
| wife_name | Text         | Normalized first and middle name(s) of the wife |
| wife_lastname | Text     | Normalized or inferred surname(s) of the wife |
| wife_social_condition | Text  | Social, ethnical, or political marker of the wife (`mestizo`, `indio`, `tributario`, `vecino`, `doña`) |
| wife_marital_status | Text | Marital status of the wife at the time of marriage (`soltera`, `viuda`) |
| wife_birth_date | Date    | Date of birth of the wife in ISO 8601 format |
| wife_birth_place | Text   | Place of birth of the wife |
| wife_resident_in | Text   | Recorded place of residence of the wife at the time of the event |
| wife_legitimacy_status | Text | Legitimacy status of the wife at birth (`legítima`, `ilegitima`, `natural`) |
| wife_father_name | Text    | Normalized name of the wife's father |
| wife_father_lastname | Text | Normalized or inferred surname(s) of the wife's father |
| wife_father_social_condition | Text | Social, ethnical, or political marker of the wife's father (`mestizo`, `indio`, `tributario`, `vecino`, `don`) |
| wife_mother_name | Text    | Normalized name of the wife's mother |
| wife_mother_lastname | Text | Normalized or inferred surname(s) of the wife's mother |
| wife_mother_social_condition | Text | Social, ethnical, or political marker of the wife's mother (`mestizo`, `indio`, `tributario`, `vecino`, `doña`) |
| godparent_1_name | Text   | Normalized name of the first godparent |
| godparent_1_lastname | Text | Normalized or inferred surname(s) of the first godparent |
| godparent_1_social_condition | Text | Social, ethnical, or political marker of the first godparent (`mestizo`, `indio`, `tributario`, `vecino`, `don`, `doña`) |
| godparent_2_name | Text   | Normalized name of the second godparent |
| godparent_2_lastname | Text | Normalized or inferred surname(s) of the second godparent |
| godparent_2_social_condition | Text | Social, ethnical, or political marker of the second godparent (`mestizo`, `indio`, `tributario`, `vecino`, `don`, `doña`) |
| godparent_3_name | Text   | Normalized name of the third godparent (when applicable) |
| godparent_3_lastname | Text | Normalized or inferred surname(s) of the third godparent (when applicable) |
| witness_1_name | Text     | Normalized name of the first witness |
| witness_1_lastname | Text | Normalized or inferred surname(s) of the first witness |
| witness_2_name | Text     | Normalized name of the second witness |
| witness_2_lastname | Text | Normalized or inferred surname(s) of the second witness |
| witness_3_name | Text     | Normalized name of the third witness (when applicable) |
| witness_3_lastname | Text | Normalized or inferred surname(s) of the third witness (when applicable) |
| witness_4_name | Text     | Normalized name of the fourth witness (when applicable) |
| witness_4_lastname | Text | Normalized or inferred surname(s) of the fourth witness (when applicable) |
| event_place | Text        | Place where the marriage event took place |
| event_geographic_descriptor_1 | Text | Place or location mentioned in the record |
| event_geographic_descriptor_2 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_3 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_4 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_5 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_6 | Text | Additional place or location mentioned in the record |

### Burials (`entierros_clean.csv`)

The `burials` table contains cleaned and standardized records of burial events extracted from parish registers. Each row represents a unique burial event with associated attributes such as date, location, and information about the deceased individual and their surviving family members.

| Property     | Expected Type | Description |
|--------------|---------------|-------------|
| file      | Text          | Source file name from which the record was extracted |
| identifier | Text          | Sequential identifier for the burial event |
| event_type | Text          | Type of event (`Entierro`) |
| event_date | Date          | Date of the burial event in ISO 8601 format |
| doctrine   | Text          | Name of the parish or doctrine where the burial was registered |
| event_place | Text        | Place where the burial event took place |
| deceased_name | Text       | Normalized first and middle name(s) of the deceased individual |
| deceased_lastname | Text   | Normalized or inferred surname(s) of the deceased individual |
| deceased_birth_date | Date    | Date of birth of the deceased individual in ISO 8601 format |
| deceased_birth_place | Text   | Place of birth of the deceased individual |
| deceased_social_condition | Text  | Social, ethnical, or political marker of the deceased (`mestizo`, `indio`, `tributario`, `vecino`, `don`, `doña`) |
| deceased_marital_status | Text | Marital status of the deceased at the time of death (`soltero/soltera`, `casado/casada`, `viudo/viuda`, `marido que fue`, `mujer que fue`) |
| deceased_legitimacy_status | Text | Legitimacy status of the deceased at birth (`legítimo`, `ilegitimo`, `natural`) |
| father_name | Text         | Normalized name of the deceased's father |
| father_lastname | Text     | Normalized or inferred surname(s) of the deceased's father |
| mother_name | Text         | Normalized name of the deceased's mother |
| mother_lastname | Text     | Normalized or inferred surname(s) of the deceased's mother |
| husband_name | Text        | Normalized name of the deceased's husband (when deceased was married) |
| wife_name | Text           | Normalized name of the deceased's wife (when deceased was married) |
| burial_place | Text        | Specific location where the deceased was buried |
| event_geographic_descriptor_1 | Text | Place or location mentioned in the record |
| event_geographic_descriptor_2 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_3 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_4 | Text | Additional place or location mentioned in the record |
| husband_lastname | Text    | Normalized or inferred surname(s) of the deceased's husband |
| wife_lastname | Text       | Normalized or inferred surname(s) of the deceased's wife |

## Places (`unique_places.csv`)

The places table represents a controlled vocabulary of geographic locations extracted from all event records and normalized through a combination of manual curation and automated gazetteer matching. Each place has been geocoded and linked to external authorities (GeoNames, Getty Thesaurus of Geographic Names) when possible, enabling spatial analysis and visualization of the historical records.

| Property     | Expected Type | Description |
|--------------|---------------|-------------|
| place_id | Numeric        | Unique identifier for the place |
| manually_normalized_place | Text | Standardized place name assigned during data cleaning |
| standardize_label | Text         | Name standardized using external gazetteers |
| language   | Text          | Language of the place name (e.g., `es`, `en`) |
| latitude   | Numeric       | Latitude coordinate of the place |
| longitude  | Numeric       | Longitude coordinate of the place |
| source | Text               | Source gazetteer used for standardization (e.g., `geonames`, `tgn`) |
| id  | Text          | Identifier of the place in the source gazetteer |
| uri | Text          | URI linking to the place in the source gazetteer |
| country_code | Text       | ISO country code of the place |
| part_of | Text         | Higher-level administrative division the place belongs to |
| part_of_uri | Text     | URI of the higher-level administrative division |
| confidence | Numeric    | Confidence score of the place standardization (0-100) |
| threshold | Numeric     | Threshold used for the place standardization |
| match_type | Text      | Type of match made during standardization (e.g., `exact`, `fuzzy`) |
| mentioned_as | Text   | Original text mention of the place in the records |

## Personas (`personas.csv`)

Personas represent individual person mentions extracted from all event records and restructured into a person-centric format. Unlike the event tables which are organized around ceremonies, this table focuses on individuals and their attributes as documented across multiple events. Each row represents a unique person mention extracted from a record--prior to any clustering or aggregation through probabilistic record linkage (PRL)--with inferred demographic information including name, birth and death details, and places. Multiple mentions may refer to the same historical individual.

| Property   | Expected Type | Description |
|------------|---------------|-------------|
| event_idno | Text          | Unique identifier for the event mention |
| original_identifier | Text          | Original identifier from the source document |
| persona_idno | Text        | Unique identifier for the persona entity |
| name       | Text          | Normalized first and middle name(s) |
| lastname   | Text          | Normalized or inferred surname(s) |
| persona_type | Text          | Type of persona (e.g., `baptized`, `parent`, `godparent`) |
| birth_date | Date          | Recorded or inferred date of birth in ISO 8601 format |
| birth_place | Text       | Place of birth |
| death_date | Date          | Recorded or inferred date of death in ISO 8601 format |
| death_place | Text       | Place of death |
| gender     | Text          |  Inferred gender (`male`, `female`, `unknown`) |
| resident_in | Text        | Recorded place of residence at the time of the event |
| legitimacy_status | Text    | Legitimacy status at birth (`legitimo`, `ilegitimo`) |
| marital_status | Text      | Marital status at the time of the event (`soltero`, `casado`) |
| social_condition | Text     | Social, ethnical, or political marker (`mestizo`, `indio`, `tributario`, `vecino`) |
---

## Methods

The dataset was processed through several stages of data cleaning and normalization.

### 1. Data Cleaning
Raw transcriptions were cleaned to remove empty rows, normalize column names, and correct obvious transcription inconsistencies.

### 2. Field Harmonization
Mapping files were used to standardize column names, social descriptors, and structural differences between the three sacramental record types.

### 3. Place Standardization
Geographic descriptors recorded in the parish registers were normalized and matched against standardized place references.

### 4. Entity Extraction
Individuals mentioned in the records were extracted and associated with specific roles (e.g., baptized child, parent, witness).

### 5. Dataset Generation
Cleaned records and extracted entities were combined to produce structured tables suitable for probabilistic record linkage and prosopographical analysis.

All transformations are documented in the Jupyter notebooks and Python modules contained in the `project_code/` directory.

---

# Data Sources

The dataset was compiled from sacramental registers preserved in the Archive of the Parish of Aucará in the Sondondo Valley, Peru.

Data capture involved manual transcription from digitized images of the original registers. Transcriptions were initially recorded using structured templates in shared spreadsheets. The data then underwent manual review and computational normalization to ensure consistency.

Digitized images of the original registers are currently stored in a private repository and are not yet publicly available.

---

# Code and Software

Data processing was implemented in *Python (version 3.8 or later)* using the following primary libraries:

- pandas  
- numpy  
- pathlib  
- spacy  
- georesolver  

The repository includes Jupyter notebooks and Python modules that document the workflow used to transform raw transcriptions into the cleaned dataset.

These scripts implement procedures for:

- data cleaning  
- field normalization  
- geographic standardization  
- entity extraction  

---

# Citation

Melo Flórez, J. A., Ramos, G., de la Puente Luna, J. C., Cobo Betancourt, J., Ancho, B., Xue, D., Ayinaparthi, S., Roque, G., & Gonzales Rojas, E. (2026). The People of Aucará (1760–1921): A Dataset of Individuals Reconstructed from Parish Records of the Sondondo Valley, Peru (Version 1.0.0) [Data set]. https://doi.org/10.5281/zenodo.18969893
---

# License

This repository uses a dual license:

- **Data** (`data/` directory): [Creative Commons Attribution–NonCommercial–ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) — see `LICENSE-DATA`.
- **Code** (`project_code/` directory): [MIT License](https://opensource.org/licenses/MIT) — see `LICENSE`.
