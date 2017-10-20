# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 08:38
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20171018_1821_squashed_0005_auto_20171018_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='zip_code',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.RegexValidator(message='Bitte vierstellige PLZ eingeben', regex='^\\d{4}$')]),
        ),
    ]
