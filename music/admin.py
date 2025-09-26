from django.contrib import admin
from .models import Artist, Music


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'duration', 'created_at']
    list_filter = ['artist', 'created_at']
    search_fields = ['title', 'artist__name']
    ordering = ['title']
