from django.urls import path
from . import views
from .views import player_view, upload_music

urlpatterns = [
    path("player/", views.player_view, name="player"),
    path("upload/", views.upload_music, name="upload_music"),
]
