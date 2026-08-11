"""Tests for the lesson 54 type classifier.

`test_matches_the_notebook_on_the_full_corpus` is the parity check: it
re-runs the exact NumPy computation lesson 54 has in its cells, independent
of `memory_ai.classifier`, and compares every prediction on the full train
and validation split. A silent divergence between the notebook and the
package would show up here, not just "the tests still pass".
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from memory_ai.classifier import DEFAULT_TRAIN_PATH, TrainingReport, TypeClassifier

PROCESSED = Path(__file__).resolve().parents[1] / "datasets" / "processed"
TRAIN_CSV = PROCESSED / "memory_train.csv"
VAL_CSV = PROCESSED / "memory_val.csv"


def test_default_train_path_is_relative() -> None:
    # AGENTS.md: no absolute paths committed anywhere in the repository.
    assert not DEFAULT_TRAIN_PATH.is_absolute()


def test_unfitted_classifier_refuses_to_predict() -> None:
    with pytest.raises(RuntimeError, match="non addestrato"):
        TypeClassifier().predict("Marco visited Glasgow")


def test_fit_returns_a_training_report() -> None:
    report = TypeClassifier().fit(TRAIN_CSV)
    assert isinstance(report, TrainingReport)
    assert report.vocabulary_size > 0
    assert 0.0 <= report.train_accuracy <= 1.0
    assert report.val_accuracy is None
    assert report.majority_baseline is None


def test_fit_with_validation_reports_both_accuracies_and_baseline() -> None:
    report = TypeClassifier().fit(TRAIN_CSV, VAL_CSV)
    assert report.val_accuracy is not None
    assert report.majority_baseline is not None
    assert 0.0 <= report.val_accuracy <= 1.0
    assert 0.0 <= report.majority_baseline <= 1.0


def test_reading_the_text_beats_the_majority_baseline() -> None:
    # The non-regression check lesson 54 ends on: if bag-of-words + softmax
    # cannot beat guessing the majority class, the text carries no signal.
    report = TypeClassifier().fit(TRAIN_CSV, VAL_CSV)
    assert report.val_accuracy is not None and report.majority_baseline is not None
    assert report.val_accuracy > report.majority_baseline


def test_predictions_are_one_of_the_three_types() -> None:
    clf = TypeClassifier()
    clf.fit(TRAIN_CSV)
    for text in [
        "The user prefers tea.",
        "Marco went to Rome yesterday.",
        "Water boils at 100C.",
    ]:
        assert clf.predict(text) in ("episodic", "semantic", "preference")


def test_fit_is_deterministic() -> None:
    first = TypeClassifier()
    first.fit(TRAIN_CSV, VAL_CSV)
    second = TypeClassifier()
    second.fit(TRAIN_CSV, VAL_CSV)
    assert first.fit(TRAIN_CSV, VAL_CSV) == second.fit(TRAIN_CSV, VAL_CSV)
    assert first.predict("Marco visited Glasgow") == second.predict("Marco visited Glasgow")


def test_vocabulary_ignores_words_seen_only_in_validation(tmp_path: Path) -> None:
    # No leakage: the vocabulary comes from the train split only, so a word
    # that appears only in validation cannot move a prediction at all - its
    # bag-of-words vector is all zero, exactly like an empty text.
    train_csv = tmp_path / "train.csv"
    pd.DataFrame(
        {
            "text": ["Marco visited Rome", "the user prefers tea", "water boils fast"],
            "type": ["episodic", "preference", "semantic"],
        }
    ).to_csv(train_csv, index=False)

    clf = TypeClassifier()
    clf.fit(train_csv)
    assert clf.predict("zzzqqqneverseen") == clf.predict("")


def test_matches_the_notebook_on_the_full_corpus() -> None:
    """Re-implements lesson 54's cells independently and checks parity.

    Same regex tokeniser, same vocabulary-from-train-only rule, same 300
    fixed-hyperparameter gradient steps from zero weights: if this ever
    disagrees with `TypeClassifier`, the extraction silently changed the
    lesson's numbers.
    """

    types = ["episodic", "semantic", "preference"]
    type_index = {t: i for i, t in enumerate(types)}

    def load(path: Path) -> pd.DataFrame:
        frame = pd.read_csv(path)
        return frame[frame["type"].isin(types)].reset_index(drop=True)

    train, val = load(TRAIN_CSV), load(VAL_CSV)

    def tok(text: str) -> list[str]:
        return re.findall(r"[a-zA-Z]+", str(text).lower())

    vocab: dict[str, int] = {}
    for text in train["text"]:
        for word in tok(text):
            if word not in vocab:
                vocab[word] = len(vocab)

    def bow(text: str) -> np.ndarray:
        vector = np.zeros(len(vocab))
        for word in tok(text):
            if word in vocab:
                vector[vocab[word]] += 1.0
        return vector

    x_train = np.vstack([bow(t) for t in train["text"]])
    y_train = np.array([type_index[t] for t in train["type"]])
    x_val = np.vstack([bow(t) for t in val["text"]])

    def softmax(z: np.ndarray) -> np.ndarray:
        shifted = z - z.max(axis=1, keepdims=True)
        exp = np.exp(shifted)
        return exp / exp.sum(axis=1, keepdims=True)

    num_classes = len(types)
    weights = np.zeros((len(vocab), num_classes))
    bias = np.zeros(num_classes)
    lr, lam = 0.5, 1e-3
    y_onehot = np.eye(num_classes)[y_train]

    for _ in range(300):
        probabilities = softmax(x_train @ weights + bias)
        grad_w = x_train.T @ (probabilities - y_onehot) / len(x_train) + lam * weights
        grad_b = (probabilities - y_onehot).mean(axis=0)
        weights -= lr * grad_w
        bias -= lr * grad_b

    reference_train_predictions = [types[i] for i in softmax(x_train @ weights + bias).argmax(axis=1)]
    reference_val_predictions = [types[i] for i in softmax(x_val @ weights + bias).argmax(axis=1)]

    clf = TypeClassifier()
    report = clf.fit(TRAIN_CSV, VAL_CSV)

    assert report.vocabulary_size == len(vocab)
    package_train_predictions = [clf.predict(t) for t in train["text"]]
    package_val_predictions = [clf.predict(t) for t in val["text"]]

    assert package_train_predictions == reference_train_predictions
    assert package_val_predictions == reference_val_predictions
