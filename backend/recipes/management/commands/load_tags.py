from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    """Команда для создания базовых тегов."""

    help = "Создание базовых тегов"

    def handle(self, *args, **options):
        """Обработка команды."""
        tags = [
            {"name": "Завтрак", "slug": "breakfast"},
            {"name": "Обед", "slug": "lunch"},
            {"name": "Ужин", "slug": "dinner"},
        ]

        Tag.objects.all().delete()

        for tag_data in tags:
            Tag.objects.create(**tag_data)

        self.stdout.write(
            self.style.SUCCESS(f"Успешно создано {len(tags)} тегов")
        )
