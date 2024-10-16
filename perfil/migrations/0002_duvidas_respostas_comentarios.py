# Generated by Django 4.2.6 on 2023-10-31 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cursos', '0013_marcarvistovideo_modulo'),
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duvidas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default='', max_length=5000, verbose_name='Texto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.video', verbose_name='Vídeo')),
            ],
            options={
                'verbose_name': 'Duvida',
                'verbose_name_plural': 'Duvidas',
            },
        ),
        migrations.CreateModel(
            name='Respostas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default='', max_length=5000, verbose_name='Texto')),
                ('duvida', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='perfil.duvidas', verbose_name='Resposta')),
            ],
            options={
                'verbose_name': 'Resposta',
                'verbose_name_plural': 'Respostas',
            },
        ),
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default='', max_length=5000, verbose_name='Texto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.video', verbose_name='Vídeo')),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
            },
        ),
    ]
