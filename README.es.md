# La gente de Aucará (1760–1921)  
### Un conjunto de datos de individuos reconstruidos a partir de los registros parroquiales del valle de Sondondo, Perú

## Resumen

Este repositorio contiene un conjunto de datos estructurado derivado de los registros sacramentales conservados en el archivo parroquial de Aucará en el valle de Sondondo (Ayacucho, Perú). El conjunto de datos abarca el período 1760–1921 y contiene 10.251 registros de eventos, distribuidos en:

- **6.340 bautismos** (1790–1902)  
- **1.719 matrimonios** (1760–1921)  
- **2.192 entierros** (1846–1921)

Los registros originales fueron transcritos a partir de imágenes digitalizadas de los libros parroquiales, obtenidas directamente de los depósitos del archivo. Los documentos originales no están disponibles públicamente. Estos registros fueron posteriormente procesados mediante una serie de procedimientos de limpieza, normalización y armonización. Dichas transformaciones pueden reproducirse ejecutando los cuadernos Jupyter incluidos en el directorio `project_code/`, que documentan el flujo de trabajo de transformación de datos. El conjunto de datos resultante está estructurado para facilitar el enlace probabilístico de registros y el análisis prosopográfico de los individuos mencionados en los registros sacramentales.

Además de los registros sacramentales, el conjunto de datos incluye entidades derivadas a nivel de persona, lo que permite el análisis centrado en individuos y la futura reconstrucción de trayectorias vitales a través de múltiples registros.

---

# Estructura del repositorio

El repositorio está organizado para reflejar las diferentes etapas del flujo de trabajo de transformación de datos.

```
data/
├── raw/        # Transcripciones estructuradas originales de los registros parroquiales
├── interim/    # Conjuntos de datos intermedios generados durante la normalización
├── clean/      # Conjuntos de datos finales limpios utilizados para el análisis
├── mappings/   # Archivos de mapeo usados para la armonización y normalización
└── manual/     # Conjuntos de datos de referencia curados por expertos (gazetteers, archivos de autoridad)
```

### Datos brutos (`raw/`)

El directorio `raw/` contiene las transcripciones estructuradas iniciales de los registros parroquiales. Estos archivos fueron exportados desde las hojas de cálculo utilizadas durante la captura de datos y representan la forma no procesada de los datos tomados directamente de los registros parroquiales:

- `bautismos.csv`
- `matrimonios.csv`
- `entierros.csv`
- `raw_places.csv`

---

### Datos intermedios (`interim/`)

El directorio `interim/` contiene conjuntos de datos generados durante el proceso de normalización. Estos archivos documentan las transformaciones intermedias aplicadas durante la limpieza de datos, la extracción de términos y la estandarización de lugares.

Ejemplos incluyen:

- versiones normalizadas de las tablas sacramentales  
- referencias de personas extraídas  
- descriptores geográficos estandarizados  
- salidas de diagnóstico de los procedimientos de extracción  

---

### Datos limpios (`clean/`)

El conjunto de datos principal para su reutilización se encuentra en el directorio `data/clean/`:

- `bautismos_clean.csv`
- `matrimonios_clean.csv`
- `entierros_clean.csv`
- `personas.csv`
- `unique_places.csv`

Estas tablas representan la versión normalizada y lista para el análisis del conjunto de datos.

El archivo `personas.csv` contiene **entidades individuales extraídas de los registros sacramentales**, con información contextual sobre sus roles dentro de cada registro (p. ej., niño bautizado, padre/madre, testigo).

El archivo `unique_places.csv` contiene los lugares geográficos estandarizados mencionados en los registros, junto con sus coordenadas verificadas derivadas de un gazetteer curado por una colaboradora (`data/manual/toponimos.geojson`).

---

### Archivos de mapeo (`mappings/`)

El directorio `mappings/` contiene archivos de configuración utilizados durante el proceso de normalización. Estos mapeos estandarizan los nombres de columnas, las categorías de condición social y las referencias geográficas en los tres tipos de registros.

Ejemplos incluyen:

- `bautismosMapping.json`
- `matrimoniosMapping.json`
- `entierrosMapping.json`
- `conditionMapping.json`
- `places_types.json`

---

### Datos de referencia manuales (`manual/`)

El directorio `manual/` contiene conjuntos de datos de referencia curados por expertos que sirven como insumos autoritativos para el flujo de procesamiento. A diferencia de la carpeta `mappings/` (que contiene tablas de búsqueda guiadas por código), estos archivos representan conocimiento especializado compilado a través de investigación en fuentes primarias y trabajo de campo.

- `toponimos.geojson` — gazetteer autoritativo de topónimos documentados en los registros sacramentales, con coordenadas verificadas (WGS 84 / zona UTM 18S), nombres canónicos, variantes ortográficas conocidas, clasificaciones de tipo de lugar y jerarquías de jurisdicción eclesiástica

---

## Diccionario de metadatos

Este diccionario de metadatos proporciona documentación completa de todos los conjuntos de datos en la carpeta `data/clean/`. Cada sección incluye la estructura del conjunto de datos, una descripción del propósito de la tabla y documentación detallada a nivel de campo con los tipos de datos esperados y sus descripciones.

Los conjuntos de datos representan registros parroquiales históricos de Sondondo, Perú, que cubren eventos vitales (bautismos, matrimonios y entierros), así como entidades derivadas (lugares y personas). Todos los registros han sido limpiados, normalizados y armonizados para facilitar su análisis e integración.

**Valores ausentes:** Los campos sin información registrada se representan como celdas vacías en todas las tablas. No se utiliza ningún código de sustitución explícito (p. ej., `NA`, `null`).

**Precisión de fechas:** Varios campos de fecha tienen una columna compañera `*_precision` que indica la certeza del valor normalizado. Véase [`METADATA_DICTIONARY.md`](METADATA_DICTIONARY.md) para el vocabulario completo de valores de precisión.

### Bautismos (`bautismos_clean.csv`)

| Propiedad    | Tipo esperado | Descripción |
|--------------|---------------|-------------|
| file      | Texto          | Nombre del archivo fuente del que se extrajo el registro |
| identifier | Texto          | Identificador secuencial del evento de bautismo |
| event_type | Texto          | Tipo de evento (`Bautizo`) |
| event_date | Fecha          | Fecha del bautismo en formato ISO 8601 |
| event_date_precision | Texto | Nivel de certeza de `event_date` (`exact`, `month`, `month_inferred`, `year_inferred`, `day_adjusted`, `estimated`) |
| baptized_name | Texto       | Nombre(s) de pila normalizados del bautizado |
| baptized_lastname | Texto   | Apellido(s) normalizados o inferidos del bautizado |
| baptized_birth_place | Texto   | Lugar de nacimiento del bautizado |
| baptized_birth_date | Fecha    | Fecha de nacimiento del bautizado en formato ISO 8601 |
| baptized_birth_date_precision | Texto | Nivel de certeza de `baptized_birth_date` — incluye todos los valores de `event_date_precision` más `inferred_from_age` |
| baptized_legitimacy_status | Texto | Estado de filiación al nacer (`legitimo`, `ilegitimo`) |
| father_name | Texto         | Nombre normalizado del padre |
| father_lastname | Texto     | Apellido(s) normalizados o inferidos del padre |
| father_social_condition | Texto  | Marcador social, étnico o político del padre (`mestizo`, `indio`, `tributario`, `vecino`) |
| mother_name | Texto         | Nombre normalizado de la madre |
| mother_lastname | Texto     | Apellido(s) normalizados o inferidos de la madre |
| mother_social_condition | Texto  | Marcador social, étnico o político de la madre (`mestizo`, `indio`, `tributario`, `vecino`) |
| parents_social_condition | Texto | Condición social combinada de ambos padres |
| godfather_name | Texto     | Nombre normalizado del padrino |
| godfather_lastname | Texto | Apellido(s) normalizados o inferidos del padrino |
| godfather_social_condition | Texto | Marcador social, étnico o político del padrino (`mestizo`, `indio`, `tributario`, `vecino`) |
| godmother_name | Texto     | Nombre normalizado de la madrina |
| godmother_lastname | Texto | Apellido(s) normalizados o inferidos de la madrina |
| godmother_social_condition | Texto | Marcador social, étnico o político de la madrina (`mestizo`, `indio`, `tributario`, `vecino`) |
| event_place | Texto        | Lugar donde se celebró el bautismo |
| event_geographic_descriptor_1 | Texto | Lugar o localidad mencionado en el registro |
| event_geographic_descriptor_2 | Texto | Lugar o localidad adicional mencionado en el registro |
| event_geographic_descriptor_3 | Texto | Lugar o localidad adicional mencionado en el registro |
| event_geographic_descriptor_4 | Texto | Lugar o localidad adicional mencionado en el registro |

### Matrimonios (`matrimonios_clean.csv`)

La tabla de matrimonios contiene registros limpios y estandarizados de eventos matrimoniales extraídos de los libros parroquiales. Cada fila representa un evento matrimonial único con atributos asociados de ambos cónyuges, sus familias, testigos y padrinos.

| Propiedad    | Tipo esperado | Descripción |
|--------------|---------------|-------------|
| file      | Texto          | Nombre del archivo fuente del que se extrajo el registro |
| identifier | Texto          | Identificador secuencial del evento matrimonial |
| event_type | Texto          | Tipo de evento (`Matrimonio`) |
| event_date | Fecha          | Fecha del matrimonio en formato ISO 8601 |
| event_date_precision | Texto | Nivel de certeza de `event_date` (`exact`, `month`, `month_inferred`, `year_inferred`, `day_adjusted`, `estimated`) |
| husband_name | Texto       | Nombre(s) de pila normalizados del esposo |
| husband_lastname | Texto   | Apellido(s) normalizados o inferidos del esposo |
| husband_social_condition | Texto  | Marcador social, étnico o político del esposo (`mestizo`, `indio`, `tributario`, `vecino`, `don`) |
| husband_marital_status | Texto | Estado civil del esposo al momento del matrimonio (`soltero`, `viudo`) |
| husband_birth_date | Fecha    | Fecha de nacimiento del esposo en formato ISO 8601 |
| husband_birth_date_precision | Texto | Nivel de certeza de `husband_birth_date` — incluye todos los valores de `event_date_precision` más `inferred_from_age` |
| husband_birth_place | Texto   | Lugar de nacimiento del esposo |
| husband_resident_in | Texto   | Lugar de residencia registrado del esposo al momento del evento |
| husband_legitimacy_status | Texto | Estado de filiación del esposo al nacer (`legítimo`, `ilegitimo`, `natural`) |
| husband_father_name | Texto  | Nombre normalizado del padre del esposo |
| husband_father_lastname | Texto | Apellido(s) normalizados o inferidos del padre del esposo |
| husband_father_social_condition | Texto | Marcador social, étnico o político del padre del esposo (`mestizo`, `indio`, `tributario`, `vecino`, `don`) |
| husband_mother_name | Texto  | Nombre normalizado de la madre del esposo |
| husband_mother_lastname | Texto | Apellido(s) normalizados o inferidos de la madre del esposo |
| husband_mother_social_condition | Texto | Marcador social, étnico o político de la madre del esposo (`mestizo`, `indio`, `tributario`, `vecino`, `doña`) |
| wife_name | Texto         | Nombre(s) de pila normalizados de la esposa |
| wife_lastname | Texto     | Apellido(s) normalizados o inferidos de la esposa |
| wife_social_condition | Texto  | Marcador social, étnico o político de la esposa (`mestizo`, `indio`, `tributario`, `vecino`, `doña`) |
| wife_marital_status | Texto | Estado civil de la esposa al momento del matrimonio (`soltera`, `viuda`) |
| wife_birth_date | Fecha    | Fecha de nacimiento de la esposa en formato ISO 8601 |
| wife_birth_date_precision | Texto | Nivel de certeza de `wife_birth_date` — incluye todos los valores de `event_date_precision` más `inferred_from_age` |
| wife_birth_place | Texto   | Lugar de nacimiento de la esposa |
| wife_resident_in | Texto   | Lugar de residencia registrado de la esposa al momento del evento |
| wife_legitimacy_status | Texto | Estado de filiación de la esposa al nacer (`legítima`, `ilegitima`, `natural`) |
| wife_father_name | Texto    | Nombre normalizado del padre de la esposa |
| wife_father_lastname | Texto | Apellido(s) normalizados o inferidos del padre de la esposa |
| wife_father_social_condition | Texto | Marcador social, étnico o político del padre de la esposa (`mestizo`, `indio`, `tributario`, `vecino`, `don`) |
| wife_mother_name | Texto    | Nombre normalizado de la madre de la esposa |
| wife_mother_lastname | Texto | Apellido(s) normalizados o inferidos de la madre de la esposa |
| wife_mother_social_condition | Texto | Marcador social, étnico o político de la madre de la esposa (`mestizo`, `indio`, `tributario`, `vecino`, `doña`) |
| godparent_1_name | Texto   | Nombre normalizado del primer padrino/madrina |
| godparent_1_lastname | Texto | Apellido(s) normalizados o inferidos del primer padrino/madrina |
| godparent_1_social_condition | Texto | Marcador social, étnico o político del primer padrino/madrina (`mestizo`, `indio`, `tributario`, `vecino`, `don`, `doña`) |
| godparent_2_name | Texto   | Nombre normalizado del segundo padrino/madrina |
| godparent_2_lastname | Texto | Apellido(s) normalizados o inferidos del segundo padrino/madrina |
| godparent_2_social_condition | Texto | Marcador social, étnico o político del segundo padrino/madrina (`mestizo`, `indio`, `tributario`, `vecino`, `don`, `doña`) |
| godparent_3_name | Texto   | Nombre normalizado del tercer padrino/madrina (cuando corresponda) |
| godparent_3_lastname | Texto | Apellido(s) normalizados o inferidos del tercer padrino/madrina (cuando corresponda) |
| witness_1_name | Texto     | Nombre normalizado del primer testigo |
| witness_1_lastname | Texto | Apellido(s) normalizados o inferidos del primer testigo |
| witness_2_name | Texto     | Nombre normalizado del segundo testigo |
| witness_2_lastname | Texto | Apellido(s) normalizados o inferidos del segundo testigo |
| witness_3_name | Texto     | Nombre normalizado del tercer testigo (cuando corresponda) |
| witness_3_lastname | Texto | Apellido(s) normalizados o inferidos del tercer testigo (cuando corresponda) |
| witness_4_name | Texto     | Nombre normalizado del cuarto testigo (cuando corresponda) |
| witness_4_lastname | Texto | Apellido(s) normalizados o inferidos del cuarto testigo (cuando corresponda) |
| event_place | Texto        | Lugar donde se celebró el matrimonio |
| event_geographic_descriptor_1 | Texto | Lugar o localidad mencionado en el registro |
| event_geographic_descriptor_2 | Texto | Lugar o localidad adicional mencionado en el registro |
| event_geographic_descriptor_3 | Texto | Lugar o localidad adicional mencionado en el registro |
| event_geographic_descriptor_4 | Texto | Lugar o localidad adicional mencionado en el registro |
| event_geographic_descriptor_5 | Texto | Lugar o localidad adicional mencionado en el registro |
| event_geographic_descriptor_6 | Texto | Lugar o localidad adicional mencionado en el registro |

### Entierros (`entierros_clean.csv`)

La tabla de entierros contiene registros limpios y estandarizados de eventos de sepultura extraídos de los libros parroquiales. Cada fila representa un evento de entierro único con atributos como fecha, lugar e información sobre el fallecido y sus familiares sobrevivientes.

| Propiedad    | Tipo esperado | Descripción |
|--------------|---------------|-------------|
| file      | Texto          | Nombre del archivo fuente del que se extrajo el registro |
| identifier | Texto          | Identificador secuencial del evento de entierro |
| event_type | Texto          | Tipo de evento (`Entierro`) |
| event_date | Fecha          | Fecha del entierro en formato ISO 8601 |
| event_date_precision | Texto | Nivel de certeza de `event_date` (`exact`, `month`, `month_inferred`, `year_inferred`, `day_adjusted`, `estimated`) |
| doctrine   | Texto          | Nombre de la parroquia o doctrina donde se registró el entierro |
| event_place | Texto        | Lugar donde se realizó el entierro |
| deceased_name | Texto       | Nombre(s) de pila normalizados del fallecido |
| deceased_lastname | Texto   | Apellido(s) normalizados o inferidos del fallecido |
| deceased_birth_date | Fecha    | Fecha de nacimiento del fallecido en formato ISO 8601 |
| deceased_birth_date_precision | Texto | Nivel de certeza de `deceased_birth_date` — incluye todos los valores de `event_date_precision` más `inferred_from_age` |
| deceased_birth_place | Texto   | Lugar de nacimiento del fallecido |
| deceased_social_condition | Texto  | Marcador social, étnico o político del fallecido (`mestizo`, `indio`, `tributario`, `vecino`, `don`, `doña`) |
| deceased_marital_status | Texto | Estado civil del fallecido al momento de la muerte (`soltero/soltera`, `casado/casada`, `viudo/viuda`, `marido que fue`, `mujer que fue`) |
| deceased_legitimacy_status | Texto | Estado de filiación del fallecido al nacer (`legítimo`, `ilegitimo`, `natural`) |
| father_name | Texto         | Nombre normalizado del padre del fallecido |
| father_lastname | Texto     | Apellido(s) normalizados o inferidos del padre del fallecido |
| mother_name | Texto         | Nombre normalizado de la madre del fallecido |
| mother_lastname | Texto     | Apellido(s) normalizados o inferidos de la madre del fallecido |
| husband_name | Texto        | Nombre normalizado del esposo del fallecido (cuando estaba casado/a) |
| wife_name | Texto           | Nombre normalizado de la esposa del fallecido (cuando estaba casado/a) |
| burial_place | Texto        | Lugar específico donde fue sepultado el fallecido |
| event_geographic_descriptor_1 | Texto | Lugar o localidad mencionado en el registro |
| event_geographic_descriptor_2 | Texto | Lugar o localidad adicional mencionado en el registro |
| event_geographic_descriptor_3 | Texto | Lugar o localidad adicional mencionado en el registro |
| event_geographic_descriptor_4 | Texto | Lugar o localidad adicional mencionado en el registro |
| husband_lastname | Texto    | Apellido(s) normalizados o inferidos del esposo del fallecido |
| wife_lastname | Texto       | Apellido(s) normalizados o inferidos de la esposa del fallecido |

## Lugares (`unique_places.csv`)

La tabla de lugares es un gazetteer autoritativo de localizaciones geográficas documentadas en los registros sacramentales. Está basado en un conjunto de datos GIS curado por una colaboradora (`data/manual/toponimos.geojson`) que contiene topónimos identificados mediante investigación en fuentes primarias y trabajo de campo. Las menciones de lugares en los registros se vinculan a entradas del gazetteer mediante comparación de cadenas exacta y difusa. Las coordenadas son valores de campo verificados convertidos de WGS 84 / zona UTM 18S (EPSG:32718) a grados decimales.

| Propiedad    | Tipo esperado | Descripción |
|--------------|---------------|-------------|
| place_id | Numérico | Identificador único del lugar (corresponde a `Lugar_id` en los datos GIS fuente) |
| lugar_id | Numérico | Identificador original del conjunto de datos GIS de la colaboradora |
| place_name | Texto | Nombre canónico completo del lugar según los datos GIS (puede contener alternativas separadas por `\|`) |
| standardize_label | Texto | Nombre de visualización principal (primer segmento de `place_name`) |
| alt_names | Texto | Variantes ortográficas conocidas, separadas por `\|` |
| place_type | Texto | Clasificación del tipo de lugar (p. ej., `iglesia parroquial`, `caserio`, `parroquia`) |
| es_parte | Texto | `Lugar_id` de la jurisdicción superior, si aplica |
| language | Texto | Idioma del nombre del lugar (`es`) |
| latitude | Numérico | Latitud en grados decimales (WGS 84) |
| longitude | Numérico | Longitud en grados decimales (WGS 84) |
| source | Texto | Origen de los datos geográficos (`Grecia Roque (collaborator GIS data)`) |
| uri | Texto | URI externo, si está disponible |
| country_code | Texto | Código de país ISO (`PE`) |
| mentioned_as | Texto | Lista Python de todas las cadenas brutas de los registros vinculadas a este lugar |

## Personas (`personas.csv`)

Las personas representan menciones individuales de individuos extraídas de todos los registros de eventos y reestructuradas en un formato centrado en la persona. A diferencia de las tablas de eventos, que están organizadas por ceremonia, esta tabla se centra en los individuos y sus atributos tal como aparecen documentados en múltiples eventos. Cada fila representa una mención única de una persona extraída de un registro —previa a cualquier agrupación o agregación mediante enlace probabilístico de registros (PRL)— con información demográfica inferida que incluye nombre, fechas de nacimiento y muerte, y lugares. Múltiples menciones pueden referirse al mismo individuo histórico.

| Propiedad   | Tipo esperado | Descripción |
|------------|---------------|-------------|
| event_idno | Texto          | Identificador único de la mención del evento |
| original_identifier | Texto          | Identificador original del documento fuente |
| persona_idno | Texto        | Identificador único de la entidad persona |
| name       | Texto          | Nombre(s) de pila normalizados |
| lastname   | Texto          | Apellido(s) normalizados o inferidos |
| persona_type | Texto          | Tipo de persona (p. ej., `baptized`, `parent`, `godparent`) |
| birth_date | Fecha          | Fecha de nacimiento registrada o inferida en formato ISO 8601 |
| birth_date_precision | Texto | Nivel de certeza de `birth_date` — incluye todos los valores de `event_date_precision` más `inferred_from_age` |
| birth_place | Texto       | Lugar de nacimiento |
| death_date | Fecha          | Fecha de defunción registrada o inferida en formato ISO 8601 |
| death_date_precision | Texto | Nivel de certeza de `death_date` (`exact`, `month`, `month_inferred`, `year_inferred`, `day_adjusted`, `estimated`) |
| death_place | Texto       | Lugar de defunción |
| gender     | Texto          | Género inferido (`male`, `female`, `unknown`) |
| resident_in | Texto        | Lugar de residencia registrado al momento del evento |
| legitimacy_status | Texto    | Estado de filiación al nacer (`legitimo`, `ilegitimo`) |
| marital_status | Texto      | Estado civil al momento del evento (`soltero`, `casado`) |
| social_condition | Texto     | Marcador social, étnico o político (`mestizo`, `indio`, `tributario`, `vecino`) |
---

## Métodos

El conjunto de datos fue procesado en varias etapas de limpieza y normalización.

### 1. Limpieza de datos
Las transcripciones brutas fueron limpiadas para eliminar filas vacías, normalizar los nombres de columnas y corregir inconsistencias evidentes de transcripción.

### 2. Armonización de campos
Se utilizaron archivos de mapeo para estandarizar los nombres de columnas, los descriptores sociales y las diferencias estructurales entre los tres tipos de registros sacramentales.

### 3. Estandarización de lugares
Los descriptores geográficos brutos registrados en los libros parroquiales fueron vinculados a un gazetteer autoritativo curado por una colaboradora (`data/manual/toponimos.geojson`) mediante comparación de cadenas exacta y difusa. Las coordenadas — proporcionadas como valores de campo verificados en WGS 84 / zona UTM 18S — fueron convertidas a grados decimales.

### 4. Extracción de entidades
Los individuos mencionados en los registros fueron extraídos y asociados con roles específicos (p. ej., niño bautizado, padre/madre, testigo).

### 5. Generación del conjunto de datos
Los registros limpios y las entidades extraídas fueron combinados para producir tablas estructuradas adecuadas para el enlace probabilístico de registros y el análisis prosopográfico.

Todas las transformaciones están documentadas en los cuadernos Jupyter y los módulos Python incluidos en el directorio `project_code/`.

---

# Fuentes de datos

El conjunto de datos fue compilado a partir de los registros sacramentales conservados en el Archivo de la Parroquia de Aucará en el valle de Sondondo, Perú.

La captura de datos implicó la transcripción manual a partir de imágenes digitalizadas de los registros originales. Las transcripciones fueron registradas inicialmente usando plantillas estructuradas en hojas de cálculo compartidas. Los datos fueron revisados manualmente y normalizados computacionalmente para garantizar su consistencia.

Las imágenes digitalizadas de los registros originales se encuentran actualmente en un repositorio privado y no están disponibles públicamente.

---

# Código y software

El procesamiento de datos fue implementado en *Python (versión 3.8 o posterior)* utilizando las siguientes bibliotecas principales:

- pandas  
- numpy  
- pathlib  
- rapidfuzz  
- pyproj  

El repositorio incluye cuadernos Jupyter y módulos Python que documentan el flujo de trabajo utilizado para transformar las transcripciones brutas en el conjunto de datos limpio.

Estos scripts implementan procedimientos para:

- limpieza de datos  
- normalización de campos  
- estandarización geográfica  
- extracción de entidades  

---

# Citar como

Melo Flórez, J. A., Ramos, G., de la Puente Luna, J. C., Cobo Betancourt, J., Ancho, B., Xue, D., Ayinaparthi, S., Roque Ortega, G., Gonzales Rojas, E., Quillca, J., Velarde Loayza, J., Asto Campos, C., & UCSB - Archives, Memory & Preservation Lab. (2026). The People of Aucará (1760–1921): A Dataset of Individuals Reconstructed from Parish Records of the Sondondo Valley, Peru (v1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18969892

---

# Licencia

Este repositorio utiliza una doble licencia:

- **Datos** (directorio `data/`): [Creative Commons Atribución–NoComercial–CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) — véase `LICENSE-DATA`.
- **Código** (directorio `project_code/`): [Licencia MIT](https://opensource.org/licenses/MIT) — véase `LICENSE`.
