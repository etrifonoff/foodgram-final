import hashlib

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from users.serializers import RecipeMinifiedSerializer

from .filters import IngredientFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = IngredientFilter
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Выбор сериализатора."""
        if self.action in ("create", "partial_update"):
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        """Создание рецепта."""
        serializer.save(author=self.request.user)

    @staticmethod
    def generate_short_link(recipe_id):
        """Генерация короткой ссылки."""
        hash_object = hashlib.md5(str(recipe_id).encode())
        return hash_object.hexdigest()[:6]

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[AllowAny],
        url_path="get-link",
    )
    def get_link(self, request, pk=None):
        """Получение короткой ссылки на рецепт."""
        recipe = self.get_object()
        if not recipe.short_link:
            recipe.short_link = self.generate_short_link(recipe.id)
            recipe.save()
        short_link = request.build_absolute_uri(f"/s/{recipe.short_link}")
        return Response({"short-link": short_link}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        """Добавление/удаление рецепта из избранного."""
        recipe = self.get_object()
        user = request.user

        if request.method == "POST":
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"errors": "Рецепт уже в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeMinifiedSerializer(
                recipe, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if not favorite.exists():
                return Response(
                    {"errors": "Рецепта нет в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        """Добавление/удаление рецепта из списка покупок."""
        recipe = self.get_object()
        user = request.user

        if request.method == "POST":
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"errors": "Рецепт уже в списке покупок."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeMinifiedSerializer(
                recipe, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            shopping_cart = ShoppingCart.objects.filter(
                user=user, recipe=recipe
            )
            if not shopping_cart.exists():
                return Response(
                    {"errors": "Рецепта нет в списке покупок."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Скачивание списка покупок."""
        user = request.user
        ingredients = (
            Ingredient.objects.filter(
                recipe_ingredients__recipe__shopping_cart__user=user
            )
            .values("name", "measurement_unit")
            .annotate(total_amount=Sum("recipe_ingredients__amount"))
            .order_by("name")
        )

        shopping_list = "Список покупок:\n\n"
        for ingredient in ingredients:
            shopping_list += (
                f"{ingredient['name']} "
                f"({ingredient['measurement_unit']}) — "
                f"{ingredient['total_amount']}\n"
            )

        response = HttpResponse(shopping_list, content_type="text/plain")
        response["Content-Disposition"] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response


def short_link_redirect(request, short_link):
    """Перенаправление по короткой ссылке."""
    recipe = get_object_or_404(Recipe, short_link=short_link)
    return redirect(f"/recipes/{recipe.id}")
