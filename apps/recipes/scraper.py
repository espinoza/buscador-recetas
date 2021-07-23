from apps.recipes.source_finder import save_source
from django.shortcuts import redirect
from urllib.parse import urlparse
from apps.recipes.models import Recipe, IngredientLine, Host, Source
from bs4 import BeautifulSoup
import requests


def save_recipe_from_url(url):
    source = save_source(url)
    recipe = save_recipe_from_source(source)
    return recipe


def save_recipe_from_source(source):
    try:
        page = requests.get(source.url)
    except:
        return None

    soup = BeautifulSoup(page.content, 'html.parser')
    scraper = eval(source.host.get_recipe_info_function_name)
    title, ingredient_lines, preparation_section = scraper(soup, source)

    if not title:
        return None

    new_recipe = Recipe.objects.create(
        title=title,
        preparation_section=preparation_section,
    )
    for ingredient_line in ingredient_lines:
        new_ingredient_line = IngredientLine.objects.create(
            text=ingredient_line
        )
        new_recipe.ingredient_lines.add(new_ingredient_line)

    source.recipe = new_recipe

    return new_recipe


def recetas_gratis_get_recipe_info(soup, source):
    if soup.find(class_="ctrl-error action-error"):
        if source.clicks == 0:
            source.delete()
        return None, None, None

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
