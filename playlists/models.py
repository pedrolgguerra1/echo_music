from django.db import models
from django.contrib.auth.models import User
from music.models import Music


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    musics = models.ManyToManyField(Music, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_total_duration(self):
        """Calcula a duração total da playlist"""
        total_seconds = 0
        for music in self.musics.all():
            # Converte duração "2:30" para segundos
            if music.duration:
                parts = music.duration.split(':')
                if len(parts) == 2:
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                    total_seconds += minutes * 60 + seconds
        
        # Converte de volta para formato "mm:ss"
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def get_music_count(self):
        """Retorna o número de músicas na playlist"""
        return self.musics.count()
    
    class Meta:
        ordering = ['-created_at']
