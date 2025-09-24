from django.urls import path
from . import views
from .views import player_view

urlpatterns = [
    path("player/", views.player_view, name="player"),
]
