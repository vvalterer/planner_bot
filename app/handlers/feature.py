"""
Обработчики команд бота.
"""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.handlers.help_text import get_help
from app.services.planner import generate_content_plan
from app.keyboards.main import get_main_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обработчик команды /start."""
    await message.answer(
        "👋 Привет! Я <b>AI Content Planner</b> под брендом Вячеслав Ветошкин.\n\n"
        "📝 Напиши свою нишу и целевую аудиторию, и я создам для тебя "
        "недельный контент-план!\n\n"
        "Пример: <code>ниша: фитнес, ЦА: женщины 25-35</code>\n\n"
        "Используй /help для справки.",
        reply_markup=get_main_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Обработчик команды /help."""
    await message.answer(get_help())


@router.message()
async def handle_plan_request(message: Message) -> None:
    """Обработка запроса на генерацию контент-плана."""
    if not message.text:
        return
    
    user_input = message.text.strip()
    
    if len(user_input) < 5:
        await message.answer(
            "⚠️ Слишком короткий запрос. Опиши свою нишу и целевую аудиторию подробнее.\n\n"
            "Пример: <code>ниша: кулинария, ЦА: молодые мамы</code>"
        )
        return
    
    await message.answer("⏳ Генерирую контент-план...")
    
    plan = generate_content_plan(user_input)
    await message.answer(plan)
