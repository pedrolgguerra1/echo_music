from django.contrib import admin
from django.urls import path, include
from core.views import home, search_music
from music import views as music_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", home, name="home"),
    path("search/", search_music, name="search_music"),
    path("player/", music_views.player, name="player"),
    path("music/", include("music.urls")),
    path("playlists/", include("playlists.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # ⚠️ não usa STATIC_ROOT no dev, deixa o Django servir dos apps
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
