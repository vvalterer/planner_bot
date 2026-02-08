"""
Pytest fixtures для тестирования бота.
"""

import pytest
import asyncio
import os
from unittest.mock import AsyncMock, MagicMock

# Устанавливаем тестовые переменные окружения до импорта модулей
os.environ["BOT_TOKEN"] = "test_token_12345"
os.environ["ADMIN_IDS"] = "123456789"
os.environ["DB_PATH"] = ":memory:"
os.environ["LOG_LEVEL"] = "DEBUG"


@pytest.fixture(scope="session")
def event_loop():
    """Создаёт event loop для всей сессии тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_message():
    """Мок объекта Message от aiogram."""
    message = MagicMock()
    message.text = "ниша: фитнес, ЦА: женщины 25-35"
    message.from_user = MagicMock()
    message.from_user.id = 123456789
    message.from_user.username = "testuser"
    message.from_user.first_name = "Test"
    message.answer = AsyncMock()
    return message


@pytest.fixture
def mock_message_short():
    """Мок сообщения с коротким текстом."""
    message = MagicMock()
    message.text = "hi"
    message.from_user = MagicMock()
    message.from_user.id = 123456789
    message.answer = AsyncMock()
    return message


@pytest.fixture
async def temp_db():
    """Временная база данных для тестов."""
    from app.database.connection import init_db, close_db

    # Используем in-memory базу
    original_path = os.environ.get("DB_PATH")
    os.environ["DB_PATH"] = ":memory:"

    await init_db()
    yield
    await close_db()

    if original_path:
        os.environ["DB_PATH"] = original_path
