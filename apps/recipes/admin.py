from django.contrib import admin
from .models import Recipe, Host, Source

admin.site.register([Recipe, Host, Source])