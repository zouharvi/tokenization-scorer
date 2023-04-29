from collections import Counter
import numpy as np

def _seq_len(text):
    # negate so that higher is always better
    return -np.average([len(l) for l in text])

def _renyi_efficiency(text, **kwargs):
    print("hit renyi")
    pass

def _renyi_entropy(text):
    pass

def _shannon_entropy(text):
    pass

def _shannon_efficiency(text):
    pass

def _percentile_freq(text):
    pass

def get_metric(metric):
    if metric in {"renyi", "renyi_efficiency"}:
        return _renyi_efficiency
    elif metric in {"renyi_entropy"}:
        return _renyi_entropy
    elif metric in {"entropy", "shannon_entropy"}:
        return _shannon_entropy
    elif metric in {"shannon", "shannon_efficiency"}:
        return _shannon_efficiency
    elif metric in {"sequence_length", "seq_len"}:
        return _seq_len
    elif metric in {"gowda", "percentile_freq", "perc_freq"}:
        return _percentile_freq
    else:
        raise Exception(f"Unknown metric name {metric}")