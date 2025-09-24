from django.contrib import admin
from django.utils.html import format_html
from .models import Artist, Music, Playlist


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
    def cover_thumb(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:6px" />', obj.cover.url)
        return "-"
    cover_thumb.short_description = "Capa"


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "cover_thumb", "created_at")
    search_fields = ("name", "user__username")

    def cover_thumb(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:6px" />', obj.cover.url)
        return "-"
    cover_thumb.short_description = "Capa"
