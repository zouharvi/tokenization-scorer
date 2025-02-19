# tokenization-scorer &nbsp;&nbsp;&nbsp;

[![PyPI Version](https://img.shields.io/pypi/v/tokenization-scorer.svg)](https://pypi.python.org/pypi/tokenization-scorer)
&nbsp;
[![test tokenization-scorer](https://github.com/zouharvi/tokenization-scorer/actions/workflows/test.yml/badge.svg)](https://github.com/zouharvi/tokenization-scorer/actions/workflows/test.yml)
&nbsp;
[![Paper](https://img.shields.io/badge/📜%20paper-481.svg)](https://aclanthology.org/2023.acl-long.284/)

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
tokenization_scorer.score(text1, metric="renyi", power=2.5)
> 0.8031528501359657

text2 = "pick @@e @@d pick @@l @@e @@d pick @@l @@e @@s"
tokenization_scorer.score(text2, metric="renyi", power=2.5)
> 0.9105681923824472
```

Use `tokenization-scorer -h` to get an overview of supported metrics.
This package is a side-product of the paper [Tokenization and the Noiseless Channel](https://aclanthology.org/2023.acl-long.284/) which has [code here](https://github.com/zouharvi/tokenization-principle).

```
@inproceedings{tokenization_noiseless, 
    title={Tokenization and the Noiseless Channel},
    author={Zouhar, Vilém and Meister, Clara and Gastaldi, Juan Luis and Sachan, Mrinmaya and Cotterell, Ryan},
    booktitle={Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics},
    year={2023},
    url={https://aclanthology.org/2023.acl-long.284/},
}
```
