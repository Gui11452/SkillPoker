# Generated by Django 4.2.6 on 2023-10-19 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0009_video_curso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='curso',
        ),
    ]
