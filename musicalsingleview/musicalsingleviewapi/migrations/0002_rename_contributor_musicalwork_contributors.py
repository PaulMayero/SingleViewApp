# Generated by Django 3.2.2 on 2021-05-11 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicalsingleviewapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='musicalwork',
            old_name='contributor',
            new_name='contributors',
        ),
    ]
