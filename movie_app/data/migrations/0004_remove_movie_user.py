# Generated by Django 5.1.6 on 2025-02-15 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_movie_user_alter_movie_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='user',
        ),
    ]
