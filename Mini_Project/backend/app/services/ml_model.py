"""
Module 3 — Adaptive Learning & Personalization
Syllabus mapping: Unit IV (inductive learning, decision trees,
                            statistical learning)

Trains a scikit-learn DecisionTreeClassifier on the user's own
task-completion history: (task_type, time_of_day, planned_duration) ->
completed_on_time. Predictions are then used to (a) recommend the best
time-of-day per category and (b) feed better duration/likelihood
estimates back to Module 1.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


MIN_ROWS_TO_TRAIN = 6


@dataclass
class TrainedModel:
    model: DecisionTreeClassifier
    category_encoder: LabelEncoder
    categories: List[str]
    accuracy: Optional[float]
    n_samples: int


def train_decision_tree(history_rows: List[dict]) -> Optional[TrainedModel]:
    """
    history_rows: list of dicts with keys
      task_type, time_of_day, planned_duration, completed_on_time
    """
    if len(history_rows) < MIN_ROWS_TO_TRAIN:
        return None

    categories = sorted({r["task_type"] for r in history_rows})
    encoder = LabelEncoder()
    encoder.fit(categories)

    X = np.array([
        [encoder.transform([r["task_type"]])[0], r["time_of_day"], r["planned_duration"]]
        for r in history_rows
    ])
    y = np.array([1 if r["completed_on_time"] else 0 for r in history_rows])

    accuracy = None
    if len(history_rows) >= 10 and len(set(y.tolist())) > 1:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        clf = DecisionTreeClassifier(max_depth=4, random_state=42)
        clf.fit(X_train, y_train)
        accuracy = float(clf.score(X_test, y_test))
        clf.fit(X, y)  # refit on all data for production use
    else:
        clf = DecisionTreeClassifier(max_depth=4, random_state=42)
        clf.fit(X, y)

    return TrainedModel(model=clf, category_encoder=encoder, categories=categories, accuracy=accuracy, n_samples=len(history_rows))


def recommend_best_hours(trained: TrainedModel, top_n_per_category: int = 1) -> List[dict]:
    """For each category, scan hours 0-23 and predict on-time probability."""
    recs = []
    for cat in trained.categories:
        cat_code = trained.category_encoder.transform([cat])[0]
        best_hour, best_prob = None, -1.0
        for hour in range(6, 23):  # sane working hours
            X = np.array([[cat_code, hour, 60]])
            proba = trained.model.predict_proba(X)[0]
            classes = trained.model.classes_
            prob_on_time = proba[list(classes).index(1)] if 1 in classes else 0.0
            if prob_on_time > best_prob:
                best_prob, best_hour = prob_on_time, hour
        if best_hour is not None:
            recs.append({
                "category": cat,
                "best_hour": best_hour,
                "confidence": round(float(best_prob), 2),
                "message": (
                    f'You complete "{cat}" tasks on time '
                    f'{round(best_prob * 100)}% of the time when scheduled around '
                    f'{best_hour if best_hour <= 12 else best_hour - 12}{"AM" if best_hour < 12 else "PM"}.'
                ),
            })
    recs.sort(key=lambda r: -r["confidence"])
    return recs
