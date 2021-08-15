from django.core.management.base import BaseCommand
from apps.ingredients.detect import detect_ingredients
from apps.ingredients.models import IngredientName
from apps.recipes.models import Recipe


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("--- Detectando ingredients ---")
        recipes = Recipe.objects.all()
        for recipe in recipes:
            print(f"Ingredientes de {recipe.title}")
            detect_ingredients(recipe)
        IngredientName.objects.update(is_active=True)
