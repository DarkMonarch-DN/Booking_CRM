#!/bin/sh
set -e
# 1. Ждем секунду, чтобы Postgres точно успел инициализироваться и начать принимать подключения
echo "Waiting for database..."
sleep 2 

# 2. Запускаем миграции Alembic
echo "Running alembic migrations..."
alembic upgrade head

# 3. Запускаем наше FastAPI приложение (команда, которая раньше была в Dockerfile)
echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
