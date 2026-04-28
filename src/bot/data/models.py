from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Animal:
    id: str
    title: str
    short_title: str
    species_url: str
    description: str
    adoption_pitch: str
    photo_url: str | None = None


@dataclass(frozen=True)
class AnswerOption:
    text: str
    weights: dict[str, int]


@dataclass(frozen=True)
class Question:
    text: str
    options: list[AnswerOption]
