from django.contrib import admin
from .models import Host, Source

admin.site.register([Host, Source])