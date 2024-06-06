from collections import Counter
import numpy as np
import sys

def get_prob_distribution(text):
    words_freqs = list(Counter((w for l in text for w in l)).most_common())
    total_subwords = sum([x[1] for x in words_freqs])
    freqs = [
        freq
        for word, freq in words_freqs
    ]
    probs = [
        freq / total_subwords
        for freq in freqs
    ]
    vocab_size = len(words_freqs)
    return freqs, probs, vocab_size

def _seq_len(text, **kwargs):
    # negate so that higher is always better
    return -np.average([len(l) for l in text])

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

    val = scale * np.log2(np.sum([
        prob**kwargs["power"]
        for prob in word_probs
    ])) / np.log2(vocab_size)
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

    val = scale * np.log2(np.sum([
        prob**kwargs["power"]
        for prob in word_probs
    ]))
    return val


def _shannon_entropy(text, **kwargs):
    _, word_probs, _ = get_prob_distribution(text)
    return -np.sum(word_probs * np.log2(word_probs))


def _shannon_efficiency(text, **kwargs):
    _, word_probs, vocab_size = get_prob_distribution(text)
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
    _, _, vocab_size = get_prob_distribution(text)
    # negate so that higher is better
    return -len([w for l in text for w in l]) * np.log2(vocab_size)


def get_metric(metric):
    if metric in {"renyi", "renyi_efficiency"}:
        return _renyi_efficiency
    elif metric in {"renyi_entropy"}:
        return _renyi_entropy
    elif metric in {"shannon", "shannon_efficiency"}:
        return _shannon_efficiency
    elif metric in {"entropy", "shannon_entropy"}:
        return _shannon_entropy
    elif metric in {"sequence_length", "seq_len"}:
        return _seq_len
    elif metric in {"gowda", "percentile_freq", "perc_freq"}:
        return _percentile_freq
    elif metric in {"bits"}:
        return _bits
    else:
        raise Exception(f"Unknown metric name {metric}")
