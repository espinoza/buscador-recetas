from django.shortcuts import redirect
from urllib.parse import urlparse
from apps.recipes.models import Recipe, IngredientLine, Host, Source
from bs4 import BeautifulSoup
import requests


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


def recetas_gratis_get_recipe_info(soup):
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