from django import forms
from urllib.parse import urlparse
from apps.scraper.models import Host, Source


class SourceUrlForm(forms.Form):

    source_url = forms.CharField(
        label="Escribe la url de una fuente externa"
    )

    def clean(self):
        cleaned_data = super().clean()
        source_url = cleaned_data.get("source_url")
        parsed_url = urlparse(source_url)
        host = Host.objects.filter(url_scheme=parsed_url.scheme) \
                           .filter(url_netloc=parsed_url.netloc)
        if not host:
            raise forms.ValidationError(
                "El sitio ingresado no forma parte de los sitios permitidos"
            )
        host = host[0]
        source = Source.objects.filter(host=host) \
                               .filter(url_path=parsed_url.path)
        if source:
            raise forms.ValidationError(
                "La url ya fue ingresada para otra receta"
            )
        return cleaned_data

