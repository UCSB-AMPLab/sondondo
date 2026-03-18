# Metadata Dictionary

This metadata dictionary provides comprehensive documentation for all datasets in the `data/clean/` folder. Each section includes a description of the table's purpose and detailed field-level documentation with expected data types and descriptions.

The datasets represent historical parish records from Sondondo, Peru, covering vital events (baptisms, marriages, and burials) as well as derived entities (places and personas). All records have been cleaned, normalized, and harmonized to facilitate analysis and integration.

---

## Date Precision Values

Several date fields have a companion `*_precision` column. The following values are used across all precision fields:

| Value | Meaning |
|---|---|
| `exact` | Date taken directly from the source record or corrected only for format (e.g. inverted order, Excel serial number) |
| `month` | Day was absent in the source; filled with `01` |
| `month_inferred` | Month was absent; inferred from the nearest preceding record |
| `year_inferred` | Year was absent; inferred from the nearest preceding record |
| `day_adjusted` | Date contained a nonexistent day (e.g. 31 November); corrected to the nearest valid day |
| `estimated` | Record was physically torn (`roto`); day estimated as the average of the indicated range |
| `inferred_from_age` | Birth date back-calculated by subtracting a recorded age expression from the event date *(birth date fields only)* |

---

## Events

Event tables document vital religious ceremonies recorded in parish registers: baptisms, marriages, and burials. These records form the primary source material for the project, capturing not only the principal individuals involved but also family relationships, social conditions, and geographic information.

### Baptisms — `data/clean/bautismos_clean.csv`

Each row represents a unique baptism event.

| Property | Expected Type | Description |
|---|---|---|
| file | Text | Source file name from which the record was extracted |
| identifier | Text | Sequential identifier for the baptism event |
| event_type | Text | Type of event (`Bautizo`) |
| event_date | Date | Date of the baptism event in ISO 8601 format |
| event_date_precision | Text | Certainty level of `event_date` — see [Date Precision Values](#date-precision-values) |
| baptized_name | Text | Normalized first and middle name(s) of the baptized individual |
| baptized_lastname | Text | Normalized or inferred surname(s) of the baptized individual |
| baptized_birth_place | Text | Place of birth of the baptized individual |
| baptized_birth_date | Date | Date of birth of the baptized individual in ISO 8601 format |
| baptized_birth_date_precision | Text | Certainty level of `baptized_birth_date` — see [Date Precision Values](#date-precision-values) |
| baptized_legitimacy_status | Text | Legitimacy status at birth (`legitimo`, `ilegitimo`) |
| father_name | Text | Normalized name of the father |
| father_lastname | Text | Normalized or inferred surname(s) of the father |
| father_social_condition | Text | Social, ethnical, or political marker of the father (`mestizo`, `indio`, `tributario`, `vecino`) |
| mother_name | Text | Normalized name of the mother |
| mother_lastname | Text | Normalized or inferred surname(s) of the mother |
| mother_social_condition | Text | Social, ethnical, or political marker of the mother (`mestizo`, `indio`, `tributario`, `vecino`) |
| parents_social_condition | Text | Combined social condition of both parents |
| godfather_name | Text | Normalized name of the godfather |
| godfather_lastname | Text | Normalized or inferred surname(s) of the godfather |
| godfather_social_condition | Text | Social, ethnical, or political marker of the godfather (`mestizo`, `indio`, `tributario`, `vecino`) |
| godmother_name | Text | Normalized name of the godmother |
| godmother_lastname | Text | Normalized or inferred surname(s) of the godmother |
| godmother_social_condition | Text | Social, ethnical, or political marker of the godmother (`mestizo`, `indio`, `tributario`, `vecino`) |
| event_place | Text | Place where the baptism event took place |
| event_geographic_descriptor_1 | Text | Place or location mentioned in the record |
| event_geographic_descriptor_2 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_3 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_4 | Text | Additional place or location mentioned in the record |

---

### Marriages — `data/clean/matrimonios_clean.csv`

Each row represents a unique marriage event with associated attributes for both spouses, their families, witnesses, and godparents.

| Property | Expected Type | Description |
|---|---|---|
| file | Text | Source file name from which the record was extracted |
| identifier | Text | Sequential identifier for the marriage event |
| event_type | Text | Type of event (`Matrimonio`) |
| event_date | Date | Date of the marriage event in ISO 8601 format |
| event_date_precision | Text | Certainty level of `event_date` — see [Date Precision Values](#date-precision-values) |
| husband_name | Text | Normalized first and middle name(s) of the husband |
| husband_lastname | Text | Normalized or inferred surname(s) of the husband |
| husband_social_condition | Text | Social, ethnical, or political marker of the husband (`mestizo`, `indio`, `tributario`, `vecino`, `don`) |
| husband_marital_status | Text | Marital status of the husband at the time of marriage (`soltero`, `viudo`) |
| husband_birth_date | Date | Date of birth of the husband in ISO 8601 format |
| husband_birth_date_precision | Text | Certainty level of `husband_birth_date` — see [Date Precision Values](#date-precision-values) |
| husband_birth_place | Text | Place of birth of the husband |
| husband_resident_in | Text | Recorded place of residence of the husband at the time of the event |
| husband_legitimacy_status | Text | Legitimacy status of the husband at birth (`legítimo`, `ilegitimo`, `natural`) |
| husband_father_name | Text | Normalized name of the husband's father |
| husband_father_lastname | Text | Normalized or inferred surname(s) of the husband's father |
| husband_father_social_condition | Text | Social, ethnical, or political marker of the husband's father (`mestizo`, `indio`, `tributario`, `vecino`, `don`) |
| husband_mother_name | Text | Normalized name of the husband's mother |
| husband_mother_lastname | Text | Normalized or inferred surname(s) of the husband's mother |
| husband_mother_social_condition | Text | Social, ethnical, or political marker of the husband's mother (`mestizo`, `indio`, `tributario`, `vecino`, `doña`) |
| wife_name | Text | Normalized first and middle name(s) of the wife |
| wife_lastname | Text | Normalized or inferred surname(s) of the wife |
| wife_social_condition | Text | Social, ethnical, or political marker of the wife (`mestizo`, `indio`, `tributario`, `vecino`, `doña`) |
| wife_marital_status | Text | Marital status of the wife at the time of marriage (`soltera`, `viuda`) |
| wife_birth_date | Date | Date of birth of the wife in ISO 8601 format |
| wife_birth_date_precision | Text | Certainty level of `wife_birth_date` — see [Date Precision Values](#date-precision-values) |
| wife_birth_place | Text | Place of birth of the wife |
| wife_resident_in | Text | Recorded place of residence of the wife at the time of the event |
| wife_legitimacy_status | Text | Legitimacy status of the wife at birth (`legítima`, `ilegitima`, `natural`) |
| wife_father_name | Text | Normalized name of the wife's father |
| wife_father_lastname | Text | Normalized or inferred surname(s) of the wife's father |
| wife_father_social_condition | Text | Social, ethnical, or political marker of the wife's father (`mestizo`, `indio`, `tributario`, `vecino`, `don`) |
| wife_mother_name | Text | Normalized name of the wife's mother |
| wife_mother_lastname | Text | Normalized or inferred surname(s) of the wife's mother |
| wife_mother_social_condition | Text | Social, ethnical, or political marker of the wife's mother (`mestizo`, `indio`, `tributario`, `vecino`, `doña`) |
| godparent_1_name | Text | Normalized name of the first godparent |
| godparent_1_lastname | Text | Normalized or inferred surname(s) of the first godparent |
| godparent_1_social_condition | Text | Social, ethnical, or political marker of the first godparent (`mestizo`, `indio`, `tributario`, `vecino`, `don`, `doña`) |
| godparent_2_name | Text | Normalized name of the second godparent |
| godparent_2_lastname | Text | Normalized or inferred surname(s) of the second godparent |
| godparent_2_social_condition | Text | Social, ethnical, or political marker of the second godparent (`mestizo`, `indio`, `tributario`, `vecino`, `don`, `doña`) |
| godparent_3_name | Text | Normalized name of the third godparent (when applicable) |
| godparent_3_lastname | Text | Normalized or inferred surname(s) of the third godparent (when applicable) |
| witness_1_name | Text | Normalized name of the first witness |
| witness_1_lastname | Text | Normalized or inferred surname(s) of the first witness |
| witness_2_name | Text | Normalized name of the second witness |
| witness_2_lastname | Text | Normalized or inferred surname(s) of the second witness |
| witness_3_name | Text | Normalized name of the third witness (when applicable) |
| witness_3_lastname | Text | Normalized or inferred surname(s) of the third witness (when applicable) |
| witness_4_name | Text | Normalized name of the fourth witness (when applicable) |
| witness_4_lastname | Text | Normalized or inferred surname(s) of the fourth witness (when applicable) |
| event_place | Text | Place where the marriage event took place |
| event_geographic_descriptor_1 | Text | Place or location mentioned in the record |
| event_geographic_descriptor_2 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_3 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_4 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_5 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_6 | Text | Additional place or location mentioned in the record |

---

### Burials — `data/clean/entierros_clean.csv`

Each row represents a unique burial event with associated attributes for the deceased individual and their surviving family members.

| Property | Expected Type | Description |
|---|---|---|
| file | Text | Source file name from which the record was extracted |
| identifier | Text | Sequential identifier for the burial event |
| event_type | Text | Type of event (`Entierro`) |
| event_date | Date | Date of the burial event in ISO 8601 format |
| event_date_precision | Text | Certainty level of `event_date` — see [Date Precision Values](#date-precision-values) |
| doctrine | Text | Name of the parish or doctrine where the burial was registered |
| event_place | Text | Place where the burial event took place |
| deceased_name | Text | Normalized first and middle name(s) of the deceased individual |
| deceased_lastname | Text | Normalized or inferred surname(s) of the deceased individual |
| deceased_birth_date | Date | Date of birth of the deceased individual in ISO 8601 format |
| deceased_birth_date_precision | Text | Certainty level of `deceased_birth_date` — see [Date Precision Values](#date-precision-values) |
| deceased_birth_place | Text | Place of birth of the deceased individual |
| deceased_social_condition | Text | Social, ethnical, or political marker of the deceased (`mestizo`, `indio`, `tributario`, `vecino`, `don`, `doña`) |
| deceased_marital_status | Text | Marital status of the deceased at the time of death (`soltero/soltera`, `casado/casada`, `viudo/viuda`, `marido que fue`, `mujer que fue`) |
| deceased_legitimacy_status | Text | Legitimacy status of the deceased at birth (`legítimo`, `ilegitimo`, `natural`) |
| father_name | Text | Normalized name of the deceased's father |
| father_lastname | Text | Normalized or inferred surname(s) of the deceased's father |
| mother_name | Text | Normalized name of the deceased's mother |
| mother_lastname | Text | Normalized or inferred surname(s) of the deceased's mother |
| husband_name | Text | Normalized name of the deceased's husband (when deceased was married) |
| husband_lastname | Text | Normalized or inferred surname(s) of the deceased's husband |
| wife_name | Text | Normalized name of the deceased's wife (when deceased was married) |
| wife_lastname | Text | Normalized or inferred surname(s) of the deceased's wife |
| burial_place | Text | Specific location where the deceased was buried |
| event_geographic_descriptor_1 | Text | Place or location mentioned in the record |
| event_geographic_descriptor_2 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_3 | Text | Additional place or location mentioned in the record |
| event_geographic_descriptor_4 | Text | Additional place or location mentioned in the record |

---

## Places — `data/clean/places.csv`

The places table represents a controlled vocabulary of geographic locations extracted from all event records and normalized through a combination of manual curation and automated gazetteer matching. Each place has been geocoded and linked to external authorities (GeoNames, Getty Thesaurus of Geographic Names) when possible.

| Property | Expected Type | Description |
|---|---|---|
| place_id | Numeric | Unique identifier for the place |
| manually_normalized_name | Text | Standardized name assigned during data cleaning |
| standardized_name | Text | Name standardized using external gazetteers |
| language | Text | Language of the place name (e.g., `es`, `en`) |
| latitude | Numeric | Latitude coordinate of the place |
| longitude | Numeric | Longitude coordinate of the place |
| source_gazetteer | Text | Source gazetteer used for standardization (e.g., `geonames`, `tgn`) |
| id | Text | Identifier of the place in the source gazetteer |
| uri | Text | URI linking to the place in the source gazetteer |
| country_code | Text | ISO country code of the place |
| part_of | Text | Higher-level administrative division the place belongs to |
| part_of_uri | Text | URI of the higher-level administrative division |
| confidence | Numeric | Confidence score of the place standardization (0–100) |
| treshold | Numeric | Threshold used for the place standardization |
| match_type | Text | Type of match made during standardization (e.g., `exact`, `fuzzy`) |
| mentioned_as | Text | Original text mention of the place in the records |

---

## Personas — `data/clean/personas.csv`

Personas represent individual person mentions extracted from all event records and restructured into a person-centric format. Unlike the event tables which are organized around ceremonies, this table focuses on individuals and their attributes as documented across multiple events. Each row is a unique person mention with inferred demographic information; multiple rows may refer to the same historical individual before probabilistic record linkage.

| Property | Expected Type | Description |
|---|---|---|
| event_idno | Text | Unique identifier for the source event |
| original_identifier | Text | Original identifier from the source document |
| persona_type | Text | Role of the person in the event (`baptized`, `father`, `mother`, `godfather`, `godmother`, `godparent`, `husband`, `wife`, `witness`, `deceased`) |
| name | Text | Normalized first and middle name(s) |
| lastname | Text | Normalized or inferred surname(s) |
| gender | Text | Inferred gender (`male`, `female`, `unknown`) |
| birth_date | Date | Recorded or inferred date of birth in ISO 8601 format |
| birth_date_precision | Text | Certainty level of `birth_date` — see [Date Precision Values](#date-precision-values) |
| birth_place | Text | Place of birth |
| death_date | Date | Recorded or inferred date of death in ISO 8601 format |
| death_date_precision | Text | Certainty level of `death_date` — see [Date Precision Values](#date-precision-values) |
| death_place | Text | Place of death |
| resident_in | Text | Recorded place of residence at the time of the event |
| legitimacy_status | Text | Legitimacy status at birth (`legitimo`, `ilegitimo`) |
| marital_status | Text | Marital status at the time of the event (`soltero`, `casado`) |
| social_condition | Text | Social, ethnical, or political marker (`mestizo`, `indio`, `tributario`, `vecino`) |
