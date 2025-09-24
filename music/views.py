from django.shortcuts import render
from .models import Music
from playlists.models import Playlist


def player(request):
    return render(request, "player.html")

def player_view(request):
    musics = Music.objects.all()
    return render(request, "player.html", {"musics": musics})



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