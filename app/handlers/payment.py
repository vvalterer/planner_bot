"""
Обработчики оплаты и подписки.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.services.subscription import SubscriptionService

router = Router(name=__name__)


@router.message(Command("buy"))
async def cmd_buy(message: Message) -> None:
    """Команда /buy - оформление подписки."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Оплатить 990₽ (Тест)",
                    callback_data="pay:test_success"
                )
            ]
        ]
    )

    await message.answer(
        "💎 <b>Оформление подписки</b>\n\n"
        "Получите доступ к генератору контент-планов на 30 дней.\n"
        "Стоимость: <b>990₽</b>\n\n"
        "<i>(В тестовом режиме оплата не списывается)</i>",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "pay:test_success")
async def process_test_payment(callback: CallbackQuery) -> None:
    """Обработка тестовой успешной оплаты."""
    await callback.answer("Обработка платежа...")

    user_id = callback.from_user.id

    # Выдаем доступ на 30 дней
    new_end_date = await SubscriptionService.grant_access(user_id, 30)
    date_str = new_end_date.strftime("%d.%m.%Y")

    await callback.message.edit_text(
        f"✅ <b>Оплата прошла успешно!</b>\n\n"
        f"Подписка активирована до: <b>{date_str}</b>\n\n"
        f"Теперь вы можете генерировать контент-планы.\n"
        f"Напишите нишу и ЦА 👇"
    )
