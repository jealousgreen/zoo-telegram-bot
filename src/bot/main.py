from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import BASE_DIR, load_settings
from bot.handlers import common, contact_feedback, quiz
from bot.services.storage import Storage

LOG_DIR = BASE_DIR / "logs"


def setup_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_DIR / "bot.log", encoding="utf-8"),
        ],
    )


async def main() -> None:
    setup_logging()
    settings = load_settings()
    storage = Storage(settings.database_path)
    await storage.init()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp["settings"] = settings
    dp["database"] = storage

    dp.include_router(common.router)
    dp.include_router(quiz.router)
    dp.include_router(contact_feedback.router)

    logging.getLogger(__name__).info("Bot is starting")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
