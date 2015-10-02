# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_create_model_productionform'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionSource',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=200, null=True)),
                ('observations', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'connection_source',
                'verbose_name_plural': 'ConnectionSources',
            },
        ),
        migrations.CreateModel(
            name='ConnectionTarget',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=200, null=True)),
                ('ip_firewall', models.CharField(max_length=200, null=True)),
                ('observations', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'connection_target',
                'verbose_name_plural': 'ConnectionTargets',
            },
        ),
        migrations.AddField(
            model_name='applicationform',
            name='connection_sources',
            field=models.ManyToManyField(to='app.ConnectionSource', blank=True),
        ),
        migrations.AddField(
            model_name='applicationform',
            name='connection_targets',
            field=models.ManyToManyField(to='app.ConnectionTarget', blank=True),
        ),
        migrations.AddField(
            model_name='productionform',
            name='connection_sources',
            field=models.ManyToManyField(to='app.ConnectionSource', blank=True),
        ),
        migrations.AddField(
            model_name='productionform',
            name='connection_targets',
            field=models.ManyToManyField(to='app.ConnectionTarget', blank=True),
        ),
    ]
