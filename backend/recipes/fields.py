import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для работы с изображениями в base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}"
            )
        return super().to_internal_value(data)

    def to_representation(self, value):
        """Возвращает относительный URL вместо абсолютного."""
        if not value:
            return None
        # Возвращаем относительный URL, чтобы избежать Mixed Content ошибок
        return value.url
