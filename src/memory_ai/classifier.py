"""The type classifier of lesson 54: bag-of-words + softmax regression.

Lesson 54 trains a NumPy classifier — vocabulary built from the train split
only, softmax regression fit by 300 steps of gradient descent with L2
regularisation, starting from zero weights — that predicts a memory's
`type` from its text.

Decision D5 (`course/research_gaps.md`, "Decisioni dell'autore del corso",
2026-08-09) settled how the package carries it: **trained at use time**,
never from committed parameters. The corpus is ~15 KB, the training is
NumPy-pure and deterministic (fixed hyperparameters, zero-initialised
weights), so retraining on the way in costs milliseconds and can never
silently drift from the corpus the way a saved-and-forgotten `W`/`b` could.
Two constraints follow directly from that decision: `fit()` is always
explicit — nothing trains on import — and its corpus path is a parameter
with a relative default, never an absolute one (`AGENTS.md`, no absolute
paths).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from memory_ai.text import tokenize

TYPES = ("episodic", "semantic", "preference")

# Relative to the current working directory, matching how the notebook
# reaches the same file from `notebooks/` with `Path('..') / 'datasets' /
# 'processed'`. A default must exist for the package to be usable without
# repeating the path everywhere, and it must not be absolute (AGENTS.md).
DEFAULT_TRAIN_PATH = Path("datasets/processed/memory_train.csv")

LEARNING_RATE = 0.5
L2_PENALTY = 1e-3
TRAIN_STEPS = 300


@dataclass(frozen=True)
class TrainingReport:
    """What `fit()` learned and how well it generalised, for auditing.

    `val_accuracy` and `majority_baseline` are `None` when `fit()` was
    called without a validation split — there is nothing dishonest to report
    in that case, so the report says so rather than fabricating a number.
    """

    vocabulary_size: int
    train_accuracy: float
    val_accuracy: float | None
    majority_baseline: float | None


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp = np.exp(shifted)
    result: np.ndarray = exp / exp.sum(axis=1, keepdims=True)
    return result


def _load_split(path: Path | str) -> pd.DataFrame:
    """Read a processed memory split, keeping only the three known types.

    Mirrors the notebook's `carica()`: a handful of rows carry `type ==
    "unknown"` (see `datasets/processed/memory_train.csv`) and neither the
    lesson nor the package trains or scores on them.
    """

    frame = pd.read_csv(path)
    return frame[frame["type"].isin(TYPES)].reset_index(drop=True)


class TypeClassifier:
    """Bag-of-words + softmax regression that predicts a memory's `type`.

    Mirrors lesson 54 gradient step for gradient step, so the extraction can
    be checked for parity against the notebook rather than trusted on
    inspection. Unfitted, it refuses to predict rather than guessing.
    """

    def __init__(self) -> None:
        self._vocabulary: dict[str, int] | None = None
        self._weights: np.ndarray | None = None
        self._bias: np.ndarray | None = None

    @property
    def is_fitted(self) -> bool:
        return self._weights is not None

    def fit(
        self,
        train_path: Path | str = DEFAULT_TRAIN_PATH,
        val_path: Path | str | None = None,
    ) -> TrainingReport:
        """Build the vocabulary from `train_path` and fit the weights on it.

        Training never happens implicitly (no constructor, no import-time
        side effect) — a caller always calls `fit()`, which is what keeps a
        parity check against the notebook meaningful: both run the exact
        same 300 steps from the exact same zero-initialised weights.
        """

        train = _load_split(train_path)

        vocabulary: dict[str, int] = {}
        for text in train["text"]:
            for word in tokenize(text):
                if word not in vocabulary:
                    vocabulary[word] = len(vocabulary)

        type_index = {name: i for i, name in enumerate(TYPES)}
        x_train = self._bag_of_words_matrix(train["text"], vocabulary)
        y_train = np.array([type_index[t] for t in train["type"]])

        num_classes = len(TYPES)
        weights = np.zeros((len(vocabulary), num_classes))
        bias = np.zeros(num_classes)
        y_onehot = np.eye(num_classes)[y_train]

        for _ in range(TRAIN_STEPS):
            probabilities = _softmax(x_train @ weights + bias)
            grad_w = x_train.T @ (probabilities - y_onehot) / len(x_train) + L2_PENALTY * weights
            grad_b = (probabilities - y_onehot).mean(axis=0)
            weights -= LEARNING_RATE * grad_w
            bias -= LEARNING_RATE * grad_b

        self._vocabulary = vocabulary
        self._weights = weights
        self._bias = bias

        train_accuracy = self._accuracy(x_train, y_train)
        majority = int(np.bincount(y_train).argmax())

        val_accuracy: float | None = None
        majority_baseline: float | None = None
        if val_path is not None:
            val = _load_split(val_path)
            x_val = self._bag_of_words_matrix(val["text"], vocabulary)
            y_val = np.array([type_index[t] for t in val["type"]])
            val_accuracy = self._accuracy(x_val, y_val)
            majority_baseline = float((y_val == majority).mean())

        return TrainingReport(
            vocabulary_size=len(vocabulary),
            train_accuracy=train_accuracy,
            val_accuracy=val_accuracy,
            majority_baseline=majority_baseline,
        )

    def predict(self, text: str) -> str:
        """Predict the type of one memory. Raises if `fit()` was never called."""

        if self._weights is None or self._bias is None or self._vocabulary is None:
            raise RuntimeError("classificatore non addestrato: chiamare fit() prima")
        vector = self._bag_of_words(text, self._vocabulary)
        logits = vector[None, :] @ self._weights + self._bias
        return TYPES[int(_softmax(logits).argmax())]

    def _accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        assert self._weights is not None and self._bias is not None
        predictions = _softmax(x @ self._weights + self._bias).argmax(axis=1)
        return float((predictions == y).mean())

    @staticmethod
    def _bag_of_words(text: str, vocabulary: dict[str, int]) -> np.ndarray:
        vector = np.zeros(len(vocabulary))
        for word in tokenize(text):
            index = vocabulary.get(word)
            if index is not None:
                vector[index] += 1.0
        return vector

    @classmethod
    def _bag_of_words_matrix(cls, texts: "pd.Series[str]", vocabulary: dict[str, int]) -> np.ndarray:
        return np.vstack([cls._bag_of_words(text, vocabulary) for text in texts])
