from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def _int_or_none(value: str | None) -> int | None:
    if value is None or value.strip() == "":
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError("ADMIN_CHAT_ID должен быть числом") from exc


@dataclass(frozen=True)
class Settings:
    bot_token: str
    bot_username: str
    admin_chat_id: int | None
    database_path: Path
    guardianship_url: str = "https://moscowzoo.ru/about/guardianship"
    animals_catalog_url: str = "https://moscowzoo.ru/animals/kinds"
    privacy_url: str | None = None
    zoo_contact_email: str = "zoopark@culture.mos.ru"
    zoo_contact_phone: str = "+7 499 252-29-51"

    @property
    def bot_link(self) -> str:
        if self.bot_username:
            return f"https://t.me/{self.bot_username.lstrip('@')}"
        return "https://t.me/"


def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "Не найден BOT_TOKEN. Создайте .env по примеру .env и вставьте токен BotFather."
        )

    db_value = os.getenv("DATABASE_PATH", "data/zoo_bot.sqlite3")
    db_path = Path(db_value)
    if not db_path.is_absolute():
        db_path = BASE_DIR / db_path

    return Settings(
        bot_token=token,
        bot_username=os.getenv("BOT_USERNAME", "").strip(),
        admin_chat_id=_int_or_none(os.getenv("ADMIN_CHAT_ID")),
        database_path=db_path,
        privacy_url=os.getenv("PRIVACY_URL") or None,
        zoo_contact_email=os.getenv("ZOO_CONTACT_EMAIL", "zoopark@culture.mos.ru"),
        zoo_contact_phone=os.getenv("ZOO_CONTACT_PHONE", "+7 499 252-29-51"),
    )
