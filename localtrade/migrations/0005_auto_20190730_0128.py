# Generated by Django 2.2.3 on 2019-07-29 23:28

from django.db import migrations, models
import localtrade.models


class Migration(migrations.Migration):

    dependencies = [
        ('localtrade', '0004_auto_20190730_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='publicid',
            field=models.IntegerField(default=localtrade.models.GetMaxGameId, unique=True),
        ),
    ]
