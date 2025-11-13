#!/bin/bash

# Скрипт для инициализации базы данных

echo "Применение миграций..."
python manage.py migrate

echo "Сборка статики..."
python manage.py collectstatic --noinput

echo "Загрузка ингредиентов..."
python manage.py load_ingredients

echo "Загрузка тегов..."
python manage.py load_tags

echo "База данных инициализирована!"

