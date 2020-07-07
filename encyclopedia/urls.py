from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.new_page, name="new_page"),
    path("edit/<title>", views.edit_page, name="edit_page"),
    path("random", views.random, name="random"),
    path("<str:title>", views.entry, name="entry")
]
