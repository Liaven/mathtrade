from django.db.models import Max
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list


def GetMaxGameId():
  max = Game.objects.all().aggregate(Max('publicid'))['publicid__max']
  if not max:
    return 1
  return max + 1


def validate_checklist(value):
    err = None
    try:
        validate_comma_separated_integer_list(value)
        # Check all
        for item in value.split(","):
            obj = Game.objects.get(pk=item)
    except Game.DoesNotExist:
        raise ValidationError(str(item) + ' Not found in games')
    except ValidationError as exc:
        err = exc
    # Value match nothing, raise error
    if not err is None:
        raise err




class Player(models.Model):
    name = models.CharField(max_length=50)
    telf = models.CharField(max_length=9, default="", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "#player-{pk}".format(pk=self.pk)


class Game(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    publicid = models.IntegerField(default=GetMaxGameId, unique=True)
    name = models.CharField(max_length=250)
    idbgg = models.CharField(max_length=20, default="", blank=True)
    description = models.CharField(max_length=300, default="", blank=True)
    changelist = models.CharField(max_length=500, default="", blank=True, validators=[validate_checklist])
    imageurl = models.URLField(default="", blank=True)


    def __str__(self):
        return '{} - {}'.format(self.publicid, self.name)

    def get_absolute_url(self):
        return "#game-{pk}".format(pk=self.pk)