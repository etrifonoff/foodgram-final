from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для тегов."""

    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    list_filter = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""

    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)


class RecipeIngredientInline(admin.TabularInline):
    """Инлайн для ингредиентов в рецепте."""

    model = RecipeIngredient
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для рецептов."""

    list_display = ("id", "name", "author", "favorites_count")
    search_fields = ("name", "author__username")
    list_filter = ("author", "tags")
    inlines = [RecipeIngredientInline]
    readonly_fields = ("favorites_count",)

    def favorites_count(self, obj):
        """Количество добавлений в избранное."""
        return obj.favorites.count()

    favorites_count.short_description = "В избранном"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка для избранного."""

    list_display = ("id", "user", "recipe")
    search_fields = ("user__username", "recipe__name")
    list_filter = ("user",)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админка для списка покупок."""

    list_display = ("id", "user", "recipe")
    search_fields = ("user__username", "recipe__name")
    list_filter = ("user",)
