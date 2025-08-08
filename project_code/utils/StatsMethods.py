import numpy as np
from typing import List, Union, Optional


def cv(frequencies: List[Union[int, float]], rounding: Optional[int] = None) -> Union[float, None]:
    """
    Coefficient of Variation (CV) calculation.
    
    Args:
        frequencies: List of term frequencies
        
    Returns:
        Coefficient of Variation as a float
    """
    if not frequencies:
        raise ValueError("Frequencies list cannot be empty")

    mean_frequency = sum(frequencies) / len(frequencies) if frequencies else 0
    std_frequency = np.std(frequencies, ddof=1) 
    cv = std_frequency / mean_frequency if mean_frequency > 0 else 0
    return round(float(cv), rounding) if rounding is not None else float(cv)


def shannon_entropy(frequencies: List[Union[int, float]], rounding: Optional[int] = None) -> dict:
    """
    Calculate Shannon Entropy for a list of frequencies.
    
    Args:
        frequencies: List of term frequencies

    Returns:
        Shannon Entropy as a float
    """
    if not frequencies:
        raise ValueError("Frequencies list cannot be empty")
    
    prob = [f / sum(frequencies) for f in frequencies]
    entropy = -sum(p * np.log2(p) for p in prob if p > 0)
    max_entropy = np.log2(len(prob)) if len(prob) > 1 else 0
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
    redundancy = 1 - normalized_entropy
    return {
        'entropy': round(entropy, rounding) if rounding is not None else entropy,
        'max_entropy': round(max_entropy, rounding) if rounding is not None else max_entropy,
        'normalized_entropy': round(normalized_entropy, rounding) if rounding is not None else normalized_entropy,
        'redundancy': round(redundancy, rounding) if rounding is not None else redundancy
    }


def zipf_distribution(frequencies: List[Union[int, float]], rounding: Optional[int] = None) -> List[float]:
    """
    Calculate Zipf distribution for a list of frequencies.
    
    Args:
        frequencies: List of term frequencies

    Returns:
        List of Zipfian probabilities
    """
    if not frequencies:
        raise ValueError("Frequencies list cannot be empty")

    
    sorted_frequencies = sorted(frequencies, reverse=True)
    total_terms = len(sorted_frequencies)
    zipf_probs = [1 / (i + 1) for i in range(total_terms)]
    sum_zipf_probs = sum(zipf_probs)
    
    zipf_distribution = [round(prob / sum_zipf_probs, rounding) if rounding is not None else prob / sum_zipf_probs 
                         for prob in zipf_probs]

    return zipf_distribution
