# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_remove_subscription_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='number',
        ),
        migrations.AddField(
            model_name='invoice',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
