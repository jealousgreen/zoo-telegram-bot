from bot.data.quiz import QUESTIONS
from bot.services.scoring import choose_animal, empty_scores, score_answers


def test_score_answers_returns_known_animal():
    answers = [question.options[0] for question in QUESTIONS]
    scores = score_answers(answers)
    animal = choose_animal(scores)
    assert animal.id in scores
    assert scores[animal.id] == max(scores.values())


def test_empty_scores_contains_all_animals():
    scores = empty_scores()
    assert scores
    assert all(value == 0 for value in scores.values())
