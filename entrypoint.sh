#!/bin/bash
set -e

# Здесь можно добавить миграции, если появятся (например, alembic)
# python -m alembic upgrade head

# Запуск бота
exec python app/main.py
