"""
Тесты для системы подписок.
"""

import pytest
from datetime import datetime, timedelta

from app.services.subscription import SubscriptionService
from app.database.repository import UserRepository


class TestSubscriptionService:
    """Тесты сервиса подписок."""

    @pytest.mark.asyncio
    async def test_grant_access_new_user(self, temp_db):
        """Тест выдачи доступа новому пользователю."""
        user_id = 1001
        await UserRepository.get_or_create(user_id)

        # Выдаем доступ
        new_end = await SubscriptionService.grant_access(user_id, 30)

        assert new_end > datetime.now()

        # Проверяем доступ
        has_access = await SubscriptionService.check_access(user_id)
        assert has_access is True

    @pytest.mark.asyncio
    async def test_grant_access_extension(self, temp_db):
        """Тест продления доступа."""
        user_id = 1002
        await UserRepository.get_or_create(user_id)

        # Первая выдача
        end1 = await SubscriptionService.grant_access(user_id, 30)

        # Продление
        end2 = await SubscriptionService.grant_access(user_id, 30)

        # Разница должна быть около 60 дней от сейчас (или 30 от end1)
        diff = end2 - end1
        assert 29 <= diff.days <= 31

    @pytest.mark.asyncio
    async def test_access_denied_expired(self, temp_db):
        """Тест истекшей подписки."""
        user_id = 1003
        await UserRepository.get_or_create(user_id)

        # Ставим дату в прошлом
        past_date = datetime.now() - timedelta(days=1)
        await UserRepository.update_subscription(user_id, past_date)

        has_access = await SubscriptionService.check_access(user_id)
        assert has_access is False

    @pytest.mark.asyncio
    async def test_access_denied_no_sub(self, temp_db):
        """Тест отсутствия подписки."""
        user_id = 1004
        await UserRepository.get_or_create(user_id)

        has_access = await SubscriptionService.check_access(user_id)
        assert has_access is False
