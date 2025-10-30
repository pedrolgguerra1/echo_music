from django.shortcuts import render, redirect, get_object_or_404
from .models import Music, Favorite
from playlists.models import Playlist
from .forms import MusicForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages


def player(request):
    return render(request, "player.html")


def player_view(request):
    music_id = request.GET.get('music_id')
    if music_id:
        current_music = get_object_or_404(Music, id=music_id)
    else:
        # música atual (escolha por lógica — aqui pegamos a primeira como exemplo)
        current_music = Music.objects.first()

    # fila: usar apenas as músicas adicionadas à fila via session
    queue_ids = request.session.get('music_queue', [])
    next_musics = Music.objects.filter(id__in=queue_ids).order_by('id')

    # playlists do usuário logado
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user=request.user)
    else:
        playlists = Playlist.objects.none()

    # mostruário: 6 itens a partir das músicas (pode criar model separado depois)
    showcase_items = Music.objects.all()[:6]

    # Verificar se a música atual é favorita
    is_favorite = False
    if request.user.is_authenticated and current_music:
        is_favorite = Favorite.objects.filter(user=request.user, music=current_music).exists()

    # Adicionar autoplay se música foi selecionada
    autoplay = bool(music_id)

    context = {
        "current_music": current_music,
        "next_musics": next_musics,
        "playlists": playlists,
        "showcase_items": showcase_items,
        "is_favorite": is_favorite,
        "autoplay": autoplay,
    }
    return render(request, "player.html", context)


@login_required
def toggle_favorite(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, music=music)
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})


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
        return redirect("player")  # or redirect to a success page
    else:
        # Provide artists for selection
        from .models import Artist
        artists = Artist.objects.all()
        return render(request, "music/upload.html", {"artists": artists})


@login_required
def add_to_queue(request, music_id):
    """Adiciona música à fila de reprodução (em seguida)"""
    music = get_object_or_404(Music, id=music_id)

    # Usar sessão para armazenar a fila
    queue = request.session.get('music_queue', [])
    if music_id not in queue:
        queue.append(music_id)
        request.session['music_queue'] = queue
        return JsonResponse({'status': 'added', 'message': f'{music.title} adicionada à fila'})
    else:
        return JsonResponse({'status': 'already_in_queue', 'message': f'{music.title} já está na fila'})


@login_required
def remove_from_queue(request, music_id):
    """Remove música da fila de reprodução"""
    queue = request.session.get('music_queue', [])
    if music_id in queue:
        queue.remove(music_id)
        request.session['music_queue'] = queue
        music = get_object_or_404(Music, id=music_id)
        return JsonResponse({'status': 'removed', 'message': f'{music.title} removida da fila'})
    return JsonResponse({'status': 'not_in_queue', 'message': 'Música não está na fila'})


@login_required
def get_queue(request):
    """Retorna a fila atual de músicas"""
    queue_ids = request.session.get('music_queue', [])
    musics = Music.objects.filter(id__in=queue_ids).order_by('id')
    queue_data = [{'id': music.id, 'title': music.title, 'artist': music.artist.name, 'duration': music.duration} for music in musics]
    return JsonResponse({'queue': queue_data})
