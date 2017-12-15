# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_invoice_canceled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iceslot',
            name='date',
        ),
        migrations.RemoveField(
            model_name='training',
            name='date',
        ),
        migrations.AlterField(
            model_name='iceslot',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='iceslot',
            name='start_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='training',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='training',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]