from django.urls import path
from . import views

urlpatterns = [

    path('new/source/',
         views.InsertSourceFormView.as_view(),
         name='insert_source'),

]
