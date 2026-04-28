from __future__ import annotations

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import Settings
from bot.keyboards import back_to_menu, main_menu

router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Привет! Я бот-викторина Московского зоопарка. "
        "За 8 вопросов подберу вам тотемное животное и расскажу, как можно поддержать программу опеки.\n\n"
        "Готовы узнать, кто вы сегодня: манул, сивуч, пингвин или кто-то совсем неожиданный?",
        reply_markup=main_menu(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Как пользоваться ботом:\n"
        "1. Нажмите «Начать викторину».\n"
        "2. Выберите по одному варианту в каждом вопросе.\n"
        "3. Получите животное, фото, описание и кнопки для опеки, связи и репоста.\n\n"
        "Команды: /start — меню, /help — справка, /privacy — конфиденциальность.",
        reply_markup=main_menu(),
    )


@router.message(Command("privacy"))
async def cmd_privacy(message: Message, settings: Settings) -> None:
    text = (
        "Конфиденциальность: бот хранит только минимальные данные, нужные для работы викторины: "
        "ваш Telegram ID, выбранные ответы, итоговое животное и текст отзыва, если вы его оставляете. "
        "Токен бота и служебные контакты хранятся в переменных окружения, не в коде."
    )
    if settings.privacy_url:
        text += f"\n\nПолная политика: {settings.privacy_url}"
    await message.answer(text, reply_markup=main_menu())


@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer()
    await callback.message.edit_text("Главное меню. Что делаем?", reply_markup=main_menu())


@router.callback_query(F.data == "info:help")
async def cb_help(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(
        "Викторина состоит из 8 коротких вопросов. За каждый ответ начисляются баллы нескольким животным. "
        "В финале побеждает животное с самым высоким счетом.\n\n"
        "Потом можно поделиться результатом, узнать про опеку, связаться с сотрудником или пройти заново.",
        reply_markup=back_to_menu(),
    )


@router.callback_query(F.data == "info:guardianship")
async def cb_guardianship(callback: CallbackQuery, settings: Settings) -> None:
    await callback.answer()
    await callback.message.answer(
        "🪽 <b>Что такое опека?</b>\n\n"
        "Опекун помогает любимому животному: поддерживает его содержание, кормление, ветеринарный уход "
        "и работу специалистов. Это не про «забрать домой», а про регулярную помощь зоопарку и участие "
        "в сохранении животных.\n\n"
        f"Подробнее: {settings.guardianship_url}\n"
        f"Контакты для демонстрации: {settings.zoo_contact_email}, {settings.zoo_contact_phone}",
        reply_markup=back_to_menu(),
    )
