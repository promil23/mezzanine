# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20170120_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='slug_en',
            field=models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='page',
            name='slug_pl',
            field=models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL'),
        ),
    ]
