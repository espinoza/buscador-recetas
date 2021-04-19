from django import forms
from apps.ingredients.models import Ingredient, IngredientName


class AddIngredientForm(forms.Form):

    new_ingredient = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "id": "new-ingredient",
            }
        )
    )

    class Meta:
        fields = []

    def clean_new_ingredient(self):
        new_ingredient = self.cleaned_data.get("new_ingredient")
        if all(char.isalpha() or char.isspace() for char in new_ingredient):
            return new_ingredient
        else:
            raise forms.ValidationError(
                "Nombre no válido."
            )


class CreateIngredientForm(forms.ModelForm):

    class Meta:
        model = IngredientName
        fields = ['singular', 'plural']

    def clean_singular(self):
        singular = self.cleaned_data.get("singular")
        if all(char.isalpha() or char.isspace() for char in singular):
            return singular
        else:
            raise forms.ValidationError(
                "Nombre no válido."
            )

    def clean_plural(self):
        plural = self.cleaned_data.get("plural")
        if all(char.isalpha() or char.isspace() for char in plural):
            return plural
        else:
            raise forms.ValidationError(
                "Nombre no válido."
            )