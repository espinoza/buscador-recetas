from apps.recipes.source_finder import save_source
from apps.recipes.models import Recipe, IngredientLine
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
    title, ingredient_lines = scraper(soup, source)

    if not title:
        return None

    if source.recipe:
        recipe = source.recipe.delete()

    recipe = Recipe.objects.create(
        title=title,
    )
    for ingredient_line in ingredient_lines:
        new_ingredient_line = IngredientLine.objects.create(
            text=ingredient_line
        )
        recipe.ingredient_lines.add(new_ingredient_line)

    source.recipe = recipe
    source.save()

    return recipe


def recetas_gratis_get_recipe_info(soup, source):
    if soup.find(class_="ctrl-error action-error"):
        if source.clicks == 0:
            source.delete()
        return None, None

    title_text = soup.find(class_="titulo titulo--articulo").text
    start = 10 if "Receta de " in title_text else 0
    title = title_text[start:]

    ingredient_li_items = soup.find_all(class_="ingrediente")
    ingredient_lines = [li.text.strip("\n") for li in ingredient_li_items]

    return title, ingredient_lines


def recetas_de_rechupete_get_recipe_info(soup, source):
    if soup.find(id="error404") or not soup.find(id="ingredients"):
        if source.clicks == 0:
            source.delete()
        return None, None

    title_text = soup.header.h1.text.strip("\t\r\n")
    end = title_text.find(".") if "." in title_text else len(title_text)
    title = title_text[:end]

    ingredient_li_items = soup.find(id="ingredients").find_all('li')
    ingredient_lines = [li.text for li in ingredient_li_items]

    return title, ingredient_lines
