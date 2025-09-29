from django.shortcuts import render, redirect
from .models import Music
from playlists.models import Playlist
from .forms import MusicForm
from django.contrib.auth.decorators import login_required


def player(request):
    return render(request, "player.html")


def player_view(request):
    # música atual (escolha por lógica — aqui pegamos a primeira como exemplo)
    current_music = Music.objects.first()

    # fila: próximas 5 (exceto a atual)
    if current_music:
        next_musics = Music.objects.exclude(id=current_music.id)[:5]
    else:
        next_musics = Music.objects.all()[:5]

    # playlists do usuário logado
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user=request.user)
    else:
        playlists = Playlist.objects.none()

    # mostruário: 6 itens a partir das músicas (pode criar model separado depois)
    showcase_items = Music.objects.all()[:6]

    context = {
        "current_music": current_music,
        "next_musics": next_musics,
        "playlists": playlists,
        "showcase_items": showcase_items,
    }
    return render(request, "player.html", context)


@login_required
def upload_music(request):
    if request.method == "POST":
        title = request.POST.get("title")
        artist_id = request.POST.get("artist")
        duration = request.POST.get("duration")
        file_url = request.FILES.get("file_url")
        cover = request.FILES.get("cover")

        # Basic validation
        if not title or not artist_id or not duration or not file_url:
            error = "Por favor, preencha todos os campos obrigatórios."
            return render(request, "music/upload.html", {"error": error})

        # Get artist instance
        from .models import Artist
        try:
            artist = Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            error = "Artista inválido."
            return render(request, "music/upload.html", {"error": error})

        # Save music instance
        music = Music(
            title=title,
            artist=artist,
            duration=duration,
            file_url=file_url,
            cover=cover
        )
        music.save()
        return redirect("player")
    else:
        # Provide artists for selection
        from .models import Artist
        artists = Artist.objects.all()
        return render(request, "music/upload.html", {"artists": artists})
