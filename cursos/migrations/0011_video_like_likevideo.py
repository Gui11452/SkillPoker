# Generated by Django 4.2.6 on 2023-10-29 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cursos', '0010_remove_video_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='like',
            field=models.IntegerField(default=0, verbose_name='Likes'),
        ),
        migrations.CreateModel(
            name='LikeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.video', verbose_name='Vídeo')),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likes',
            },
        ),
    ]
