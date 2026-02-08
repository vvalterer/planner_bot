"""
Тесты для базы данных и репозиториев.
"""

import pytest
from app.database.connection import init_db, close_db, get_connection
from app.database.repository import UserRepository, ContentPlanRepository


@pytest.fixture
async def db_connection():
    """Фикстура для инициализации тестовой БД."""
    import os
    os.environ["DB_PATH"] = ":memory:"
    
    # Сбрасываем глобальное соединение
    import app.database.connection as conn_module
    conn_module._connection = None
    
    await init_db()
    yield
    await close_db()


class TestUserRepository:
    """Тесты для UserRepository."""
    
    @pytest.mark.asyncio
    async def test_get_or_create_new_user(self, db_connection):
        """Тест создания нового пользователя."""
        user = await UserRepository.get_or_create(
            telegram_id=12345,
            username="testuser",
            first_name="Test"
        )
        
        assert user["telegram_id"] == 12345
        assert user["username"] == "testuser"
        assert user["first_name"] == "Test"
    
    @pytest.mark.asyncio
    async def test_get_or_create_existing_user(self, db_connection):
        """Тест получения существующего пользователя."""
        # Создаём пользователя
        user1 = await UserRepository.get_or_create(telegram_id=67890)
        
        # Получаем его снова
        user2 = await UserRepository.get_or_create(telegram_id=67890)
        
        assert user1["id"] == user2["id"]
    
    @pytest.mark.asyncio
    async def test_get_by_telegram_id(self, db_connection):
        """Тест поиска пользователя по telegram_id."""
        await UserRepository.get_or_create(telegram_id=11111, username="find_me")
        
        user = await UserRepository.get_by_telegram_id(11111)
        
        assert user is not None
        assert user["username"] == "find_me"
    
    @pytest.mark.asyncio
    async def test_get_by_telegram_id_not_found(self, db_connection):
        """Тест поиска несуществующего пользователя."""
        user = await UserRepository.get_by_telegram_id(99999)
        
        assert user is None


class TestContentPlanRepository:
    """Тесты для ContentPlanRepository."""
    
    @pytest.mark.asyncio
    async def test_create_plan(self, db_connection):
        """Тест создания контент-плана."""
        plan_id = await ContentPlanRepository.create(
            user_id=12345,
            niche="фитнес",
            target_audience="женщины",
            plan_content="План контента..."
        )
        
        assert plan_id is not None
        assert plan_id > 0
    
    @pytest.mark.asyncio
    async def test_get_by_user(self, db_connection):
        """Тест получения планов пользователя."""
        user_id = 54321
        
        await ContentPlanRepository.create(
            user_id=user_id,
            niche="кулинария",
            target_audience="мамы",
            plan_content="План 1"
        )
        await ContentPlanRepository.create(
            user_id=user_id,
            niche="спорт",
            target_audience="молодёжь",
            plan_content="План 2"
        )
        
        plans = await ContentPlanRepository.get_by_user(user_id)
        
        assert len(plans) == 2
    
    @pytest.mark.asyncio
    async def test_count_by_user(self, db_connection):
        """Тест подсчёта планов пользователя."""
        user_id = 77777
        
        await ContentPlanRepository.create(
            user_id=user_id,
            niche="тест",
            target_audience="тест",
            plan_content="тест"
        )
        
        count = await ContentPlanRepository.count_by_user(user_id)
        
        assert count == 1
