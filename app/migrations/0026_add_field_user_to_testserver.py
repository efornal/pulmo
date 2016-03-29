# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0025_add_field_related_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='testserver',
            name='user',
            field=models.ForeignKey(verbose_name='Usuario', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='date_event',
            field=models.DateTimeField(null=True, verbose_name='Fecha del evento', blank=True),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='ip_firewall',
            field=models.CharField(max_length=200, null=True, verbose_name='IP Firewall'),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='port',
            field=models.CharField(max_length=200, null=True, verbose_name='Puerto', blank=True),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='related_ticket',
            field=models.CharField(max_length=200, null=True, verbose_name='Ticket relacionado'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='related_ticket',
            field=models.CharField(max_length=200, null=True, verbose_name='Ticket relacionado'),
        ),
    ]
