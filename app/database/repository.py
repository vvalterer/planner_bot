"""
Repository для работы с данными.
Паттерн Repository для абстрагирования доступа к данным.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime

from app.database.connection import get_connection


class UserRepository:
    """Репозиторий для работы с пользователями."""

    @staticmethod
    async def get_or_create(
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Получить или создать пользователя."""
        conn = await get_connection()

        cursor = await conn.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        row = await cursor.fetchone()

        if row:
            return dict(row)

        await conn.execute(
            "INSERT INTO users (telegram_id, username, first_name) VALUES (?, ?, ?)",
            (telegram_id, username, first_name)
        )
        await conn.commit()

        cursor = await conn.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        row = await cursor.fetchone()
        return dict(row)

    @staticmethod
    async def get_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получить пользователя по Telegram ID."""
        conn = await get_connection()
        cursor = await conn.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    @staticmethod
    async def count_all() -> int:
        """Получить общее количество пользователей."""
        conn = await get_connection()
        cursor = await conn.execute("SELECT COUNT(*) as cnt FROM users")
        row = await cursor.fetchone()
        return row["cnt"] if row else 0

    @staticmethod
    async def get_all_ids() -> List[int]:
        """Получить ID всех пользователей (для рассылки)."""
        conn = await get_connection()
        cursor = await conn.execute("SELECT telegram_id FROM users")
        rows = await cursor.fetchall()
        return [row["telegram_id"] for row in rows]

    @staticmethod
    async def update_subscription(user_id: int, end_date: datetime) -> None:
        """Обновить дату окончания подписки."""
        conn = await get_connection()
        await conn.execute(
            "UPDATE users SET subscription_end_date = ? WHERE telegram_id = ?",
            (end_date, user_id)
        )
        await conn.commit()


class ContentPlanRepository:
    """Репозиторий для работы с контент-планами."""

    @staticmethod
    async def create(
        user_id: int,
        niche: str,
        target_audience: str,
        plan_content: str
    ) -> int:
        """Создать новый контент-план."""
        conn = await get_connection()
        cursor = await conn.execute(
            """INSERT INTO content_plans
               (user_id, niche, target_audience, plan_content)
               VALUES (?, ?, ?, ?)""",
            (user_id, niche, target_audience, plan_content)
        )
        await conn.commit()
        return cursor.lastrowid

    @staticmethod
    async def get_by_user(user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Получить контент-планы пользователя."""
        conn = await get_connection()
        cursor = await conn.execute(
            """SELECT * FROM content_plans
               WHERE user_id = ?
               ORDER BY created_at DESC
               LIMIT ?""",
            (user_id, limit)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    async def count_by_user(user_id: int) -> int:
        """Подсчитать количество планов пользователя."""
        conn = await get_connection()
        cursor = await conn.execute(
            "SELECT COUNT(*) as cnt FROM content_plans WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return row["cnt"] if row else 0

    @staticmethod
    async def count_all() -> int:
        """Получить общее количество созданных планов."""
        conn = await get_connection()
        cursor = await conn.execute("SELECT COUNT(*) as cnt FROM content_plans")
        row = await cursor.fetchone()
        return row["cnt"] if row else 0
