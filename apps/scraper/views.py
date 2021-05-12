from django.shortcuts import render, redirect
from urllib.parse import urlparse
from apps.scraper.models import Host, Source
from apps.recipes.models import Recipe, RecipeEdition, IngredientLine
from bs4 import BeautifulSoup
import requests


def pre_scraper(request):
    source_url = request.GET["source_url"]
    parsed_url = urlparse(source_url)
    host = Host.objects.filter(url_netloc=parsed_url.netloc)
    if not host:
        return redirect("/")
    host = host[0]

    page = requests.get(source_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    scraper_function_name = host.name.lower().replace(" ", "_") + "_scraper"
    scraper = eval(scraper_function_name)
    title, ingredient_lines, preparation_section = scraper(soup)

    new_recipe = Recipe.objects.create(author=request.user)
    new_recipe_edition = RecipeEdition.objects.create(
        title=title,
        author=request.user,
        preparation_section=preparation_section,
        recipe=new_recipe,
    )
    for ingredient_line in ingredient_lines:
        new_ingredient_line = IngredientLine.objects.create(
            text=ingredient_line
        )
        new_recipe_edition.ingredient_lines.add(new_ingredient_line)

    return redirect('check_recipe_ingredients', recipe_id=new_recipe.id)


def recetas_gratis_scraper(soup):
    title_item = soup.find(class_="titulo")
    start = len("Receta de ")
    title = title_item.text[start:]

    ingredient_li_items = soup.find_all(class_="ingrediente")
    ingredient_lines = [li.text.strip("\n") for li in ingredient_li_items]

    preparation_div_items = soup.find_all(class_="apartado")
    instructions = [div.text.strip("\n")
                    for div in preparation_div_items]
    excluded_phrases = ["Si te ha gustado la receta", "Sube la foto de"]
    real_instructions = [inst for inst in instructions
                              if not any(inst.startswith(phrase)
                                         for phrase in excluded_phrases)]
    preparation_section = "\n\n".join(real_instructions)

    return title, ingredient_lines, preparation_section
