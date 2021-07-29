from django import forms
from django.forms import widgets
from apps.ingredients.models import IngredientName


class AddIngredientForm(forms.Form):

    new_ingredient = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "id": "new-ingredient",
            }
        )
    )

    def clean_new_ingredient(self):
        new_ingredient = self.cleaned_data.get("new_ingredient")
        if not all(char.isalpha() or char.isspace()
                   for char in new_ingredient):
            raise forms.ValidationError("Nombre no válido.")
        else:
            return new_ingredient


class CreateIngredientNameForm(forms.ModelForm):

    ingredient_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    class Meta:
        model = IngredientName
        fields = ["singular", "plural"]
        labels = {
            "singular": "",
            "plural": "",
        }
        widgets = {
            "singular": forms.TextInput(attrs={"placeholder": "Singular"}),
            "plural": forms.TextInput(attrs={"placeholder": "Plural"}),
        }

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
