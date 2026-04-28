from __future__ import annotations

import html

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import Settings
from bot.data.quiz import ANIMALS
from bot.handlers.quiz import QuizState
from bot.keyboards import back_to_menu, main_menu
from bot.services.storage import Storage

router = Router(name="contact_feedback")


@router.callback_query(F.data == "contact:request")
async def request_contact(
    callback: CallbackQuery,
    bot: Bot,
    database: Storage,
    settings: Settings,
) -> None:
    await callback.answer()
    latest = await database.latest_result(callback.from_user.id)
    if latest is None:
        await callback.message.answer(
            "Сначала пройдите викторину, чтобы сотрудник увидел ваш результат.",
            reply_markup=main_menu(),
        )
        return

    animal = ANIMALS.get(latest["result_animal"])
    animal_text = animal.title if animal else latest["result_animal"]
    user = callback.from_user
    public_name = user.full_name or "без имени"
    username = f"@{user.username}" if user.username else "username не указан"

    admin_text = (
        "📩 <b>Новая заявка по программе опеки</b>\n\n"
        f"Пользователь: {html.escape(public_name)} ({html.escape(username)})\n"
        f"Telegram ID: <code>{user.id}</code>\n"
        f"Результат викторины: <b>{html.escape(animal_text)}</b>\n\n"
        "Ответьте пользователю в Telegram, если это демонстрационный аккаунт сотрудника."
    )

    if settings.admin_chat_id:
        await bot.send_message(settings.admin_chat_id, admin_text)
        await callback.message.answer(
            "Готово! Я передал сотруднику ваш результат викторины. "
            "Так ему будет проще подсказать, как оформить опеку или выбрать животное.",
            reply_markup=back_to_menu(),
        )
    else:
        await callback.message.answer(
            "В демо-режиме ADMIN_CHAT_ID не задан, поэтому заявку некому переслать.\n\n"
            f"Ваш результат: {html.escape(animal_text)}\n"
            f"Можно написать на {settings.zoo_contact_email} или позвонить {settings.zoo_contact_phone}.\n\n"
            "Чтобы включить пересылку сотруднику, укажите ADMIN_CHAT_ID в .env.",
            reply_markup=back_to_menu(),
        )


@router.callback_query(F.data == "feedback:start")
async def feedback_start(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(QuizState.waiting_feedback)
    await callback.message.answer(
        "Напишите отзыв одним сообщением: что понравилось, что улучшить, какого животного не хватило?"
    )


@router.message(QuizState.waiting_feedback)
async def feedback_message(
    message: Message,
    state: FSMContext,
    database: Storage,
    bot: Bot,
    settings: Settings,
) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer("Пожалуйста, отправьте отзыв текстом.")
        return

    await database.save_feedback(message.from_user, text)
    await state.clear()

    if settings.admin_chat_id:
        await bot.send_message(
            settings.admin_chat_id,
            "📝 <b>Новый отзыв о боте</b>\n\n"
            f"От: {html.escape(message.from_user.full_name)} "
            f"(@{message.from_user.username or 'без username'}, ID {message.from_user.id})\n"
            f"Текст: {html.escape(text)}",
        )

    await message.answer("Спасибо! Отзыв сохранён и поможет улучшить викторину 🐾", reply_markup=main_menu())
