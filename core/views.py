from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import JsonResponse
from music.models import Music, Artist
from playlists.models import Playlist


def home(request):
    """Página inicial com busca de músicas e playlists do usuário"""
    search_query = request.GET.get('search', '')
    musics = []
    playlists = []
    
    if search_query:
        musics = Music.objects.filter(
            Q(title__icontains=search_query) | 
            Q(artist__name__icontains=search_query)
        )[:10]
    else:
        # Mostrar algumas músicas aleatórias
        musics = Music.objects.all()[:6]
    
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user=request.user)[:5]
    
    context = {
        'musics': musics,
        'playlists': playlists,
        'search_query': search_query,
    }
    return render(request, 'core/home.html', context)


def search_music(request):
    """API endpoint para busca de músicas via AJAX"""
    query = request.GET.get('q', '')
    if query:
        musics = Music.objects.filter(
            Q(title__icontains=query) | 
            Q(artist__name__icontains=query)
        )[:10]
        
        results = []
        for music in musics:
            results.append({
                'id': music.id,
                'title': music.title,
                'artist': music.artist.name,
                'duration': music.duration,
            })
        
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})


def signup(request):
    """Página de cadastro de usuário"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao criar conta. Verifique os dados.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})
