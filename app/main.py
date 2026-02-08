"""
AI Content Planner Bot — Main Entry Point
Бот для генерации недельного контент-плана под нишу и ЦА

Автор: Вячеслав Ветошкин
Сайт: https://1vetoshkin.ru
Telegram: https://t.me/TkAs007bot
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.handlers import feature
from app.database.connection import init_db, close_db


logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """Действия при запуске бота."""
    await init_db()
    logger.info("Bot started successfully")


async def on_shutdown(bot: Bot) -> None:
    """Действия при остановке бота."""
    await close_db()
    logger.info("Bot stopped")


async def main() -> None:
    """Главная функция запуска бота."""
    if not settings.bot_token:
        logger.error("BOT_TOKEN is not set!")
        sys.exit(1)
    
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Регистрация startup/shutdown
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    from app.handlers import feature, admin, payment
    from app.middlewares.subscription import SubscriptionMiddleware
    
    # Регистрация middleware
    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())
    
    # Подключение роутеров
    dp.include_router(admin.router)  # Admin router first
    dp.include_router(payment.router) # Payment router second
    dp.include_router(feature.router)
    
    logger.info("Starting bot polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
