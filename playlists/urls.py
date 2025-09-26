from django.urls import path
from . import views

urlpatterns = [
    path('<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('create/', views.create_playlist, name='create_playlist'),
    path('<int:playlist_id>/add-music/', views.add_music_to_playlist, name='add_music_to_playlist'),
    path('<int:playlist_id>/remove-music/', views.remove_music_from_playlist, name='remove_music_from_playlist'),
]

