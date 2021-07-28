from django import forms
import re


class SearchForm(forms.Form):

    ingredient_restriction = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
        label="Solo tengo estos ingredientes",
    )

    include_ingredient_names = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "id": "include-ingredient-names",
            }
        )
    )

    exclude_ingredient_names = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "id": "exclude-ingredient-names",
            }
        )
    )

    recipe_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Filtrar por nombre de receta",
            }
        ),
        label="Nombre de la receta",
    )

    def clean(self):
        cleaned_data = super().clean()
        include_ingredient_names = cleaned_data.get("include_ingredient_names")
        exclude_ingredient_names = cleaned_data.get("exclude_ingredient_names")
        RE_INGREDIENTS = re.compile(r'^[A-Za-z_ÑñÁáÉéÍíÓóÚúÜü ,]*$')
        if not (RE_INGREDIENTS.match(include_ingredient_names)
                or RE_INGREDIENTS.match(exclude_ingredient_names)):
            raise forms.ValidationError(
                "Hay un nombre de ingrediente no válido"
            )
        return cleaned_data

    def clean_recipe_name(self):
        recipe_name = self.cleaned_data.get("recipe_name")
        RE_RECIPE_NAME = re.compile(r'^[A-Za-z_ÑñÁáÉéÍíÓóÚúÜü ]*$')
        if not RE_RECIPE_NAME.match(recipe_name):
            raise forms.ValidationError(
                "Nombre de receta no válido"
            )
        return recipe_name

