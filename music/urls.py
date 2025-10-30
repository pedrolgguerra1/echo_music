from django.urls import path
from . import views

urlpatterns = [
    path("player/", views.player_view, name="player"),
    path("upload/", views.upload_music, name="upload_music"),
    path("favorite/<int:music_id>/", views.toggle_favorite, name="toggle_favorite"),
    path("queue/add/<int:music_id>/", views.add_to_queue, name="add_to_queue"),
    path("queue/remove/<int:music_id>/", views.remove_from_queue, name="remove_from_queue"),
    path("queue/", views.get_queue, name="get_queue"),
    path("next/", views.next_music, name="next_music"),
    path("prev/", views.prev_music, name="prev_music"),
]
