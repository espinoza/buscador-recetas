from django import forms
import re


class SearchButtonForm(forms.Form):

    ingredient_names = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "id": "ingredient-names",
                "value": "",
            }
        )
    )

    search_mode = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Buscar recetas que contengan...",
        choices=[
            ("soft", "...al menos uno de estos ingredientes"),
            ("normal", "...todos estos ingredientes"),
            ("hard", "...solo estos ingredientes"),
        ],
    )

    class Meta:
        fields = []

    def clean(self):
        cleaned_data = super(SearchButtonForm, self).clean()
        ingredient_names = cleaned_data.get("ingredient_names")
        RE_INGREDIENTS = re.compile(r'^[a-z ,]+$')
        if not RE_INGREDIENTS.match(ingredient_names):
            raise forms.ValidationError(
                "Hay un nombre de ingrediente no válido"
            )
        search_mode = cleaned_data.get("search_mode")
        if search_mode not in ("soft", "normal", "hard"):
            raise forms.ValidationError(
                "Problema al realizar la búsqueda"
            )
        return cleaned_data