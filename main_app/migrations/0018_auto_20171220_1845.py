# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_subscription_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paid_date',
            field=models.DateField(null=True),
        ),
    ]
