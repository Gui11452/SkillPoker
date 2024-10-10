# Generated by Django 4.2.6 on 2023-10-29 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cursos', '0011_video_like_likevideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='deslike',
            field=models.IntegerField(default=0, verbose_name='Desikes'),
        ),
        migrations.AlterField(
            model_name='likevideo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.CreateModel(
            name='MarcarVistoVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.video', verbose_name='Vídeo')),
            ],
            options={
                'verbose_name': 'Marcar Visto Video',
                'verbose_name_plural': 'Marcar Visto Video',
            },
        ),
        migrations.CreateModel(
            name='DeslikeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.video', verbose_name='Vídeo')),
            ],
            options={
                'verbose_name': 'Deslike',
                'verbose_name_plural': 'Deslikes',
            },
        ),
    ]
