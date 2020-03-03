from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Einreichung


def home(request):
    return render(request, 'choosemusic/home.html', {})

class SuggestionsView(generic.ListView):
    template_name = 'choosemusic/suggestions.html'
    context_object_name = 'suggestions'

    def get_queryset(self):
        return Einreichung.objects.all()

class PlaylistView(generic.ListView):
    template_name = 'choosemusic/playlist.html'
    context_object_name = 'playlist'

    def get_queryset(self):
        try:
            playlist = Einreichung.objects.filter(status="playlist")
        except Einreichung.DoesNotExist:
            playlist = []
        return playlist

def play(request):
    song = ""
    try:
        song = Einreichung.objects.get(status="play")
        if song.has_ended():
            song = False
            raise Einreichung.DoesNotExist
    except Einreichung.DoesNotExist as e:
        try:
            songs = Einreichung.objects.filter(status="playlist").order_by('timestamp')
            if len(songs) > 0:
                song = songs[0]
                song.play()
        except Einreichung.DoesNotExist:
            pass
    if song:
        embedlink = "https://www.youtube.com/embed/"+song.link.split('=')[1] +"?rel=0&autoplay=1&controls=0&showinfo=0&autohide=1&iv_load_policy=3"
    else:
        song = False
        embedlink = ""
    return render(request, 'choosemusic/play.html', {"song":song,"embedlink":embedlink})


@login_required(login_url="/choosemusic/login")
def suggest(request):
    form = request.POST
    if form:
        if request.user.has_perm("change_einreichung"):
            obj = Einreichung.objects.create(link=form["link"],benutzer=request.user,status="playlist")
        else:
            obj = Einreichung.objects.create(link=form["link"],benutzer=request.user)
        obj.save()
        return redirect("/choosemusic/suggestions")
    else:
        return render(request, 'choosemusic/suggest.html', {})
