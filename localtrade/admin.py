# Register your models here.
from django.http import HttpResponseRedirect
from django.forms import Textarea
from django.contrib import admin, messages
from django.db import models
from inline_actions.admin import InlineActionsMixin
from inline_actions.admin import InlineActionsModelAdminMixin
from libbgg.apiv2 import BGG


from .models import Player, Game

bgg = BGG()


def getformfield(request, pk, field):
    formfield = ""
    items = request.POST.dict().items()
    for key, value in items:
        print (key)
        if key.startswith("game_set-") and key.endswith("-id") and value == pk:
            deskey = key.replace("-id", "-" + field)
            formfield = request.POST[deskey]
    return formfield

from django.utils.safestring import mark_safe

def getbgginfo(name, id, url):
    newid = id
    newurl = url

    if newid == "":
        result = bgg.search(name, qtype='boardgame', exact=True)
        number = int(result["items"]["total"])
        if (number == 1):
            newid = result["items"]["item"]["id"]
        elif (number > 1):
            newid = result["items"]["item"][0]["id"]
    if newid != "" and newurl == "":
        result = bgg.boardgame(newid)
        newurl = result['items']['item']['thumbnail']['TEXT']
    return newid, newurl


class GameInline(InlineActionsMixin, admin.TabularInline):
    model = Game
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})},
    }
    inline_actions = ['bgg']
    readonly_fields = ["headshot_image"]
    exclude= ['imageurl']


    def headshot_image(self, obj):
        return mark_safe('<img src="{url}"/>'.format(url=obj.imageurl))


    def bgg(self, request, obj, parent_obj=None):
        # Get bgg id
        newname = getformfield(request, str(obj.pk), "name")
        obj.idbgg, obj.imageurl = getbgginfo(newname, obj.idbgg, obj.imageurl)
        obj.save()
        messages.info(request, "New bgg saved")

        return
        #return redirect(url)

    bgg.short_description = "Check bgg"


    def get_toggle_bgg_css(self, obj):
        return ('button object-tools')
        #return('default')


class PlayerAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    inlines = [
        GameInline,
    ]
    change_form_template = "localtrade/admin_playeraddbutton.html"

    def response_change(self, request, obj):
        if "_check-data" in request.POST:
            obj.save()
            self.message_user(request, "Show PopUp")
            #return HttpResponseRedirect(".")
            return HttpResponseRedirect('/showtrade/' + str(obj.pk))
        return super().response_change(request, obj)


    def save_related(self, request, form, formsets, change):
        super(PlayerAdmin, self).save_related(request, form, formsets, change)
        player = form.instance
        for game in Game.objects.all().filter(player=player.id):
            if game.idbgg == "" or game.imageurl == "":
                game.idbgg, game.imageurl = getbgginfo(game.name, game.idbgg, game.imageurl)
                game.save()
        #player.save()


admin.site.register(Player, PlayerAdmin)
admin.site.register(Game)

