"""
Тесты для сервиса генерации контент-плана.
"""


from app.services.planner import (
    parse_user_input,
    generate_content_plan,
    generate_day_content
)


class TestParseUserInput:
    """Тесты для функции parse_user_input."""

    def test_parse_full_input(self):
        """Тест парсинга полного ввода с нишей и ЦА."""
        text = "ниша: фитнес, ЦА: женщины 25-35"
        niche, ta = parse_user_input(text)

        assert niche == "фитнес"
        assert ta == "женщины 25-35"

    def test_parse_niche_only(self):
        """Тест парсинга только ниши."""
        text = "ниша: программирование"
        niche, ta = parse_user_input(text)

        assert niche == "программирование"
        assert ta == "широкая аудитория"

    def test_parse_plain_text(self):
        """Тест парсинга простого текста без паттернов."""
        text = "кулинария для мам"
        niche, ta = parse_user_input(text)

        assert niche == "кулинария для мам"
        assert ta == "широкая аудитория"

    def test_parse_with_colon_space(self):
        """Тест парсинга с разными вариантами разделителей."""
        text = "ниша кулинария, ЦА молодёжь"
        niche, ta = parse_user_input(text)

        assert niche == "кулинария"
        assert ta == "молодёжь"


class TestGenerateContentPlan:
    """Тесты для функции generate_content_plan."""

    def test_plan_contains_7_days(self):
        """Тест что план содержит 7 дней."""
        plan = generate_content_plan("ниша: тест")

        for i in range(1, 8):
            assert f"День {i}" in plan

    def test_plan_contains_niche(self):
        """Тест что план содержит указанную нишу."""
        plan = generate_content_plan("ниша: фитнес, ЦА: спортсмены")

        assert "фитнес" in plan
        assert "спортсмены" in plan

    def test_plan_has_header(self):
        """Тест что план имеет заголовок."""
        plan = generate_content_plan("ниша: тест")

        assert "Контент-план на 7 дней" in plan

    def test_plan_has_tips(self):
        """Тест что план содержит советы."""
        plan = generate_content_plan("ниша: тест")

        assert "Совет" in plan


class TestGenerateDayContent:
    """Тесты для функции generate_day_content."""

    def test_returns_string(self):
        """Тест что функция возвращает строку."""
        content = generate_day_content(0, "тест", "аудитория")

        assert isinstance(content, str)
        assert len(content) > 0

    def test_different_days_can_have_different_types(self):
        """Тест что разные дни могут иметь разный контент."""
        contents = [generate_day_content(i, "тест", "аудитория") for i in range(7)]

        # Должны быть хоть какие-то различия
        assert len(set(contents)) > 1
