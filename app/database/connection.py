"""
Управление подключением к базе данных.
Использует aiosqlite для асинхронной работы с SQLite.
"""

import aiosqlite
import logging
import os
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

_connection: Optional[aiosqlite.Connection] = None


async def get_connection() -> aiosqlite.Connection:
    """Получить текущее подключение к БД."""
    global _connection
    if _connection is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _connection


async def init_db() -> None:
    """Инициализация базы данных."""
    global _connection
    
    # Создаём директорию для БД если не существует
    db_dir = os.path.dirname(settings.db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        logger.info(f"Created database directory: {db_dir}")
    
    _connection = await aiosqlite.connect(settings.db_path)
    _connection.row_factory = aiosqlite.Row
    
    # Создание таблиц
    await _connection.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            subscription_end_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS content_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            niche TEXT NOT NULL,
            target_audience TEXT,
            plan_content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(telegram_id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
        CREATE INDEX IF NOT EXISTS idx_plans_user_id ON content_plans(user_id);
    """)
    await _connection.commit()
    logger.info(f"Database initialized: {settings.db_path}")


async def close_db() -> None:
    """Закрытие подключения к БД."""
    global _connection
    if _connection:
        await _connection.close()
        _connection = None
        logger.info("Database connection closed")
