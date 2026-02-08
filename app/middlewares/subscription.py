"""
Middleware для проверки подписки.
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from app.services.subscription import SubscriptionService
from app.config import settings


class SubscriptionMiddleware(BaseMiddleware):
    """
    Проверяет наличие активной подписки у пользователя.
    Блокирует доступ к функционалу, если подписки нет.
    """
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Пропускаем команды /start, /help, /buy, /admin для всех
        if event.text and event.text.startswith(("/start", "/help", "/buy", "/admin")):
            return await handler(event, data)
            
        user = event.from_user
        if not user:
            return await handler(event, data)
            
        # Админы всегда имеют доступ
        if settings.is_admin(user.id):
            return await handler(event, data)
            
        # Проверка подписки
        has_access = await SubscriptionService.check_access(user.id)
        
        if has_access:
            return await handler(event, data)
        else:
            await event.answer(
                "⛔ <b>Доступ закрыт</b>\n\n"
                "Ваша подписка истекла или не была активирована.\n"
                "Оформите доступ, чтобы продолжить пользоваться ботом.\n\n"
                "👉 Нажмите /buy для оформления."
            )
            return None
