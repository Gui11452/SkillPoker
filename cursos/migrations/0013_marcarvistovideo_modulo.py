# Generated by Django 4.2.6 on 2023-10-30 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0012_video_deslike_alter_likevideo_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='marcarvistovideo',
            name='modulo',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cursos.modulo', verbose_name='Módulo'),
        ),
    ]
