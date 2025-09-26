from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Playlist
from music.models import Music


@login_required
def playlist_detail(request, playlist_id):
    """Página de detalhes da playlist"""
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    musics = playlist.musics.all()
    
    context = {
        'playlist': playlist,
        'musics': musics,
    }
    return render(request, 'playlists/detail.html', context)


@login_required
def create_playlist(request):
    """Criar uma nova playlist"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            playlist = Playlist.objects.create(
                name=name,
                user=request.user
            )
            messages.success(request, f'Playlist "{name}" criada com sucesso!')
            return redirect('playlist_detail', playlist_id=playlist.id)
        else:
            messages.error(request, 'Nome da playlist é obrigatório.')
    
    return render(request, 'playlists/create.html')


@login_required
def add_music_to_playlist(request, playlist_id):
    """Adicionar música à playlist via AJAX"""
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        music_id = request.POST.get('music_id')
        
        try:
            music = Music.objects.get(id=music_id)
            playlist.musics.add(music)
            return JsonResponse({
                'success': True,
                'message': f'Música "{music.title}" adicionada à playlist!'
            })
        except Music.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Música não encontrada.'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido.'})


@login_required
def remove_music_from_playlist(request, playlist_id):
    """Remover música da playlist via AJAX"""
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        music_id = request.POST.get('music_id')
        
        try:
            music = Music.objects.get(id=music_id)
            playlist.musics.remove(music)
            return JsonResponse({
                'success': True,
                'message': f'Música "{music.title}" removida da playlist!'
            })
        except Music.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Música não encontrada.'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido.'})
