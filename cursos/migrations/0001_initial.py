# Generated by Django 4.2.6 on 2023-10-18 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=1500, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=1500, verbose_name='Nome')),
                ('curso', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso', verbose_name='Curso')),
            ],
            options={
                'verbose_name': 'Modulo',
                'verbose_name_plural': 'Modulos',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=1500, verbose_name='Nome')),
                ('descricao', models.TextField(default='', max_length=10000, verbose_name='Email')),
                ('link', models.URLField(default='', max_length=2000, verbose_name='Link')),
                ('modulo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cursos.modulo', verbose_name='Módulo')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
        ),
    ]
