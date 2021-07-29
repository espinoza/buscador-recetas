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

        # Ingredient line as a list of phrases without special characters
        for char in SPECIAL_CHARACTERS:
            line = line.replace(char, "&")
        phrases = [phrase.strip(" ") for phrase in re.split(r'&|\sy\s', line)
                                     if re.search(r'\w', phrase)]

        for phrase in phrases:
            # Analyse concatenations of words that could be ingredient names
            words = [word for word in phrase.split(" ")
                          if not word.isnumeric()]

            # The ingredient name is more likely to appear to the right
            for start in range(len(words)-1, -1, -1):
                end = len(words)
                ingredient_found = False

                while not ingredient_found and end > start:
                    mini_phrase = " ".join(words[start:end])
                    ingredients = Ingredient.objects.filter(
                        Q(names__singular=mini_phrase)
                        | Q(names__plural=mini_phrase)
                    )

                    if ingredients:
                        ingredient_found = True
                        recipe.ingredients.add(*ingredients)
                        end = start
                    else:
                        end -= 1

