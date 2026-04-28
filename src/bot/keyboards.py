from __future__ import annotations

from urllib.parse import quote_plus

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import Settings
from bot.data.models import Animal, Question


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🐾 Начать викторину", callback_data="quiz:start")],
            [InlineKeyboardButton(text="🦉 Как работает опека", callback_data="info:guardianship")],
            [InlineKeyboardButton(text="❓ Справка", callback_data="info:help")],
        ]
    )


def question_keyboard(question: Question) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=option.text, callback_data=f"quiz:answer:{index}")]
            for index, option in enumerate(question.options)
        ]
    )


def result_keyboard(settings: Settings, animal: Animal) -> InlineKeyboardMarkup:
    bot_link = settings.bot_link
    share_text = (
        f"Моё тотемное животное в Московском зоопарке — {animal.short_title}! "
        f"Пройди викторину: {bot_link}"
    )
    telegram_share = f"https://t.me/share/url?url={quote_plus(bot_link)}&text={quote_plus(share_text)}"
    vk_share = (
        "https://vk.com/share.php?"
        f"url={quote_plus(bot_link)}&title={quote_plus('Какое у вас тотемное животное?')}&comment={quote_plus(share_text)}"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🪽 Узнать про опеку", callback_data="info:guardianship")],
            [InlineKeyboardButton(text="💬 Связаться с сотрудником", callback_data="contact:request")],
            [
                InlineKeyboardButton(text="📣 Поделиться в Telegram", url=telegram_share),
                InlineKeyboardButton(text="VK", url=vk_share),
            ],
            [InlineKeyboardButton(text="🔁 Попробовать ещё раз", callback_data="quiz:start")],
            [InlineKeyboardButton(text="📝 Оставить отзыв", callback_data="feedback:start")],
        ]
    )


def back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ В меню", callback_data="menu:main")]]
    )
