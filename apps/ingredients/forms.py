from django import forms
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
        text_input = lambda singular_plural: forms.TextInput(
            attrs={
                "placeholder": singular_plural,
                "size": 7,
            }
        )
        widgets = {
            "singular": text_input("Singular"),
            "plural": text_input("Plural"),
        }

    def clean_singular(self):
        singular = self.cleaned_data.get("singular", "")
        if all(char.isalpha() or char.isspace() for char in singular):
            return singular.lower()
        else:
            raise forms.ValidationError(
                "Nombre no válido."
            )

    def clean_plural(self):
        plural = self.cleaned_data.get("plural", "")
        if plural is None:
            return None
        if all(char.isalpha() or char.isspace() for char in plural):
            return plural.lower()
        else:
            raise forms.ValidationError(
                "Nombre no válido."
            )
