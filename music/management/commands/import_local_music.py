import os
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.core.files.base import File
from django.core.management.base import BaseCommand

from music.models import Artist, Music

SUPPORTED_AUDIO_EXT = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
SUPPORTED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def _safe_duration(path: Path) -> str:
    """Try to read duration using mutagen; fallback to '--:--'."""
    try:
        from mutagen import File as MutagenFile  # type: ignore
    except Exception:
        return "--:--"

    try:
        audio = MutagenFile(path)
        if not audio or not audio.info or not getattr(audio.info, "length", None):
            return "--:--"
        total_seconds = int(audio.info.length)
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes}:{seconds:02d}"
    except Exception:
        return "--:--"


def _find_cover(media_root: Path, audio_path: Path) -> Optional[Path]:
    """Look for a cover with the same stem either beside the file or in media/covers."""
    stem = audio_path.stem

    # 1) Same directory as audio
    for ext in SUPPORTED_IMAGE_EXT:
        candidate = audio_path.with_suffix(ext)
        if candidate.exists():
            return candidate

    # 2) media/covers/<stem>.<ext>
    covers_dir = media_root / "covers"
    for ext in SUPPORTED_IMAGE_EXT:
        candidate = covers_dir / f"{stem}{ext}"
        if candidate.exists():
            return candidate

    return None


def _parse_artist_title(filename: str) -> tuple[str, str]:
    """From 'Artist - Title.mp3' => ('Artist', 'Title'); fallback to 'Desconhecido'."""
    name_part = Path(filename).stem
    if " - " in name_part:
        artist, title = name_part.split(" - ", 1)
        return artist.strip() or "Desconhecido", title.strip() or name_part
    return "Desconhecido", name_part


class Command(BaseCommand):
    help = (
        "Importa arquivos já presentes em MEDIA_ROOT/music criando registros de música/artist.\n"
        "Suporta extensões: mp3, wav, ogg, flac, m4a. Para preencher duração, instale 'mutagen'.\n"
        "Capa: arquivo com o mesmo nome do áudio (.jpg/.png/.webp) na mesma pasta ou em media/covers."
    )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        music_dir = media_root / "music"

        if not music_dir.exists():
            self.stdout.write(self.style.ERROR(f"Pasta não encontrada: {music_dir}"))
            return

        created = 0
        skipped = 0
        updated_count = 0

        for audio_path in music_dir.rglob("*"):
            if not audio_path.is_file() or audio_path.suffix.lower() not in SUPPORTED_AUDIO_EXT:
                continue

            artist_name, title = _parse_artist_title(audio_path.name)
            artist, _ = Artist.objects.get_or_create(name=artist_name)

            rel_path = audio_path.relative_to(media_root).as_posix()
            basename = audio_path.name.lower()

            # Evita duplicar músicas já cadastradas pelo caminho do arquivo ou pelo nome
            existing = (
                Music.objects.filter(file_url=rel_path).first()
                or Music.objects.filter(file_url__iendswith=basename).first()
                or Music.objects.filter(title=title, artist=artist).first()
            )
            if existing:
                # Atualiza metadados se estiverem faltando
                item_updated = False
                if not existing.duration or existing.duration in ("", "--:--", "0:00", None):
                    duration = _safe_duration(audio_path)
                    if duration != "--:--":
                        existing.duration = duration
                        item_updated = True
                if not existing.cover:
                    cover_path = _find_cover(media_root, audio_path)
                    if cover_path:
                        rel_cover = cover_path.relative_to(media_root).as_posix()
                        with cover_path.open("rb") as f:
                            existing.cover.save(str(rel_cover), File(f), save=False)
                        item_updated = True
                if existing.artist.name == "Desconhecido" and artist_name != "Desconhecido":
                    existing.artist = artist
                    item_updated = True
                if item_updated:
                    existing.save()
                    updated_count += 1
                else:
                    skipped += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Pulando duplicada: {title} ({artist_name}) já existe (id={existing.id})"
                    )
                )
                continue

            music = Music(
                title=title,
                artist=artist,
                duration=_safe_duration(audio_path),
            )
            just_created = True

            # If file_url empty, attach existing file
            item_updated = False

            if not music.file_url:
                # store relative path (relative to MEDIA_ROOT)
                rel_path = audio_path.relative_to(media_root)
                # reopen as File for Django to keep storage happy
                with audio_path.open("rb") as f:
                    music.file_url.save(str(rel_path), File(f), save=False)
                item_updated = True

            # Fill duration if missing/placeholder
            if music.duration in ("", "--:--", "0:00", None):
                duration = _safe_duration(audio_path)
                if duration != "--:--":
                    music.duration = duration
                    item_updated = True

            # Try to attach cover if none
            if not music.cover:
                cover_path = _find_cover(media_root, audio_path)
                if cover_path:
                    rel_cover = cover_path.relative_to(media_root)
                    with cover_path.open("rb") as f:
                        music.cover.save(str(rel_cover), File(f), save=False)
                    item_updated = True

            if just_created:
                created += 1
            elif item_updated:
                updated_count += 1
            else:
                skipped += 1

            music.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Criadas: {created}, atualizadas: {updated_count}, mantidas: {skipped}"
            )
        )
        self.stdout.write(self.style.SUCCESS("Importação concluída."))
