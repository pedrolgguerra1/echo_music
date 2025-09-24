from django.contrib import admin
from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'get_music_count', 'get_total_duration', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username']
    filter_horizontal = ['musics']
    ordering = ['-created_at']
