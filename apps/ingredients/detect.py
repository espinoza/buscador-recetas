import re
from django.db.models import Q
from apps.ingredients.models import Ingredient

def detect_ingredients(recipe):
    """Reads ingredient lines in a recipe to search for ingredient names
    and saves many to many relationship between the recipe and corresponding
    ingredient objects.
    """
    recipe.ingredients.clear()
    SPECIAL_CHARACTERS = ",.;:¡!¿?()/"

    for ingredient_line in recipe.ingredient_lines.all():
        line = ingredient_line.text.lower()

        # Analyse concatenations of words that could be ingredient names
        for char in SPECIAL_CHARACTERS:
            line = line.replace(char, "&")
        phrases = [phrase.strip(" ") for phrase in re.split(r'&|\sy\s', line)
                                     if re.search(r'\w', phrase)]

        for phrase in phrases:
            words = [word for word in phrase.split(" ")
                          if not word.isnumeric()]

            for end in range(len(words), 0, -1):
                start = 0
                ingredient_found = False

                while not ingredient_found and start < end:
                    mini_phrase = " ".join(words[start:end])
                    ingredients = Ingredient.objects.filter(
                        Q(names__singular=mini_phrase)
                        | Q(names__plural=mini_phrase)
                    )

                    if ingredients:
                        ingredient_found = True
                        recipe.ingredients.add(*ingredients)
                    else:
                        start += 1
