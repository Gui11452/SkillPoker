# Generated by Django 4.2.6 on 2023-11-05 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cursos', '0014_video_arquivo'),
        ('liberacao', '0006_liberacaovideos'),
    ]

    operations = [
        migrations.AddField(
            model_name='liberacaovideos',
            name='tempo',
            field=models.CharField(choices=[('Diário', 'Diário'), ('Semanal', 'Semanal'), ('Mensal', 'Mensal')], default='Diário', max_length=30, verbose_name='Tempo de Liberação'),
        ),
        migrations.CreateModel(
            name='LiberacaoGradual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videos_liberados', models.IntegerField(default=0, verbose_name='Número de Vídeos Liberados')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso', verbose_name='Curso')),
                ('usuario', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Liberação Gradual',
                'verbose_name_plural': 'Liberação Gradual',
            },
        ),
    ]
