# Foodgram - продуктовый помощник

Foodgram - это веб-приложение для публикации рецептов, подписки на авторов и создания списков покупок.

## Технологии

- Python 3.11
- Django 5.2
- Django REST Framework 3.16
- PostgreSQL 16
- Docker & Docker Compose
- Nginx
- Gunicorn
- Djoser (authentication)

## Функциональность

- Регистрация и аутентификация пользователей
- Публикация рецептов с фото
- Добавление рецептов в избранное
- Подписка на авторов
- Создание списка покупок
- Скачивание списка покупок
- Фильтрация рецептов по тегам
- Короткие ссылки на рецепты

## Установка и запуск

### Локальный запуск для разработки

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd foodgram
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Создайте файл `.env` в корне проекта по образцу `.env.example`

4. Примените миграции:
```bash
python manage.py migrate
```

5. Загрузите ингредиенты:
```bash
python manage.py load_ingredients
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустите сервер:
```bash
python manage.py runserver
```

### Запуск в Docker

#### Локальная разработка (порт 8080)

1. Создайте файл `.env` в корне проекта

2. Соберите и запустите контейнеры:
```bash
docker-compose up -d
```

3. Загрузите данные:
```bash
docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py load_tags
```

4. Создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

Проект будет доступен по адресу: http://localhost:8080

#### Продакшен (порт 80)

Для развертывания на удаленном сервере используйте `docker-compose.production.yml`:

```bash
docker-compose -f docker-compose.production.yml up -d
```

Подробная инструкция по развертыванию: [DEPLOYMENT.md](DEPLOYMENT.md)

## API Documentation

API документация доступна по адресу: `/api/docs/`

## Автор

Проект разработан в рамках обучения в Яндекс.Практикум

## Домен

Проект доступен по адресу: https://efoodgram.webhop.me
IP: 51.250.29.55
