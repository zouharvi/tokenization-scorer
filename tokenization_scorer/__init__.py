from typing import Union, Generator, List
import argparse
import tqdm
from .metrics import get_metric

def score(
    text: Union[str, Generator, List[Generator]],
    metric: str = "renyi",
    **kwargs
) -> float:
    # be generous when parsing the input to allow for list of files and strings
    if type(text) == str:
        text = [l for l in tqdm.tqdm(text.split("\n"))]
    else:
        text = list(text)
        if type(text[0]) != str:
            # flatten once more
            text = [w for l in text for w in tqdm.tqdm(l)]
        text = [l.rstrip("\n").split() for l in tqdm.tqdm(text)]

    # cleanup (remove empty lines and words)
    text = [
        [w.strip() for w in l if w.strip()]
        for l in text
    ]
    text = [l for l in text if l]
    
    score_val = get_metric(metric)(text, **kwargs)

    return score_val


def entry():
    args = argparse.ArgumentParser(description="TODO")
    args.add_argument("-i", "--input", nargs="+", default=None)
    args.add_argument("-m", "--metric", default="renyi")
    args.add_argument("-e", "--extra", nargs="+", default=[])
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
        **{x.split("=")[0]: x.split("=")[1] for x in args.extra}
    )
    print(score_val)
