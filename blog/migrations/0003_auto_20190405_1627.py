# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-05 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190405_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='pv',
        ),
        migrations.RemoveField(
            model_name='category',
            name='uv',
        ),
        migrations.AddField(
            model_name='post',
            name='pv',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='post',
            name='uv',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
