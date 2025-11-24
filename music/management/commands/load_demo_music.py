import os
from urllib.parse import urlparse
from urllib.request import urlopen

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from music.models import Artist, Music


SONGS = [
    {
        "title": "SoundHelix Song 1",
        "artist": "SoundHelix",
        "duration": "6:13",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "cover_url": "https://images.unsplash.com/photo-1464375117522-1311d6a5b81f?auto=format&fit=crop&w=900&q=70",
    },
    {
        "title": "SoundHelix Song 2",
        "artist": "SoundHelix",
        "duration": "5:05",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "cover_url": "https://images.unsplash.com/photo-1483412033650-1015ddeb83d1?auto=format&fit=crop&w=900&q=70",
    },
    {
        "title": "SoundHelix Song 3",
        "artist": "SoundHelix",
        "duration": "4:40",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "cover_url": "https://images.unsplash.com/photo-1470229538611-16ba8c7ffbd7?auto=format&fit=crop&w=900&q=70",
    },
]


def _fetch_bytes(url: str) -> bytes:
    """Download bytes from a URL."""
    with urlopen(url) as response:
        return response.read()


def _pick_filename(prefix: str, url: str, fallback: str) -> str:
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    return f"{prefix}_{name or fallback}"


class Command(BaseCommand):
    help = "Baixa algumas músicas reais de demonstração e popula o banco com artistas/músicas."

    def handle(self, *args, **options):
        os.makedirs(settings.MEDIA_ROOT / "music", exist_ok=True)
        os.makedirs(settings.MEDIA_ROOT / "covers", exist_ok=True)

        for song in SONGS:
            artist, _ = Artist.objects.get_or_create(name=song["artist"])

            music, created = Music.objects.get_or_create(
                title=song["title"],
                artist=artist,
                defaults={"duration": song["duration"]},
            )

            updated = False

            # Baixar e anexar o arquivo de áudio se ainda não existir
            if not music.file_url:
                try:
                    audio_bytes = _fetch_bytes(song["audio_url"])
                    audio_name = _pick_filename(
                        prefix=music.title.lower().replace(" ", "_"),
                        url=song["audio_url"],
                        fallback="audio.mp3",
                    )
                    music.file_url.save(audio_name, ContentFile(audio_bytes), save=False)
                    updated = True
                except Exception as exc:  # noqa: BLE001
                    self.stdout.write(self.style.ERROR(f"Falha ao baixar áudio: {exc}"))

            # Baixar capa se não existir
            if song.get("cover_url") and not music.cover:
                try:
                    cover_bytes = _fetch_bytes(song["cover_url"])
                    cover_name = _pick_filename(
                        prefix=music.title.lower().replace(" ", "_"),
                        url=song["cover_url"],
                        fallback="cover.jpg",
                    )
                    music.cover.save(cover_name, ContentFile(cover_bytes), save=False)
                    updated = True
                except Exception as exc:  # noqa: BLE001
                    self.stdout.write(self.style.ERROR(f"Falha ao baixar capa: {exc}"))

            if music.duration != song["duration"]:
                music.duration = song["duration"]
                updated = True

            if created or updated:
                music.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Música pronta: {music.title} ({artist.name})")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Nada a fazer para: {music.title} ({artist.name})")
                )

        self.stdout.write(self.style.SUCCESS("Catálogo de demonstração instalado!"))
