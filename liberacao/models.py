from django.db import models
from django.contrib.auth.models import User
from cursos.models import Video, Curso, Modulo
from django.utils import timezone

class LiberacaoModulos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", default=True)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, verbose_name="Módulo")
    liberacao = models.BooleanField(default=True, verbose_name="Liberação")

    class Meta:
        verbose_name = 'Liberação do Módulo'
        verbose_name_plural = 'Liberação dos Módulos'

    def __str__(self):
        return f'{self.usuario} / {self.modulo}'


class LiberacaoVideos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", default=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Vídeo")
    liberacao = models.BooleanField(default=True, verbose_name="Liberação")

    class Meta:
        verbose_name = 'Liberação do Vídeo'
        verbose_name_plural = 'Liberação dos Vídeos'

    def __str__(self):
        return f'{self.usuario} / {self.video}'
    

class LiberacaoGradual(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", default=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name="Curso")
    videos_liberados = models.IntegerField(default=0, verbose_name='Número de Vídeos Liberados')
    diferenca_periodo = models.IntegerField(default=0, verbose_name='Diferença Período')
    data = models.DateTimeField(verbose_name="Data", default=timezone.now)
    tempo = models.CharField(default='Diário', max_length=30, verbose_name="Tempo de Liberação", 
        choices=[
			("Diário", "Diário"),
			("Dois Dias", "Dois Dias"),
			("Semanal", "Semanal"),
		])

    class Meta:
        verbose_name = 'Liberação Gradual'
        verbose_name_plural = 'Liberação Gradual'

    def __str__(self):
        return f'{self.usuario} / {self.curso}'
    

class LiberacaoTotal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário", default=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name="Curso")
    data = models.DateTimeField(verbose_name="Data", default=timezone.now)

    class Meta:
        verbose_name = 'Liberação Total'
        verbose_name_plural = 'Liberação Total'

    def __str__(self):
        return f'{self.usuario} / {self.curso}'
