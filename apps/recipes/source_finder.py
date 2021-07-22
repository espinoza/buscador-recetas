from django.shortcuts import redirect
from apps.recipes.models import Host, Source
from bs4 import BeautifulSoup
import requests


def get_sources_for_all_hosts():
    hosts = Host.objects.all()
    for host in hosts:
        get_sources_function = eval(host.get_sources_function_name)
        get_sources_function()
    return redirect("update_recipe_database")


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
