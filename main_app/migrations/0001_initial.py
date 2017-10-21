# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 18:55
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.PositiveSmallIntegerField(unique=True, validators=[django.core.validators.RegexValidator(message='Bitte vierstellige PLZ eingeben', regex='^\\d{4}$')])),
                ('city', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(message='Bitte gültige Telefonnummer eingeben', regex='^\\+41\\d{9}$')])),
                ('email', models.EmailField(max_length=200)),
                ('website', models.URLField(blank=True, max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='main_app.City')),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
