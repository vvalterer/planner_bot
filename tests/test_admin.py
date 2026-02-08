"""
Тесты для админ-панели.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.handlers.admin import cmd_admin_stats, cmd_broadcast
from app.config import settings


@pytest.fixture
def mock_admin_message():
    """Мок сообщения от админа."""
    message = MagicMock()
    message.from_user.id = 123456789  # ID из conftest/env
    message.answer = AsyncMock()
    message.bot.send_message = AsyncMock()
    return message


@pytest.fixture
def mock_user_message():
    """Мок сообщения от обычного пользователя."""
    message = MagicMock()
    message.from_user.id = 999999999
    message.answer = AsyncMock()
    return message


class TestAdminHandlers:
    """Тесты обработчиков админ-панели."""

    @pytest.mark.asyncio
    async def test_admin_stats_access_granted(self, mock_admin_message, temp_db):
        """Тест доступа к статистике для админа."""
        # Настраиваем фикстуру
        settings.admin_ids = [123456789]

        await cmd_admin_stats(mock_admin_message)

        # Проверяем, что ответ был отправлен
        mock_admin_message.answer.assert_called_once()
        args = mock_admin_message.answer.call_args[0][0]
        assert "Статистика бота" in args

    @pytest.mark.asyncio
    async def test_admin_stats_access_denied(self, mock_user_message):
        """Тест отказа в доступе к статистике."""
        settings.admin_ids = [123456789]

        await cmd_admin_stats(mock_user_message)

        # Проверяем, что ответ НЕ был отправлен
        mock_user_message.answer.assert_not_called()

    @pytest.mark.asyncio
    async def test_broadcast_success(self, mock_admin_message, temp_db):
        """Тест успешной рассылки."""
        settings.admin_ids = [123456789]
        mock_admin_message.text = "/broadcast Тестовое сообщение"

        # Добавляем пользователей в БД для рассылки
        from app.database.repository import UserRepository
        await UserRepository.get_or_create(111, "user1")
        await UserRepository.get_or_create(222, "user2")

        await cmd_broadcast(mock_admin_message)

        # Проверяем отправку
        assert mock_admin_message.bot.send_message.call_count == 2
        mock_admin_message.answer.assert_called()  # Отчет админу

    @pytest.mark.asyncio
    async def test_broadcast_no_text(self, mock_admin_message):
        """Тест рассылки без текста."""
        settings.admin_ids = [123456789]
        mock_admin_message.text = "/broadcast"

        await cmd_broadcast(mock_admin_message)

        # Проверяем сообщение об ошибке
        mock_admin_message.answer.assert_called_with("⚠️ Использование: <code>/broadcast Текст сообщения</code>")
        mock_admin_message.bot.send_message.assert_not_called()
