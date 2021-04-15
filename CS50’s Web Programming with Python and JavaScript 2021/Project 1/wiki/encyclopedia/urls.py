from django.urls import path

from . import views

urlpatterns = [
    path("wiki/<str:title>", views.page, name="page"),
    path("", views.index, name="index"),
    path("random",views.random_page, name="random"),
    path("edit/<str:edition_entry>",views.edit_page, name="edit_page"),
    path("new", views.new_page, name="new")
]
