"""
Тесты для модуля конфигурации.
"""

import pytest
import os


class TestSettings:
    """Тесты для класса Settings."""
    
    def test_settings_loads_bot_token(self):
        """Тест загрузки BOT_TOKEN."""
        from app.config import settings
        
        assert settings.bot_token == "test_token_12345"
    
    def test_settings_loads_admin_ids(self):
        """Тест загрузки ADMIN_IDS."""
        from app.config import settings
        
        assert 123456789 in settings.admin_ids
    
    def test_is_admin_true(self):
        """Тест проверки администратора - положительный."""
        from app.config import settings
        
        assert settings.is_admin(123456789) is True
    
    def test_is_admin_false(self):
        """Тест проверки администратора - отрицательный."""
        from app.config import settings
        
        assert settings.is_admin(999999999) is False
    
    def test_default_log_level(self):
        """Тест значения по умолчанию для LOG_LEVEL."""
        from app.config import settings
        
        assert settings.log_level == "DEBUG"
