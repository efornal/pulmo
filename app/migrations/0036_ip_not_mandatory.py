# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_blanck_in_mandatory_referrers_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='ip',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='IP', validators=[django.core.validators.validate_ipv46_address]),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='ip',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='IP', validators=[django.core.validators.validate_ipv46_address]),
        ),
        migrations.AlterField(
            model_name='productionconnectionsource',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='IP', blank=True),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='IP', blank=True),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='ip_firewall',
            field=models.CharField(max_length=200, null=True, verbose_name='IP Firewall', blank=True),
        ),
    ]
