# Generated by Django 2.2.3 on 2019-07-30 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localtrade', '0005_auto_20190730_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='telf',
            field=models.CharField(blank=True, default='', max_length=9),
        ),
    ]
