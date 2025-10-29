from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Music(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    duration = models.CharField(max_length=10)  # formato "2:30"
    file_url = models.URLField(blank=True, null=True)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)  # nova capa
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

    class Meta:
        ordering = ['title']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'music')

    def __str__(self):
        return f"{self.user.username} - {self.music.title}"


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    musics = models.ManyToManyField("music.Music", blank=True, related_name="in_music_playlists")
    cover = models.ImageField(upload_to="playlists/", blank=True, null=True)  # capa da playlist
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

