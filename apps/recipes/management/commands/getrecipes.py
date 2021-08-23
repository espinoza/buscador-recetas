from django.core.management.base import BaseCommand
from apps.recipes.scraper import save_recipe_from_source
from apps.recipes.models import Source


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("--- Obteniendo recetas desde fuentes ---")
        sources = Source.objects.filter(host__available=True)
        for source in sources:
            print(f"Leyendo {source.url}")
            save_recipe_from_source(source)
