"""
Административные функции бота.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from app.config import settings
from app.database.repository import UserRepository, ContentPlanRepository

router = Router(name=__name__)


@router.message(Command("admin"))
async def cmd_admin_stats(message: Message) -> None:
    """Показать статистику бота (только для админов)."""
    if not settings.is_admin(message.from_user.id):
        return

    users_count = await UserRepository.count_all()
    plans_count = await ContentPlanRepository.count_all()
    
    texto = (
        f"📊 <b>Статистика бота</b>\n\n"
        f"👥 Пользователей: <b>{users_count}</b>\n"
        f"📝 Создано планов: <b>{plans_count}</b>"
    )
    await message.answer(texto)


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message) -> None:
    """Рассылка сообщения всем пользователям (только для админов)."""
    if not settings.is_admin(message.from_user.id):
        return
        
    # Получаем текст рассылки из аргументов команды
    # Пример: /broadcast Привет всем!
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("⚠️ Использование: <code>/broadcast Текст сообщения</code>")
        return
        
    text_to_send = parts[1]
    user_ids = await UserRepository.get_all_ids()
    
    sent_count = 0
    errors_count = 0
    
    await message.answer(f"⏳ Начинаю рассылку на {len(user_ids)} пользователей...")
    
    for user_id in user_ids:
        try:
            await message.bot.send_message(chat_id=user_id, text=text_to_send)
            sent_count += 1
        except Exception:
            errors_count += 1
            
    await message.answer(
        f"✅ Рассылка завершена!\n\n"
        f"Отправлено: {sent_count}\n"
        f"Ошибок: {errors_count}"
    )
