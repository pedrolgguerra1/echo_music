from django.shortcuts import render
from .models import Music


def player(request):
    return render(request, "player.html")

def player(request):
    current_music = Music.objects.first()  # pega a primeira música (teste)
    queue = Music.objects.all()[1:5]       # próximas músicas
    return render(request, "player.html", {
        "current_music": current_music,
        "queue": queue,
    })


