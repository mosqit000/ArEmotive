from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.startup),
    path("queryStringFromOntology/", views.searchTerm)
]