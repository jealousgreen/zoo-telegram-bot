from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from bot.data.models import AnswerOption, Animal
from bot.data.quiz import ANIMALS


def empty_scores() -> dict[str, int]:
    return {animal_id: 0 for animal_id in ANIMALS}


def apply_answer(scores: dict[str, int], answer: AnswerOption) -> dict[str, int]:
    updated = dict(scores)
    for animal_id, points in answer.weights.items():
        updated[animal_id] = updated.get(animal_id, 0) + points
    return updated


def score_answers(answers: Iterable[AnswerOption]) -> dict[str, int]:
    scores: dict[str, int] = defaultdict(int)
    for animal_id in ANIMALS:
        scores[animal_id] = 0
    for answer in answers:
        for animal_id, points in answer.weights.items():
            scores[animal_id] += points
    return dict(scores)


def choose_animal(scores: dict[str, int]) -> Animal:
    """Deterministic max-score choice.

    If scores tie, the animal that appears earlier in ANIMALS wins. This keeps the
    result stable and easy to explain during a demo.
    """
    best_id = max(ANIMALS.keys(), key=lambda animal_id: (scores.get(animal_id, 0), -list(ANIMALS).index(animal_id)))
    return ANIMALS[best_id]


def top_scores(scores: dict[str, int], limit: int = 3) -> list[tuple[str, int]]:
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)[:limit]
