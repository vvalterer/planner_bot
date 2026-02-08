"""
Сервис генерации контент-плана.
Бизнес-логика создания недельного плана контента.
"""

import re
from typing import Tuple
from datetime import datetime, timedelta

# Шаблоны контента по типам постов
CONTENT_TEMPLATES = {
    "educational": [
        "📚 Образовательный пост: «{topic}» — объясни основы для новичков",
        "💡 Лайфхак дня: как сэкономить время/деньги в {niche}",
        "❓ FAQ: ответы на 5 частых вопросов о {topic}",
    ],
    "engaging": [
        "🗳️ Опрос: «Какой {topic} вам ближе?» — вовлекаем аудиторию",
        "💬 Вопрос дня: «Поделись своим опытом в {niche}»",
        "🎯 Челлендж: 7 дней {topic} — присоединяйтесь!",
    ],
    "storytelling": [
        "📖 История успеха: как клиент достиг результата в {niche}",
        "🎭 За кулисами: один день из жизни {niche}-эксперта",
        "🔥 Ошибки новичков: 5 провалов в {topic} и как их избежать",
    ],
    "promotional": [
        "🎁 Специальное предложение для {target_audience}",
        "⭐ Отзыв клиента: результаты работы в {niche}",
        "🚀 Новинка: представляем новый продукт/услугу",
    ],
    "entertainment": [
        "😄 Мемы и юмор: смешное из мира {niche}",
        "🎬 Рекомендации: топ-5 ресурсов по {topic}",
        "🏆 Подборка недели: лучшее в {niche}",
    ],
}

WEEKDAYS_RU = [
    "Понедельник", "Вторник", "Среда", "Четверг",
    "Пятница", "Суббота", "Воскресенье"
]


def parse_user_input(text: str) -> Tuple[str, str]:
    """
    Парсит ввод пользователя для извлечения ниши и ЦА.

    Args:
        text: Текст от пользователя

    Returns:
        Tuple[niche, target_audience]
    """
    niche = ""
    target_audience = ""

    # Пробуем найти паттерны "ниша: X" и "ЦА: Y"
    niche_match = re.search(r'ниша[:\s]+([^,]+)', text, re.IGNORECASE)
    ta_match = re.search(r'ЦА[:\s]+(.+)', text, re.IGNORECASE)

    if niche_match:
        niche = niche_match.group(1).strip()
    if ta_match:
        target_audience = ta_match.group(1).strip()

    # Если паттерны не найдены, используем весь текст как нишу
    if not niche:
        niche = text.strip()

    if not target_audience:
        target_audience = "широкая аудитория"

    return niche, target_audience


def generate_day_content(
    day_num: int,
    niche: str,
    target_audience: str
) -> str:
    """Генерирует контент для одного дня."""
    import random

    # Чередуем типы контента по дням
    content_types = list(CONTENT_TEMPLATES.keys())
    content_type = content_types[day_num % len(content_types)]

    templates = CONTENT_TEMPLATES[content_type]
    template = random.choice(templates)

    # Подставляем переменные
    content = template.format(
        niche=niche,
        topic=niche,
        target_audience=target_audience
    )

    return content


def generate_content_plan(user_input: str) -> str:
    """
    Генерирует недельный контент-план.

    Args:
        user_input: Текст запроса пользователя

    Returns:
        Отформатированный контент-план на 7 дней
    """
    niche, target_audience = parse_user_input(user_input)

    # Начинаем с завтрашнего дня
    start_date = datetime.now() + timedelta(days=1)

    lines = [
        "📋 <b>Контент-план на 7 дней</b>",
        f"🎯 Ниша: <b>{niche}</b>",
        f"👥 ЦА: <b>{target_audience}</b>",
        "",
        "─" * 25,
        ""
    ]

    for i in range(7):
        day_date = start_date + timedelta(days=i)
        weekday = WEEKDAYS_RU[day_date.weekday()]
        date_str = day_date.strftime("%d.%m")

        content = generate_day_content(i, niche, target_audience)

        lines.append(f"<b>День {i+1}</b> • {weekday}, {date_str}")
        lines.append(content)
        lines.append("")

    lines.extend([
        "─" * 25,
        "",
        "💡 <i>Совет: адаптируйте план под свой стиль и актуальные события!</i>",
        "",
        "🔄 Хотите новый план? Просто напишите нишу и ЦА снова."
    ])

    return "\n".join(lines)
