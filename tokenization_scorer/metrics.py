from collections import Counter
import numpy as np
import sys

def get_prob_distribution(text):
    words_freqs = Counter((w for l in text for w in l)).most_common()
    total_subwords = sum(x[1] for x in words_freqs)
    freqs = [
        freq
        for _, freq in words_freqs
    ]
    probs = [
        freq / total_subwords
        for freq in freqs
    ]
    vocab_size = len(words_freqs)
    return freqs, probs, vocab_size

def _seq_len(text, **kwargs):
    # negate so that higher is always better
    # summing 1s won't expand the whole generator into memory
    return -sum([sum(1 for _ in l) for l in text])

def _renyi_efficiency(text, **kwargs):
    # set default
    if "power" not in kwargs:
        print("Setting power to 3.0 (default)", file=sys.stderr)
        kwargs["power"] = 3.0

    _, word_probs, vocab_size = get_prob_distribution(text)

    if kwargs["power"] == 1.0:
        return _shannon_efficiency(text, **kwargs)
    else:
        scale = 1 / (1 - kwargs["power"])

    # override observed vocabulary size
    if "vocab" in kwargs:
        vocab_size = kwargs["vocab"]
    print(f"Vocabulary size {vocab_size}", file=sys.stderr)

    val = scale * np.log2(np.sum(
        np.array(word_probs) ** kwargs["power"]
    )) / np.log2(vocab_size)
    return val


def _renyi_entropy(text, **kwargs):
    # set default
    if "power" not in kwargs:
        print("Setting power to 3.0 (default)", file=sys.stderr)
        kwargs["power"] = 3.0

    _, word_probs, _ = get_prob_distribution(text)

    if kwargs["power"] == 1.0:
        return _shannon_entropy(text, **kwargs)
    else:
        scale = 1 / (1 - kwargs["power"])

    val = scale * np.log2(np.sum(
        np.array(word_probs) ** kwargs["power"]
    ))
    return val


def _shannon_entropy(text, **kwargs):
    _, word_probs, _ = get_prob_distribution(text)
    return -np.sum(word_probs * np.log2(word_probs))


def _shannon_efficiency(text, **kwargs):
    _, word_probs, vocab_size = get_prob_distribution(text)
    
    # override observed vocabulary size
    if "vocab" in kwargs:
        vocab_size = kwargs["vocab"]
    print(f"Vocabulary size {vocab_size}", file=sys.stderr)
    
    return -np.sum(word_probs * np.log2(word_probs)) / np.log2(vocab_size)


def _percentile_freq(text, **kwargs):
    # set default
    if "perc_start" not in kwargs:
        print("Setting perc_start to 0.03 (default)", file=sys.stderr)
        kwargs["perc_start"] = 0.03
    if "perc_end" not in kwargs:
        print("Setting perc_end to 0.83 (default)", file=sys.stderr)
        kwargs["perc_end"] = 0.83

    _, word_probs, _ = get_prob_distribution(text)

    start_i = min(
        int(len(word_probs) * kwargs["perc_start"]),
        len(word_probs) - 1
    )
    end_i = min(
        int(len(word_probs) * kwargs["perc_end"]), len(word_probs) - 1
    )
    if start_i == end_i:
        start_i = max(0, start_i - 1)
    if start_i == end_i:
        end_i = min(len(word_probs) - 1, end_i + 1)

    indicies = range(start_i, end_i)

    # sparsely sum frequencies
    # indicies = [int(x) for x in np.linspace(
    #     start_i, end_i + 0.001, 10
    # )]

    # get mass between indicies
    val = np.sum([
        word_probs[i]
        for i in indicies
    ])

    return val


def _bits(text, **kwargs):
    freqs, _, vocab_size = get_prob_distribution(text)
    # negate so that higher is better
    return -sum(freqs) * np.log2(vocab_size)


def _coefficient_variation(text, **kwargs):
    freqs, _, _ = get_prob_distribution(text)
    return float(np.std(freqs) / np.average(freqs))


def _quartile_dispersion(text, **kwargs):
    freqs, _, _ = get_prob_distribution(text)
    perc_start = kwargs.get("perc_start", kwargs.get("freq_alpha_start", 0.25))
    perc_end = kwargs.get("perc_end", kwargs.get("freq_alpha_end", 0.75))
    index_start = int(len(freqs) * perc_start)
    index_end = min(int(len(freqs) * perc_end), len(freqs) - 1)
    denom = freqs[index_end] + freqs[index_start]
    if denom == 0:
        return 0.0
    return float((freqs[index_end] - freqs[index_start]) / denom)


def _inter_quantile_range(text, **kwargs):
    freqs, probs, _ = get_prob_distribution(text)
    base = kwargs.get("base_vals", "probs")
    vals = probs if base == "probs" else freqs
    perc_start = kwargs.get("perc_start", kwargs.get("freq_alpha_start", 0.25))
    perc_end = kwargs.get("perc_end", kwargs.get("freq_alpha_end", 0.75))
    index_start = int(len(vals) * perc_start)
    index_end = min(int(len(vals) * perc_end), len(vals) - 1)
    return float(vals[index_end] - vals[index_start])


def _aggregate_deviation(text, **kwargs):
    freqs, _, _ = get_prob_distribution(text)
    central = kwargs.get("central_measure", "mean")
    if central == "mean":
        c = np.mean(freqs)
    elif central == "median":
        c = np.median(freqs)
    elif central == "mode":
        _, counts = np.unique(freqs, return_counts=True)
        mode_idx = np.argwhere(counts == np.max(counts))
        c = freqs[mode_idx[0][0]]
    else:
        raise Exception(f"Unknown central measure {central}")

    power = kwargs.get("power", 1.0)
    if np.ceil(power) != power:
        vals = np.abs(np.array(freqs) - c) ** power
    else:
        vals = (np.array(freqs) - c) ** power

    agg = kwargs.get("aggregator", "mean")
    if agg == "mean":
        return float(np.average(vals))
    elif agg == "median":
        return float(np.median(vals))
    elif agg == "sqrt":
        return float(np.sqrt(abs(np.sum(vals) / max(len(vals) - 1, 1))))
    else:
        raise Exception(f"Unknown aggregator {agg}")


def get_metric(metric):
    if metric in {"renyi", "renyi_efficiency", "renyi_eff"}:
        return _renyi_efficiency
    elif metric in {"renyi_entropy"}:
        return _renyi_entropy
    elif metric in {"shannon", "shannon_efficiency", "entropy_eff"}:
        return _shannon_efficiency
    elif metric in {"entropy", "shannon_entropy"}:
        return _shannon_entropy
    elif metric in {"sequence_length", "sequence_len", "seq_len"}:
        return _seq_len
    elif metric in {"document_length", "doc_len", "subwords"}:
        return _seq_len
    elif metric in {"gowda", "percentile_freq", "perc_freq"}:
        return _percentile_freq
    elif metric in {"bits"}:
        return _bits
    elif metric in {"coefficient_variation", "cov", "coeff_var"}:
        return _coefficient_variation
    elif metric in {"quartile_dispersion", "qd"}:
        return _quartile_dispersion
    elif metric in {"inter_quantile_range", "iqr"}:
        return _inter_quantile_range
    elif metric in {"aggregate_deviation", "agg_deviation"}:
        return _aggregate_deviation
    else:
        raise Exception(f"Unknown metric name {metric}")
