from __future__ import annotations

import html
import logging
from typing import Any

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, URLInputFile

from bot.config import Settings
from bot.data.quiz import ANIMALS, QUESTIONS
from bot.keyboards import question_keyboard, result_keyboard
from bot.services.photo_provider import resolve_photo_url
from bot.services.scoring import apply_answer, choose_animal, empty_scores, top_scores
from bot.services.storage import Storage

router = Router(name="quiz")
logger = logging.getLogger(__name__)


class QuizState(StatesGroup):
    answering = State()
    waiting_feedback = State()


def _format_question(index: int) -> str:
    question = QUESTIONS[index]
    return f"<b>{html.escape(question.text)}</b>\n\nВыберите вариант, который ближе всего."


async def _ask_question(message: Message, state: FSMContext, index: int) -> None:
    await state.set_state(QuizState.answering)
    await state.update_data(question_index=index)
    await message.answer(_format_question(index), reply_markup=question_keyboard(QUESTIONS[index]))


@router.callback_query(F.data == "quiz:start")
async def start_quiz(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await state.set_state(QuizState.answering)
    await state.update_data(scores=empty_scores(), answers=[], question_index=0)
    await callback.message.answer(
        "Отлично, начинаем! Отвечайте честно: у тотемных животных хорошая память 🐾"
    )
    await _ask_question(callback.message, state, 0)


@router.callback_query(F.data.startswith("quiz:answer:"), QuizState.answering)
async def answer_question(
    callback: CallbackQuery,
    state: FSMContext,
    database: Storage,
    settings: Settings,
) -> None:
    await callback.answer()
    data = await state.get_data()
    index = int(data.get("question_index", 0))
    selected_index = int(callback.data.rsplit(":", 1)[1])

    if index >= len(QUESTIONS):
        await callback.message.answer("Викторина уже завершена. Можно пройти ещё раз.")
        return

    question = QUESTIONS[index]
    try:
        selected = question.options[selected_index]
    except IndexError:
        await callback.message.answer("Не понял вариант ответа. Попробуйте ещё раз.")
        return

    scores: dict[str, int] = data.get("scores") or empty_scores()
    scores = apply_answer(scores, selected)
    answers: list[dict[str, Any]] = data.get("answers") or []
    answers.append(
        {
            "question": question.text,
            "answer": selected.text,
            "weights": selected.weights,
        }
    )

    await state.update_data(scores=scores, answers=answers)
    try:
        await callback.message.edit_text(
            f"✅ Ответ принят: <i>{html.escape(selected.text)}</i>"
        )
    except Exception:
        logger.debug("Cannot edit question message", exc_info=True)

    next_index = index + 1
    if next_index < len(QUESTIONS):
        await _ask_question(callback.message, state, next_index)
        return

    await state.clear()
    animal = choose_animal(scores)
    await database.save_result(callback.from_user, animal.id, scores, answers)
    await send_result(callback.message, animal.id, scores, settings)


async def send_result(message: Message, animal_id: str, scores: dict[str, int], settings: Settings) -> None:
    animal = ANIMALS[animal_id]
    score_lines = ", ".join(
        f"{ANIMALS[item_id].short_title}: {score}" for item_id, score in top_scores(scores)
    )
    caption = (
        f"🧭 <b>Ваше тотемное животное в Московском зоопарке — {html.escape(animal.title)}!</b>\n\n"
        f"{html.escape(animal.description)}\n\n"
        f"<b>Почему это важно:</b> {html.escape(animal.adoption_pitch)}\n\n"
        f"Топ совпадений: {html.escape(score_lines)}\n"
        f"Страница животного: {animal.species_url}"
    )
    reply_markup = result_keyboard(settings, animal)

    photo_url = await resolve_photo_url(animal)
    if photo_url:
        try:
            await message.answer_photo(URLInputFile(photo_url), caption=caption, reply_markup=reply_markup)
            return
        except Exception:
            logger.exception("Cannot send photo for %s", animal.id)

    await message.answer(caption, reply_markup=reply_markup)
