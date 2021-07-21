from django.urls import path
from . import views

urlpatterns = [
    path('/get_sources', views.get_sources, name="get_sources"),
    path('', views.pre_scraper),
]
