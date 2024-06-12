from typing import Union, Generator, List
import argparse, itertools
import tqdm
from .metrics import get_metric

def score(
    text: Union[str, Generator, List[Generator]],
    metric: str = "renyi",
    **kwargs
) -> float:
    # be generous when parsing the input to allow for list of files and strings
    if type(text) == str:
        text = [l.split() for l in tqdm.tqdm(text.split("\n"))]
    else:
        text, peekable = itertools.tee(text)
        if type(next(peekable)) != str:
            # flatten once more
            text = (w for l in text for w in tqdm.tqdm(l))
        text = (l.rstrip("\n").split() for l in tqdm.tqdm(text))

    # cleanup (remove empty lines and words)
    text = (
        (w.strip() for w in l if w.strip())
        for l in text
    )
    text = (l for l in text if l)
    score_val = get_metric(metric)(text, **kwargs)

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
        help="""
            Available metrics: renyi_efficiency (default), renyi_entropy, shannon_efficiency, 
            shannon_entropy, percentile_freq, bits, sequence_len.
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
