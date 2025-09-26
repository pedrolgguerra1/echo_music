from django.contrib import admin
from django.urls import path, include
from core.views import home, search_music
from music import views as music_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('search/', search_music, name='search_music'),
    path('playlists/', include('playlists.urls')),
    path("player/", music_views.player, name="player"),
]
