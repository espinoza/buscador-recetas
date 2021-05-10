from django.db import models
from apps.recipes.models import Recipe


class Host(models.Model):
    name = models.CharField(max_length=255)
    url_scheme = models.CharField(max_length=5)
    url_netloc = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def url(self):
        return self.url_scheme + "://" + self.url_netloc


class Source(models.Model):
    host = models.ForeignKey(to=Host, on_delete=models.CASCADE,
                             related_name="sources")
    url_path = models.CharField(max_length=255)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    recipe = models.OneToOneField(to=Recipe, null=True,
                                  on_delete=models.SET_NULL,
                                  related_name="source")

    @property
    def url(self):
        return self.host.url + self.url_path
