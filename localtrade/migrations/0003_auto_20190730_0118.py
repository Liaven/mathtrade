# Generated by Django 2.2.3 on 2019-07-29 23:18

from django.db import migrations, models
import localtrade.models


class Migration(migrations.Migration):

    dependencies = [
        ('localtrade', '0002_auto_20190730_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='publicid',
            field=models.IntegerField(default=localtrade.models.GetMaxGameId, unique=False),
        ),
    ]
