from actions.helpers.handlers.ColumnManager import ColumnManager
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from actions.helpers.handlers.LogerHandler import setup_logger
logger = setup_logger("textAnalysis")

import unicodedata
import re

STOPWORDS = stopwords.words("spanish")
STOPWORDS.extend(["sic", "ilegible", "roto", "conocido", "legible", "nan"])

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    
    text = unicodedata.normalize("NFD", text)
    text = ''.join(c for c in text if unicodedata.category(c) != "Mn") # Remove accents

    text = text.lower()

    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip() 

    return text

def clean_series(serie):
    """
    Function to clean a pandas Series.
    """
    cleaned = serie.fillna("").apply(normalize_text)
    cleaned = cleaned.replace("", pd.NA)
    return cleaned

def got_top_keywords(data, clusters, labels, pattern, n_terms=10):
    """
    Function to get top keywords for each cluster.
    """

    df = pd.DataFrame(data.todense()).groupby(clusters).mean()

    logger.info(f"{pattern}\nTop {n_terms} keywords for each cluster:")
    for i,r in df.iterrows():
        logger.info('Cluster {}'.format(i))
        logger.info(','.join([labels[t] for t in np.argsort(r)[-n_terms:]]))
    return df

def determine_optimal_clusters(text_matrix, max_clusters=10):
    """
    Determine optimal number of clusters using elbow method and silhouette analysis.
    """
    from sklearn.metrics import silhouette_score
    
    if text_matrix.shape[0] < 2:
        return 1
    if text_matrix.shape[0] < max_clusters:
        max_clusters = text_matrix.shape[0]
    
    inertias = []
    silhouette_scores = []
    K_range = range(2, min(max_clusters + 1, text_matrix.shape[0]))
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(text_matrix)
        inertias.append(kmeans.inertia_)
        
        # Calculate silhouette score (that is, how well each point is clustered)
        # Note: silhouette_score requires at least 2 clusters
        # and at least 2 samples in each cluster
        if len(set(cluster_labels)) > 1: 
            sil_score = silhouette_score(text_matrix, cluster_labels)
            silhouette_scores.append(sil_score)
        else:
            silhouette_scores.append(0)
    
    # Find elbow point (simplified method)
    if len(inertias) >= 2:
        # Calculate the rate of change
        changes = [inertias[i-1] - inertias[i] for i in range(1, len(inertias))]
        elbow_idx = changes.index(max(changes)) + 2  # +2 because we start from k=2
    else:
        elbow_idx = 2

    # Find best silhouette score. This is helpful to
    # determine the best number of clusters
    if silhouette_scores:
        best_sil_idx = silhouette_scores.index(max(silhouette_scores)) + 2
        print(f"Elbow method suggests: {elbow_idx} clusters")
        print(f"Silhouette analysis suggests: {best_sil_idx} clusters")
        print(f"Silhouette scores: {dict(zip(K_range, silhouette_scores))}")
        
        return best_sil_idx
    else:
        return elbow_idx

## Agglomerative clustering using TF-IDF + KMeans

def got_keywords_from_columns(column_pattern, stop_words=STOPWORDS, n_clusters='auto', max_clusters=10):
    """
    Extract keywords from columns matching a pattern and perform clustering.
    
    Args:
        column_pattern: Regex pattern to match column names
        stop_words: List of words to exclude from analysis
        n_clusters: Number of clusters ('auto' for automatic determination, or integer)
        max_clusters: Maximum number of clusters to consider when auto-determining
    """

    dataframes = {
        "bautismos": {"csv_file": "data/raw/bautismos.csv",
                  "mapping_file": "data/mappings/bautismosMapping.json"},
        "entierros": {"csv_file": "data/raw/entierros.csv",
                  "mapping_file": "data/mappings/entierrosMapping.json"},
        "matrimonios": {"csv_file": "data/raw/matrimonios.csv",
                  "mapping_file": "data/mappings/matrimoniosMapping.json"}
    }

    all_data = [] 

    for dataset, info in dataframes.items():
        print(f"\nProcessing {dataset}...")
        csv_path = info["csv_file"]
        mapping_path = info["mapping_file"]

        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows from {csv_path}")

        column_manager = ColumnManager()
        df = column_manager.harmonize_columns(df, mapping_path)

        if isinstance(column_pattern, str):
            pattern = re.compile(column_pattern)
        else:
            pattern = column_pattern
            
        columns_pattern = [col for col in df.columns if pattern.search(col)]
        print(f"Columns matching pattern '{pattern}': {columns_pattern}")

        if not columns_pattern:
            print(f"No matching columns found in {dataset}")
            continue
        
        if len(columns_pattern) > 1:
            combined_col = columns_pattern[0] + "_combined"
            df[combined_col] = df[columns_pattern].astype(str).agg(' '.join, axis=1)
            columns_pattern = [combined_col]  # Use the new combined column
        else:
            columns_pattern = [columns_pattern[0]]

        for col in columns_pattern:
            test_data = df[col].copy()
            print(f"\nProcessing column {col}")
            print(f"Initial data points: {len(test_data)}")
            
            test_data = clean_series(test_data)
            print(f"Data points after cleaning: {len(test_data.dropna())}")
            
            valid_data = test_data.dropna().unique().tolist()
            print(f"Unique valid values found: {len(valid_data)}")
            all_data.extend(valid_data)

    data = pd.Series(all_data)
    print(f"\nTotal unique data points across all datasets: {len(data)}")
    
    if len(data) == 0:
        print("No valid data points found!")
        return None

    # Create and fit the TF-IDF vectorizer
    tfidf = TfidfVectorizer(
        max_features=100,
        min_df=2,
        max_df=0.95,
        stop_words=stop_words,
        ngram_range=(1, 2) # Unigrams and bigrams
    )
    
    try:
        tfidf.fit(data)
        text = tfidf.transform(data)
        print(f"Created TF-IDF matrix with shape: {text.shape}")
        
        # Determine optimal number of clusters
        if n_clusters == 'auto':
            optimal_clusters = determine_optimal_clusters(text, max_clusters)
            print(f"Auto-determined optimal clusters: {optimal_clusters}")
        else:
            optimal_clusters = n_clusters
            print(f"Using specified number of clusters: {optimal_clusters}")

        if optimal_clusters == 1:
            clusters = np.zeros(text.shape[0])
            print("Only one cluster needed for this data")
        else:
            kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10) # type: ignore
            clusters = kmeans.fit_predict(text)
            
        unique_labels, counts = np.unique(clusters, return_counts=True)
        print(f"Assigned cluster labels: {dict(zip(unique_labels, counts))}")

        return got_top_keywords(text, clusters, tfidf.get_feature_names_out(), str(column_pattern), n_terms=15)

    except ValueError as e:
        print(f"Error during TF-IDF/clustering: {str(e)}")
        return None



result = got_keywords_from_columns(
    column_pattern=re.compile(r".*marital.*")
)
