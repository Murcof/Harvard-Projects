from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:word_id>", views.word, name="word"),
    path("search/<str:word>", views.search, name="search"),
    path("letter/<str:letter>", views.first_letter, name="first_letter"),
    path("game/<int:word_id>", views.game, name="game"),

    #API routes
    path('random', views.random, name='random')
]