# Generated by Django 3.2.2 on 2021-05-11 22:00

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicalsingleviewapi', '0002_rename_contributor_musicalwork_contributors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicalwork',
            name='contributors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None),
        ),
    ]