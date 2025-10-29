from django.urls import path
from . import views
from .views import player_view, upload_music, toggle_favorite

urlpatterns = [
    path("player/", views.player_view, name="player"),
    path("upload/", views.upload_music, name="upload_music"),
    path("favorite/<int:music_id>/", views.toggle_favorite, name="toggle_favorite"),
    path("queue/add/<int:music_id>/", views.add_to_queue, name="add_to_queue"),
    path("queue/remove/<int:music_id>/", views.remove_from_queue, name="remove_from_queue"),
    path("queue/", views.get_queue, name="get_queue"),
]
