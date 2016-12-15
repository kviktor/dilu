# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=255)),
                ('path', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('short_import', models.CharField(max_length=255)),
                ('docstring', models.TextField()),
                ('code', models.TextField()),
                ('line', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('c', 'class'), ('f', 'function'), ('u', 'unknown')], max_length=1)),
                ('module', models.ForeignKey(related_name='objects', to='dilu.Module')),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='module',
            name='version',
            field=models.ForeignKey(related_name='modules', to='dilu.Version'),
        ),
    ]
