# `tokenization-scorer`

Simple package for evaluating text tokenizations.
The input is a text (list of files or stdin) and output a single number.
The higher the number, the better the tokenization.
The intended workflow is to try multiple tokenizations and select the one with the highest number.

```
pip3 install tokenization-scorer

tokenization-scorer -i en-de.tokenized_with_unigramlm.{en,de}
> 0.4826

tokenization-scorer -i en-de.tokenized_with_wordpiece.{en,de}
> 0.5047
```

This package is a side-product of the paper "Tokenization and the Noiseless Channel" (citation and paper WIP, [experiment repository](github.com/zouharvi/tokenization-principle)).