# Generated by Django 4.2.6 on 2023-10-31 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0006_alter_duvidas_arquivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentarios',
            name='visibilidade',
            field=models.BooleanField(default=True, verbose_name='Visibilidade'),
        ),
        migrations.AddField(
            model_name='duvidas',
            name='visibilidade',
            field=models.BooleanField(default=True, verbose_name='Visibilidade'),
        ),
        migrations.AddField(
            model_name='respostas',
            name='visibilidade',
            field=models.BooleanField(default=True, verbose_name='Visibilidade'),
        ),
    ]
