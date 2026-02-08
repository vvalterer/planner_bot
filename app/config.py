"""
Централизованная конфигурация приложения.
Загружает настройки из переменных окружения.
"""

import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """Настройки приложения."""
    
    bot_token: str = os.getenv("BOT_TOKEN", "")
    admin_ids: List[int] = None
    db_path: str = os.getenv("DB_PATH", "data/database.sqlite3")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __post_init__(self):
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if admin_ids_str:
            self.admin_ids = [int(x.strip()) for x in admin_ids_str.split(",") if x.strip()]
        else:
            self.admin_ids = []
    
    def is_admin(self, user_id: int) -> bool:
        """Проверка, является ли пользователь администратором."""
        return user_id in self.admin_ids


settings = Settings()
