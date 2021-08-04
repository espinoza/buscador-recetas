from urllib.parse import urlparse
from apps.recipes.models import Host, Source
from bs4 import BeautifulSoup
import requests


def save_source(url, host=None):
    parsed_url = urlparse(url)

    if host is None:
        host = Host.objects.filter(url_netloc=parsed_url.netloc)
        if not host:
            return None
        host = host[0]

    path = parsed_url.path
    source, _ = Source.objects.get_or_create(host=host, url_path=path)
    return source


def recetas_gratis_get_sources():
    host = Host.objects.get(name="Recetas Gratis")
    base_url = "https://www.recetasgratis.net/busqueda/type/1/pag/"
    page_number = 1
    got_all_sources = False

    while not got_all_sources:
        url = base_url + str(page_number)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        detected_page_number = int(soup.find('span', class_="current").text)

        if detected_page_number < page_number:
            got_all_sources = True
            continue

        recipe_links = soup.find_all('a', class_="titulo--resultado")
        for recipe_link in recipe_links:
            source_url = recipe_link['href']
            save_source(source_url, host)

        print(f"Recetas Gratis: página {page_number} del catálogo")
        page_number += 1
