# %%
import tokenization_scorer

text1 = "pick @@ed pick @@l @@ed pick @@les"
text2 = "pick @@e @@d pick @@l @@e @@d pick @@l @@e @@s"


def test_renyi():
    assert abs(tokenization_scorer.score(text1, metric="renyi", power=2.5) - 0.8265064834225245) < 0.001
    assert abs(tokenization_scorer.score(text2, metric="renyi", power=2.5) - 0.9204840242168808) < 0.001
    assert abs(tokenization_scorer.score(text1, metric="renyi_entropy", power=2.5) - 1.653012966845049) < 0.001
    assert abs(tokenization_scorer.score(text2, metric="renyi_entropy", power=2.5) - 2.1372977167241545) < 0.001


def test_shannon():
    assert abs(tokenization_scorer.score(text1, metric="shannon_efficiency") - 0.9211854965885544) < 0.001
    assert abs(tokenization_scorer.score(text2, metric="shannon_efficiency") - 0.9609557933859342) < 0.001
    assert abs(tokenization_scorer.score(text1, metric="shannon_entropy") - 1.8423709931771088) < 0.001
    assert abs(tokenization_scorer.score(text2, metric="shannon_entropy") - 2.2312702546075758) < 0.001


def test_percentile_freq():
    assert abs(tokenization_scorer.score(text1, metric="percentile_freq", perc_start=0.03, perc_end=0.83)- 0.857142857142857) < 0.001
    assert abs(tokenization_scorer.score(text2, metric="percentile_freq", perc_start=0.03, perc_end=0.83)- 0.9090909090909092) < 0.001
    assert abs(tokenization_scorer.score(text1, metric="percentile_freq", perc_start=0.3, perc_end=0.6)- 0.2857142857142857) < 0.001
    assert abs(tokenization_scorer.score(text2, metric="percentile_freq", perc_start=0.3, perc_end=0.6)- 0.45454545454545453) < 0.001

def test_bits():
    assert abs(tokenization_scorer.score(text1, metric="bits") - -14.0) < 0.001
    assert abs(tokenization_scorer.score(text2, metric="bits") - -25.541209043760983) < 0.001


def test_seq_len():
    assert abs(tokenization_scorer.score(text1, metric="sequence_len") - -7) <= 0
    assert abs(tokenization_scorer.score(text2, metric="sequence_len") - -11) <= 0
    assert abs(tokenization_scorer.score([text1], metric="sequence_len") - -7) <= 0
    assert abs(tokenization_scorer.score([text2], metric="sequence_len") - -11) <= 0