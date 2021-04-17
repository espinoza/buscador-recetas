from django.contrib import admin
from .models import User, City, Country

admin.site.register([User, City, Country])