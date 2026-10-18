from typing import Union, Generator, List
import argparse, itertools
import tqdm
from .metrics import get_metric

METRIC_TITLES = {
    "renyi": "Rényi efficiency",
    "renyi_efficiency": "Rényi efficiency",
    "renyi_eff": "Rényi efficiency",
    "renyi_entropy": "Rényi entropy",
    "shannon": "Entropy efficiency",
    "shannon_efficiency": "Entropy efficiency",
    "entropy_eff": "Entropy efficiency",
    "entropy": "Entropy",
    "shannon_entropy": "Entropy",
    "seq_len": "Sequence length",
    "sequence_length": "Sequence length",
    "sequence_len": "Sequence length",
    "doc_len": "Document length",
    "document_length": "Document length",
    "subwords": "Subwords",
    "bits": "Encoded bits with fixed-width",
    "gowda": "Percentile freq.",
    "percentile_freq": "Percentile freq.",
    "perc_freq": "Percentile freq.",
    "coefficient_variation": "Coefficient of variation",
    "cov": "Coefficient of variation",
    "coeff_var": "Coefficient of variation",
    "quartile_dispersion": "Quartile dispersion",
    "qd": "Quartile dispersion",
    "inter_quantile_range": "Inter-quantile range",
    "iqr": "Inter-quantile range",
    "aggregate_deviation": "Aggregate deviation",
    "agg_deviation": "Aggregate deviation",
}

def score(
    text: Union[str, Generator, List[Generator]],
    metric: str = "renyi",
    verbose: bool = False,
    **kwargs
) -> float:
    # be generous when parsing the input to allow for list of files and strings
    if type(text) == str:
        text = [l.split() for l in tqdm.tqdm(text.split("\n"), disable=not verbose)]
        line_count = len(text)
    else:
        text, peekable1, peekable2 = itertools.tee(text, 3)
        line_count = len(list(peekable2))  # assumes outer iteration to be lines
        if type(next(peekable1)) != str:
            # flatten once more
            text = (w for l in text for w in tqdm.tqdm(l, disable=not verbose))
        text = (l.rstrip("\n").split() for l in tqdm.tqdm(text, disable=not verbose))

    # cleanup (remove empty lines and words)
    text = (
        (w.strip() for w in l if w.strip())
        for l in text
    )
    text = (l for l in text if l)
    score_val = get_metric(metric)(text, **kwargs)

    # line-normalize sequence length
    if metric in {"sequence_len", "seq_len"}:
        score_val /= line_count

    return score_val


def entry():
    args = argparse.ArgumentParser(description="""
        Simple package for evaluating text tokenizations. The input is a text (list of files or stdin) and output a single number.
        The higher the number, the better the tokenization.
        The intended workflow is to try multiple tokenizations and select the one with the highest number.
    """)
    args.add_argument("-i", "--input", nargs="+", default=None)
    args.add_argument(
        "-m", "--metric", default="renyi",
        choices=[
            "renyi", "renyi_efficiency", "renyi_entropy",
            "shannon_efficiency", "shannon_entropy", "shannon", "entropy",
            "sequence_length", "seq_len", "document_length", "doc_len", "subwords",
            "gowda", "percentile_freq", "perc_freq", "bits",
            "coefficient_variation", "cov", "coeff_var",
            "quartile_dispersion", "qd",
            "inter_quantile_range", "iqr",
            "aggregate_deviation", "agg_deviation",
        ],
        help="""
            Which metric to use.
        """
    )
    args.add_argument(
        "-e", "--extra", nargs="+", default=[],
        help="""
            Pass parameters to the metrics. If no parameters are specified, defaults are used.
            All renyi metrics require `-e power=FLOAT` parameter (default 3.0). percentile_freq metric requires `-e perc_start=FLOAT -e perc_end=FLOAT`.
            Entropy efficiency metrics can also take `-e vocab=INT` to override the observed vocabulary size.
        """
    )
    args = args.parse_args()

    if args.input is None:
        import sys
        args.input = [sys.stdin]
    else:
        args.input = [open(f, "r") for f in args.input]

    score_val = score(
        [f.readlines() for f in args.input],
        metric=args.metric,
        # extra metrics argument
        **{x.split("=")[0]: float(x.split("=")[1]) for x in args.extra}
    )
    print(score_val)
