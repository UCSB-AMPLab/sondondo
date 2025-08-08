import numpy as np
from typing import List, Union, Optional, Dict

Number = Union[int, float]


def cv(frequencies: List[Number], rounding: Optional[int] = None) -> float:
    """
    Coefficient of Variation (CV) calculation.
    
    Args:
        frequencies: List of term frequencies
        
    Returns:
        Coefficient of Variation as a float
    """
    if not frequencies:
        raise ValueError("Frequencies list cannot be empty")
    if any(f < 0 for f in frequencies):
        raise ValueError("Frequencies must be non-negative")

    arr = np.asarray(frequencies, dtype=float)
    mean = arr.mean()

    if mean == 0:
        return 0.0
    else:
        std = arr.std(ddof=1) if arr.size > 1 else 0.0
        val = float(std / mean)

    return round(val, rounding) if rounding is not None else val


def shannon_entropy(frequencies: List[Number], rounding: Optional[int] = None) -> Dict[str, float]:
    """
    Calculate Shannon Entropy for a list of frequencies.
    
    Args:
        frequencies: List of term frequencies

    Returns:
        Shannon Entropy as a dictionary with keys 'entropy', 'max_entropy', 'normalized_entropy', and 'redundancy'
    """
    if not frequencies:
        raise ValueError("Frequencies list cannot be empty")
    if any(f < 0 for f in frequencies):
        raise ValueError("Frequencies must be non-negative")

    total = float(sum(frequencies))
    k = len(frequencies)

    if total == 0 or k == 0:
        H = 0.0
        H_max = 0.0
        norm = 0.0
    else:
        p = [f / total for f in frequencies if f > 0]
        H = -np.sum(np.array(p) * np.log2(p)) if p else 0.0
        H_max = np.log2(k) if k > 1 else 0.0
        norm = (H / H_max) if H_max > 0 else 0.0

    red = 1.0 - norm

    def r(x): return round(x, rounding) if rounding is not None else x
    
    return {
        'entropy': r(H),
        'max_entropy': r(H_max),
        'normalized_entropy': r(norm),
        'redundancy': r(red)
    }


def zipf_distribution(frequencies: List[Number], rounding: Optional[int] = None) -> List[float]:
    """
    Theoretical Zipf probabilities for k terms: p_r ∝ 1/r. Does NOT use input values except length.
    Useful as a reference curve to compare against empirical rank-frequency.
    """
    if not frequencies:
        raise ValueError("Frequencies list cannot be empty")
    k = len(frequencies)
    z = [1.0 / (i + 1) for i in range(k)]
    s = sum(z)
    dist = [zi / s for zi in z]
    return [round(x, rounding) if rounding is not None else x for x in dist]


def empirical_rank_freq(frequencies: List[Number], normalize: bool = True, rounding: Optional[int] = None) -> List[float]:
    """
    Empirical rank-frequency curve: sort freqs desc and (optionally) convert to probabilities.
    """
    if not frequencies:
        raise ValueError("Frequencies list cannot be empty")
    if any(f < 0 for f in frequencies):
        raise ValueError("Frequencies must be non-negative")

    sorted_freqs = sorted((float(f) for f in frequencies), reverse=True)
    if normalize:
        total = sum(sorted_freqs)
        vals = [f / total if total > 0 else 0.0 for f in sorted_freqs]
    else:
        vals = sorted_freqs
    return [round(x, rounding) if rounding is not None else x for x in vals]