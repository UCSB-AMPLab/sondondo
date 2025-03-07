# Identifying Unique Individuals through Probabilistic Record Linkage: A Case Study of Sondondo Valley Parish Records

Historical parish records provide insights into demographic, social, and familial patterns but often lack explicit unique identifiers, complicating efforts to track individuals across events. This project employs probabilistic record linkage methods to systematically identify unique individuals within a rich corpus of parish records from the Sondondo Valley, Peru, encompassing baptisms, marriages, and burials from 1760 to 1921. Leveraging contextual data—such as names, familial relationships, geographic locations, and event dates—this approach aims to reduce ambiguity, enabling historical and demographic analyses. Furthermore, network analysis techniques will refine matches, attempting to uncover familial and social connections within the historical community. This methodological framework could be replicated in other historical datasets where recognizing entities is challenging, enhancing digital collections through more robust and consistent record linkage.

## Data collection

Data was gathered from parish records of baptisms, marriages, and burials from the Sondondo Valley, Peru, covering the period from 1760 to 1921. Data capture involved manual transcription directly from digitized images of the original documents. All data was ingested into a shared Google Sheet pre-populated with a structured template for each record type. Post-collection, the data underwent manual review to identify and correct obvious inconsistencies and errors.

## Raw data

The raw data files are stored in the `data/raw` folder, containing:

- `bautismos.csv`: Baptism records.
- `matrimonios.csv`: Marriage records.
- `entierros.csv`: Burial records.

These CSV files were exported directly from the original Google Sheets used for transcription.

## Proposed workflow

```mathematica
Initial Exploration & DB Setup
              │
              ▼
Database Cleaning & Standardization
              │
              ▼
Relational Key Creation
              │
              ▼
Probabilistic Record Linkage
              │
              ▼
Network Analysis & Validation
              │
              ▼
Manual Review & Quality Assurance
              │
              ▼
Final Data Export & Analysis
```
