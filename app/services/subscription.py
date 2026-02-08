"""
Сервис управления подписками.
Логика проверки и выдачи доступа.
"""

from datetime import datetime, timedelta
import logging

from app.database.repository import UserRepository

logger = logging.getLogger(__name__)


class SubscriptionService:
    """Сервис подписок."""

    @staticmethod
    async def check_access(user_id: int) -> bool:
        """
        Проверить, есть ли у пользователя активная подписка.

        Args:
            user_id: Telegram ID пользователя

        Returns:
            True, если подписка активна (или пользователь админ/тестировщик)
            False, если подписка истекла
        """
        user = await UserRepository.get_by_telegram_id(user_id)
        if not user:
            return False

        # Проверяем поле subscription_end_date
        sub_end = user.get("subscription_end_date")

        # Если подписки нет вообще
        if not sub_end:
            return False

        # Если это строка (из SQLite), преобразуем в datetime
        if isinstance(sub_end, str):
            try:
                # SQLite хранит TIMESTAMP как строку 'YYYY-MM-DD HH:MM:SS'
                sub_end = datetime.strptime(sub_end.split(".")[0], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                logger.error(f"Error parsing date: {sub_end}")
                return False

        # Проверяем срок
        if sub_end > datetime.now():
            return True

        return False

    @staticmethod
    async def grant_access(user_id: int, days: int = 30) -> datetime:
        """
        Выдать доступ пользователю на указанное количество дней.

        Args:
            user_id: Telegram ID пользователя
            days: Количество дней доступа

        Returns:
            Новая дата окончания подписки
        """
        user = await UserRepository.get_by_telegram_id(user_id)

        now = datetime.now()
        current_end = user.get("subscription_end_date") if user else None

        # Парсим текущую дату, если она есть
        if isinstance(current_end, str):
            try:
                current_end = datetime.strptime(current_end.split(".")[0], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                current_end = None

        # Если подписка активна, продлеваем её. Иначе начинаем с сейчас.
        if current_end and current_end > now:
            new_end = current_end + timedelta(days=days)
        else:
            new_end = now + timedelta(days=days)

        await UserRepository.update_subscription(user_id, new_end)
        logger.info(f"User {user_id} subscription updated until {new_end}")

        return new_end
