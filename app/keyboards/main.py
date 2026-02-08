"""
Клавиатуры бота.
Reply и Inline клавиатуры для взаимодействия с пользователем.
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура бота."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Создать план")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О боте")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Напишите нишу и ЦА..."
    )
    return keyboard


def get_inline_examples() -> InlineKeyboardMarkup:
    """Inline клавиатура с примерами ниш."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏋️ Фитнес", callback_data="niche:fitness"),
                InlineKeyboardButton(text="💻 IT", callback_data="niche:it")
            ],
            [
                InlineKeyboardButton(text="🍳 Кулинария", callback_data="niche:cooking"),
                InlineKeyboardButton(text="📚 Образование", callback_data="niche:education")
            ]
        ]
    )
    return keyboard


def get_feedback_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для обратной связи."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👍 Полезно", callback_data="feedback:useful"),
                InlineKeyboardButton(text="👎 Не полезно", callback_data="feedback:not_useful")
            ],
            [
                InlineKeyboardButton(text="🔄 Новый план", callback_data="new_plan")
            ]
        ]
    )
    return keyboard
