# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 18:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cau_college', '0005_auto_20170426_1849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursecollege',
            options={'verbose_name': '学院', 'verbose_name_plural': '学院'},
        ),
    ]
