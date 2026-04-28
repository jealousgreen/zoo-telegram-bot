from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import aiosqlite
from aiogram.types import User


class Storage:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    async def init(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    result_animal TEXT NOT NULL,
                    scores_json TEXT NOT NULL,
                    answers_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL,
                    username TEXT,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            await db.commit()

    async def save_result(
        self,
        user: User,
        result_animal: str,
        scores: dict[str, int],
        answers: list[dict[str, Any]],
    ) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO quiz_results
                    (telegram_id, username, first_name, result_animal, scores_json, answers_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user.id,
                    user.username,
                    user.first_name,
                    result_animal,
                    json.dumps(scores, ensure_ascii=False),
                    json.dumps(answers, ensure_ascii=False),
                    datetime.now(UTC).isoformat(),
                ),
            )
            await db.commit()

    async def latest_result(self, telegram_id: int) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT * FROM quiz_results
                WHERE telegram_id = ?
                ORDER BY id DESC LIMIT 1
                """,
                (telegram_id,),
            )
            row = await cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    async def save_feedback(self, user: User, message: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO feedback (telegram_id, username, message, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (user.id, user.username, message, datetime.now(UTC).isoformat()),
            )
            await db.commit()
