from django.core.management.base import BaseCommand
from apps.recipes.models import Host
import apps.recipes.source_finder as source_finder


class Command(BaseCommand):

    def handle(self, *args, **options):
        hosts = Host.objects.filter(available=True)
        for host in hosts:
            print(f"--- Obtener fuentes para {host.name} ---")
            get_sources_function = eval(
                f"source_finder.{host.get_sources_function_name}"
            )
            get_sources_function()
