# `tokenization-scorer` [![PyPI Version](https://img.shields.io/pypi/v/tokenization-scorer.svg)](https://pypi.python.org/pypi/tokenization-scorer)

Simple package for evaluating text tokenizations.
The input is a text (list of files or stdin) and output a single number.
The higher the number, the better the tokenization.
The intended workflow is to try multiple tokenizations and select the one with the highest number.

It can be used from the command line:

```bash
pip3 install tokenization-scorer

tokenization-scorer -i en-de.tokenized_with_unigramlm.{en,de}
> 0.4826

tokenization-scorer -i en-de.tokenized_with_wordpiece.{en,de}
> 0.5047
```

or within Python:

```python
import tokenization_scorer
text1 = "pick @@ed pick @@l @@ed pick @@les"
tokenization_scorer.score(text1, metric="renyi", power=3.0)
> 0.8031528501359657

text2 = "pick @@e @@d pick @@l @@e @@d pick @@l @@e @@s"
tokenization_scorer.score(text2, metric="renyi", power=3.0)
> 0.9105681923824472
```

Use `tokenization-scorer -h` to get an overview of supported metrics.
This package is a side-product of the paper "Tokenization and the Noiseless Channel" (citation and paper WIP).

<!-- 
python3 -m build
python3 -m twine upload dist/*
-->
