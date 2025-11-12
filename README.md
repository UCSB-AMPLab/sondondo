# Identifying Unique Individuals through Probabilistic Record Linkage: A Case Study of Sondondo Valley Parish Records

Historical parish records provide insights into demographic, social, and familial patterns but often lack explicit unique identifiers, complicating efforts to track individuals across events. This project employs probabilistic record linkage methods to systematically identify unique individuals within a rich corpus of parish records from the Sondondo Valley, Peru, encompassing baptisms, marriages, and burials from 1760 to 1921. Leveraging contextual data—such as names, familial relationships, geographic locations, and event dates—this approach aims to reduce ambiguity, enabling historical and demographic analyses. Furthermore, network analysis techniques will refine matches, attempting to uncover familial and social connections within the historical community. This methodological framework could be replicated in other historical datasets where recognizing entities is challenging, enhancing digital collections through more robust and consistent record linkage.

## Data collection

Data was gathered from parish records of baptisms, marriages, and burials from the Sondondo Valley, Peru, covering the period from 1760 to 1921. Data capture involved manual transcription directly from digitized images of the original documents. All data was ingested into a shared Google Sheet pre-populated with a structured template for each record type. Post-collection, the data underwent manual review to identify and correct obvious inconsistencies and errors.

## Raw data

The raw data files are stored in the `data/raw` folder, containing:

- `bautismos.csv`: Baptism records. 6,341 entries. 36 columns.
- `matrimonios.csv`: Marriage records. 1,719 entries. 66 columns.
- `entierros.csv`: Burial records. 2,198 entries. 37 columns.

These CSV files were exported directly from the original Google Sheets used for transcription.

## Cleaned Data

The processed data files are available in the `data/clean` folder:

- `bautismos_clean.csv`: Cleaned baptism records with standardized columns and normalized data
- `matrimonios_clean.csv`: Cleaned marriage records with harmonized fields
- `entierros_clean.csv`: Cleaned burial records with processed names and places

**Data Processing Achievements:**
- ✅ Column harmonization across all datasets
- ✅ Date normalization to YYYY-MM-DD format
- ✅ Name standardization using custom NamesNormalizer
- ✅ Geographic entity extraction using NER techniques
- ✅ Age inference and data validation
- ✅ Comprehensive quality audit and error reporting

## Personas Dataset

The `data/clean/personas.csv` dataset represents a consolidated view of all individuals mentioned across baptism, marriage, and burial records:

- **personas.csv**: Unified individual records extracted from all three record types
- Each row represents a unique person-record combination with role context
- Includes standardized names, relationships, dates, and geographic information
- Prepared for probabilistic record linkage and entity resolution

**Key Features:**
- Unified schema across all record types (baptisms, marriages, burials)
- Role-based extraction (child, parent, godparent, spouse, deceased, etc.)
- Preserved source record metadata for traceability
- Standardized name and place fields ready for matching algorithms

## Project Status

**Current Phase:** ✅ **Personas Dataset Creation Complete** (v0.2.0)

### Completed Milestones

#### Phase 1: Data Cleaning & Standardization ✅
- **Column Harmonization**: Standardized column names across all datasets using mapping configurations
- **Data Quality Improvements**: Normalized null values, dates, ages, and names
- **Advanced Processing**: Implemented NER for place recognition and geographic standardization
- **Quality Assurance**: Comprehensive audit system with data validation and error reporting
- **Output**: Clean, standardized datasets ready for record linkage (`data/clean/`)

**Datasets Processed:**
- **Baptisms**: 6,340 cleaned records
- **Marriages**: 1,719 cleaned records  
- **Burials**: 2,121 cleaned records
- **Total**: 10,180 historical records ready for analysis

#### Phase 2: Personas Dataset Creation ✅
- **Individual Extraction**: Systematically extracted all individuals from cleaned records
- **Role Contextualization**: Preserved individual roles (baptized, parent, godparent, spouse, deceased, etc.)
- **Schema Unification**: Harmonized fields across different record types
- **Metadata Preservation**: Maintained source record references and dates
- **Output**: Consolidated personas dataset ready for probabilistic matching

### Next Phases

```mathematica
✅ Initial Exploration & DB Setup
              │
              ▼
✅ Database Cleaning & Standardization
              │
              ▼
✅ Personas Dataset Creation
              │
              ▼
🔄 Probabilistic Record Linkage (In Progress)
              │
              ▼
🔮 Network Analysis & Validation
              │
              ▼
🔮 Manual Review & Quality Assurance
              │
              ▼
🔮 Final Data Export & Analysis
```

## Technical Contributions

### GeoResolver Library
As part of this research, we developed and published **[GeoResolver](https://pypi.org/project/georesolver/)**, a Python library for geographic entity resolution and coordinate lookup. This library emerged from our exploration of place name standardization and geographic data processing within the parish records.

**Key Features:**
- Geographic entity recognition and normalization
- Coordinate lookup and validation
- Place name standardization for historical data
- Caching mechanisms for improved performance

**Installation:**
```bash
pip install georesolver
```

The GeoResolver library is being actively used in this project for processing geographic descriptors and place names found in the historical records.

## Project Structure

```
sondondo/
├── data/
│   ├── raw/           # Original transcribed datasets
│   ├── clean/         # ✅ Processed, standardized datasets & personas
│   ├── interim/       # Intermediate processing files
│   └── mappings/      # Column and value mapping configurations
├── project_code/
│   ├── dataCleaning.ipynb    # ✅ Complete data cleaning pipeline
│   ├── personasCreation.ipynb # ✅ Personas extraction pipeline
│   ├── utils/               # Core utility classes
│   └── actions/            # Data processing modules
├── reports/          # Data quality and processing reports
└── test/            # Unit tests for processing modules
```

## Getting Started

### Prerequisites
- Python 3.8+
- pandas, numpy, pathlib
- georesolver (for geographic processing)

### Running the Data Processing Pipeline

**Step 1: Data Cleaning**
```
project_code/dataCleaning.ipynb
```
Complete pipeline from raw data to cleaned, standardized datasets.

**Step 2: Personas Extraction**
```
project_code/personasCreation.ipynb
```
Extracts and consolidates all individuals from cleaned records into a unified personas dataset.

### Key Processing Modules
- **ColumnManager**: Handles column harmonization using mapping files
- **DateNormalizer**: Standardizes date formats across datasets  
- **AgeInferrer**: Processes age-related fields and birthdates
- **NamesNormalizer**: Standardizes personal names
- **PlaceExtractor**: Extracts geographic entities using NER

## Documentation

- **Release Notes**: See `RELEASE_NOTES.md` for detailed milestone documentation
- **Process Documentation**: Complete pipeline documentation in processing notebooks
- **Data Mappings**: Column and value mappings available in `data/mappings/`
- **Quality Reports**: Data audit and validation reports in `reports/`

## Contributing

This project is part of ongoing research at UCSB AMPLab. For questions or collaboration opportunities, please refer to the project documentation and release notes.

## Related Publications

The methodological framework and GeoResolver library developed in this project are intended to be replicable for other historical datasets where entity recognition and record linkage present similar challenges.