import json
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда для загрузки ингредиентов из JSON файла."""

    help = "Загрузка ингредиентов из JSON файла"

    def handle(self, *args, **options):
        """Обработка команды."""
        # Проверяем, есть ли уже ингредиенты в базе
        if Ingredient.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Ингредиенты уже загружены. Пропускаем загрузку."
                )
            )
            return

        json_path = "/app/data/ingredients.json"

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"Файл {json_path} не найден."))
            return

        with open(json_path, "r", encoding="utf-8") as file:
            ingredients_data = json.load(file)

        ingredients_to_create = []
        for ingredient_data in ingredients_data:
            ingredients_to_create.append(
                Ingredient(
                    name=ingredient_data["name"],
                    measurement_unit=ingredient_data["measurement_unit"],
                )
            )

        # Создаем ингредиенты
        Ingredient.objects.bulk_create(ingredients_to_create)

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно загружено {len(ingredients_to_create)} ингредиентов"
            )
        )
