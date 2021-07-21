from django.shortcuts import redirect
from urllib.parse import urlparse
from apps.scraper.models import Host, Source
from apps.recipes.models import Recipe, IngredientLine
from bs4 import BeautifulSoup
import requests


def pre_scraper(request):
    source_url = request.GET["source_url"]
    new_recipe = save_recipe_from_source(source_url)
    return redirect('check_recipe_ingredients', recipe_id=new_recipe.id)


def get_sources(request):
    hosts = Host.objects.all()
    for host in hosts:
        get_sources_function = eval(host.get_sources_function_name)
        get_sources_function()
    return redirect("insert_source")


def save_recipe_from_source(source_url):
    parsed_url = urlparse(source_url)
    host = Host.objects.filter(url_netloc=parsed_url.netloc)
    if not host:
        return redirect("/")
    host = host[0]

    page = requests.get(source_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    scraper = eval(host.scraper_function_name)
    title, ingredient_lines, preparation_section = scraper(soup)

    new_recipe = Recipe.objects.create(
        title=title,
        preparation_section=preparation_section,
    )
    for ingredient_line in ingredient_lines:
        new_ingredient_line = IngredientLine.objects.create(
            text=ingredient_line
        )
        new_recipe.ingredient_lines.add(new_ingredient_line)

    Source.objects.create(host=host, url_path=source_url, recipe=new_recipe)

    return new_recipe


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
            new_source_url = recipe_link['href']
            existing_source = Source.objects.filter(url_path=new_source_url)
            if existing_source:
                continue
            Source.objects.create(host=host, url_path=new_source_url)

        page_number += 1


def recetas_gratis_scraper(soup):
    title_item = soup.find(class_="titulo")
    start = len("Receta de ")
    title = title_item.text[start:]

    ingredient_li_items = soup.find_all(class_="ingrediente")
    ingredient_lines = [li.text.strip("\n") for li in ingredient_li_items]

    preparation_div_items = soup.find_all(class_="apartado")
    instructions = [div.text.strip("\n")
                    for div in preparation_div_items]
    preparation_section = "\n\n".join(instructions)

    return title, ingredient_lines, preparation_section
