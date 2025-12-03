# Release Notes

## v0.2.0: Personas Dataset Creation

**Release Date:** November 12, 2025  
**Milestone:** Unified Individual Records Extraction Complete

### 🎯 Overview

This release marks the successful completion of the personas dataset creation phase. We have systematically extracted and consolidated all individuals mentioned across the three cleaned historical datasets (baptisms, marriages, and burials) into a unified `personas.csv` dataset, ready for probabilistic record linkage and entity resolution.

### 📊 Personas Dataset Summary

**Output:** `data/clean/personas.csv`
- Consolidated individual records from all three event types
- Role-based extraction preserving context (baptized, parent, godparent, spouse, deceased, etc.)
- Unified schema harmonizing fields across different record types
- Source record metadata maintained for traceability
- Standardized name and place fields ready for matching algorithms

### ✨ Key Achievements

#### 1. Individual Extraction
- ✅ Systematically extracted all persons from baptism records (children, parents, godparents)
- ✅ Extracted all persons from marriage records (spouses, witnesses, parents)
- ✅ Extracted all persons from burial records (deceased, parents, spouses)
- ✅ Preserved individual roles and relationships in the extraction process

#### 2. Schema Unification
- ✅ Created unified field structure across all record types
- ✅ Standardized column naming conventions for personas dataset
- ✅ Harmonized geographic and temporal fields
- ✅ Maintained data type consistency across extracted records

#### 3. Metadata Preservation
- ✅ Source record type tracking (baptism/marriage/burial)
- ✅ Source record ID references for traceability
- ✅ Event date preservation from original records
- ✅ Role context maintained for each individual

#### 4. Data Quality
- ✅ Validated extracted records against source data
- ✅ Applied existing normalization standards (names, places, dates)
- ✅ Documented extraction statistics and coverage metrics
- ✅ Quality assurance checks for data integrity

### 🔧 Technical Implementation

#### Core Components Developed
- **PersonasExtractor**: Orchestrates extraction from all record types
- **RoleMapper**: Maps individuals to their contextual roles
- **SchemaUnifier**: Harmonizes fields across different sources
- **MetadataPreserver**: Maintains source record references

#### Extraction Pipeline
```
Cleaned Data → Individual Identification → Role Assignment → 
Schema Unification → Metadata Attachment → Quality Validation → 
Personas Dataset Export
```

### 📁 File Structure
```
data/
├── raw/           # Original datasets
├── clean/         # Processed datasets
│   ├── bautismos_clean.csv     ✅
│   ├── matrimonios_clean.csv   ✅
│   ├── entierros_clean.csv     ✅
│   └── personas.csv            ✅ NEW
├── interim/       # Intermediate processing files
└── mappings/      # Configuration files

project_code/
├── dataCleaning.ipynb         ✅
├── personasCreation.ipynb     ✅ NEW
├── utils/                     # Core utility classes
└── actions/                   # Processing modules
```

### 📈 Dataset Statistics

**Source Records Processed:**
- Baptisms: 6,340 records
- Marriages: 1,719 records
- Burials: 2,121 records
- **Total: 10,180 cleaned historical records**

**Personas Extracted:**
- Comprehensive extraction from all event types
- Multiple roles per individual preserved
- Ready for entity resolution and matching

### 🎯 Next Phase: Probabilistic Record Linkage

With the personas dataset complete, the project advances to:

1. **Blocking Strategy**: Define blocking keys for efficient matching
2. **Similarity Scoring**: Implement probabilistic matching algorithms
3. **Entity Resolution**: Link duplicate individuals across records
4. **Unique ID Assignment**: Create consolidated individual identifiers
5. **Relationship Network**: Build familial and social connection graphs

### 🛠️ Dependencies
- pandas (data manipulation)
- numpy (numerical operations)
- pathlib (file handling)
- Custom utilities from v0.1.0 (maintained)

### 📝 Files Added/Modified
- **NEW:** `project_code/personasCreation.ipynb` - Personas extraction pipeline
- **NEW:** `data/clean/personas.csv` - Consolidated individual records
- **UPDATED:** `README.md` - Project status and phase documentation
- **UPDATED:** `RELEASE_NOTES.md` - This release documentation

### 🔄 Design Decision: Database-Free Approach

This release adopts a streamlined approach, leveraging CSV-based processing instead of a relational database. This decision:
- ✅ Simplifies the workflow for probabilistic record linkage
- ✅ Reduces infrastructure complexity
- ✅ Maintains data portability and accessibility
- ✅ Enables efficient pandas-based processing pipelines

The personas dataset structure provides sufficient organization for subsequent matching and analysis phases without requiring database overhead.

---

## v0.1.0: Data Cleaning Milestone

**Release Date:** July 29, 2025  
**Pre-milestone Release:** Data Cleaning and Standardization Complete

### 🎯 Overview

This release marks the completion of the comprehensive data cleaning and standardization phase for the Sondondo Valley Parish Records project. We have successfully processed and cleaned three historical datasets (baptisms, marriages, and burials) spanning 1760-1921, preparing them for the next phase of individual record creation and transformation.

### 📊 Dataset Summary

#### Cleaned Datasets
- **Baptisms (`bautismos_clean.csv`)**: 6,341 records
- **Marriages (`matrimonios_clean.csv`)**: 1,719 records  
- **Burials (`entierros_clean.csv`)**: 2,198 records
- **Total**: 10,258 cleaned historical records

### ✨ Key Achievements

#### 1. Column Harmonization
- ✅ Standardized column names across all three datasets using mapping files
- ✅ Applied consistent naming conventions for cross-dataset compatibility
- ✅ Reduced datasets to essential columns using `usefulColumnsMapping.json`
- ✅ Removed empty columns to optimize data structure

#### 2. Data Quality Improvements
- ✅ **Null Value Standardization**: Replaced inconsistent empty values (`''`, `'-'`, `'--'`, `'n/a'`, `'na'`, `'null'`, `'None'`) with proper `np.nan`
- ✅ **Date Normalization**: Standardized all dates to `YYYY-MM-DD` format using `DateNormalizer`
- ✅ **Age Inference**: Processed age-related fields and birthdates using `AgeInferrer`
- ✅ **Names Standardization**: Normalized all name fields using `NamesNormalizer`

#### 3. Advanced Data Processing
- ✅ **Place Recognition**: Implemented NER (Named Entity Recognition) for geographic location extraction from text fields
- ✅ **Geographic Standardization**: Processed place names in all location-related columns
- ✅ **Relationship Data**: Preserved and cleaned family relationship information (parents, godparents, witnesses)

#### 4. Quality Assurance
- ✅ **Data Validation**: Identified and documented inconsistent date records (birthdates after event dates)
- ✅ **Cleaning Audit**: Comprehensive audit system tracking missing values and data quality metrics
- ✅ **Documentation**: Complete process documentation in Jupyter notebook format

### 🔧 Technical Implementation

#### Core Components Developed
- **ColumnManager**: Handles column harmonization and mapping
- **DateNormalizer**: Standardizes date formats across datasets
- **AgeInferrer**: Processes and infers age-related information
- **NamesNormalizer**: Standardizes personal names
- **PlaceExtractor**: Extracts and normalizes geographic entities

#### Data Processing Pipeline
```
Raw Data → Column Harmonization → Null Value Cleanup → 
Date Normalization → Age Processing → Name Standardization → 
Place Recognition → Quality Audit → Clean Data Export
```

### 📁 File Structure
```
data/
├── raw/           # Original datasets
├── clean/         # Processed, standardized datasets ✅
├── interim/       # Intermediate processing files
└── mappings/      # Column and value mapping configurations

project_code/
├── dataCleaning.ipynb    # Complete data cleaning pipeline ✅
├── utils/               # Core utility classes
└── actions/            # Processing modules
    ├── normalizers/    # Data normalization tools
    ├── generators/     # Data generation utilities
    └── extractors/     # Entity extraction tools
```

### 🚨 Known Issues
- **Date Inconsistencies**: Some records contain birthdates after event dates, requiring manual verification against original sources
- **Missing Data**: Certain fields have high missing value percentages, documented in audit reports

### 📈 Data Quality Metrics
- **Missing Values**: Comprehensive tracking and reporting implemented
- **Standardization**: 100% of name and place fields processed through normalization
- **Date Validation**: All date fields converted to standard format with error flagging
- **Audit Trail**: Complete documentation of all cleaning operations

### 🛠️ Dependencies
- pandas (data manipulation)
- numpy (numerical operations)  
- pathlib (file handling)
- Custom utilities (ColumnManager, DateNormalizer, etc.)

### 📝 Files Modified/Added
- `project_code/dataCleaning.ipynb` - Complete data cleaning pipeline
- `data/clean/*.csv` - Cleaned datasets ready for next phase
- `project_code/utils/` - Core utility modules
- `project_code/actions/` - Data processing modules

### 🔄 Migration Notes
- All future processing should use files from `data/clean/` directory
- Original raw data preserved in `data/raw/` for reference
- Mapping configurations available in `data/mappings/` for reference

---