from typing import List, Union, Generator
import argparse

def score(
    text: Union[str, Generator[str], Generator[Generator[str]]],
    metric: str = "renyi"
) -> float:
    if type(text) == str:
        text = text.split()
    else:
        text = list(text)
        if type(text[0]) == str:
            text = [w for l in text for w in l.split()]
        else:
            text = [list(l) for l in text]


    # cleanup
    text = [w.strip() for w in text]
    text = [w for w in text if w]

    pass

def entry():
    args = argparse.ArgumentParser()
    args.add_argument("-i", "--input", nargs="+", default=None)
    args.add_argument("-m", "--metric", default="renyi")
    args = args.parse_args()
    print("hello there!")