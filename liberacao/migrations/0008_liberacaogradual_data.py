# Generated by Django 4.2.6 on 2023-11-05 18:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('liberacao', '0007_liberacaovideos_tempo_liberacaogradual'),
    ]

    operations = [
        migrations.AddField(
            model_name='liberacaogradual',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data'),
        ),
    ]
