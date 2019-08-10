from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .models import Player, Game
from django.http import Http404
import subprocess
import os
import re


def index(request):
    return render(request, 'localtrade/index.html')
    #return HttpResponse("Hello, world. You're at the polls index.")


def ShowTrade(request, pk):
    try:
        player = Player.objects.get(pk=pk)
        games = Game.objects.filter(player=pk)
    except Player.DoesNotExist:
        raise Http404("Poll does not exist")
    except Game.DoesNotExist:
        games = []
    # Convert games
    listgames = []
    for game in games:
        gam = {"name": game.name, "picture": game.imageurl, "trades": []}
        if game.changelist != "":
            for related in game.changelist.split(","):
                if related == "":
                    continue
                g = Game.objects.get(pk=related)
                gam["trades"].append({"name": g.name, "picture": g.imageurl})
        listgames.append(gam)
    return render(request, 'localtrade/player_trade.html', {'player':player, 'games': listgames} )


def ShowWants(request):
    lines = []

    os.chdir(os.path.dirname(__file__))
    filename = os.path.join(os.getcwd(), "wantlist.txt")

    file = open(filename, 'w')
    for game in Game.objects.order_by('player', 'publicid'):
        line = "(" + game.player.name + ") " + str(game.publicid) + " : " + game.changelist.replace(",", " ")
        lines.append(line)
        file.write(line + "\n")
    file.close()

    return render(request, 'localtrade/wantlist.html', {'lines': lines, 'filename': filename})


def _getGame(idgame, user):
    try:
        game = Game.objects.get(publicid=idgame)
        name = user + " (" + game.name + ")"
        image = game.imageurl
    except Game.DoesNotExist:
        name = "NOT FOUND (" + idgame + ")"
        image = ""
    return name, image


def ExecTrade(request):
    regex = "^\((?P<name1>.*)\) (?P<game1>\d) *receives \((?P<name2>.*)\) (?P<game2>\d) *and sends to \((?P<name3>.*)\) (?P<game3>\d)$"
    regnotrade = "^\((?P<name1>.*)\) (?P<game1>\d) *does not trade$"
    os.chdir(os.path.dirname(__file__))
    jarname = os.path.join(os.getcwd(), "tm.jar")
    filename = os.path.join(os.getcwd(), "wantlist.txt")

    p = subprocess.Popen(["java", "-jar", jarname, filename],stdout=subprocess.PIPE)
    out, err = p.communicate()
    sout = out.decode("utf-8")
    lines = sout.splitlines()
    data = []

    for line in lines:
        game1 = ""
        game2 = ""
        game3 = ""
        urlgame1 = ""
        urlgame2 = ""
        urlgame3 = ""
        match = re.match(regex, line)
        if match is not None:
            game1, urlgame1 = _getGame(match.group("game1"), match.group("name1"))
            game2, urlgame2 = _getGame(match.group("game2"), match.group("name2"))
            game3, urlgame3 = _getGame(match.group("game3"), match.group("name3"))
        else:
            match = re.match(regnotrade, line)
            if match is not None:
                game1, urlgame1 = _getGame(match.group("game1"), match.group("name1"))

        if game1 != "":
            data.append( {"game1": game1, "game2": game2, "game3": game3,
                         "urlgame1": urlgame1, "urlgame2": urlgame2, "urlgame3": urlgame3 })

    return render(request, 'localtrade/results.html', {'data': data})

