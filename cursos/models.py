from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


class Curso(models.Model):
    nome = models.SlugField(default='', max_length=1500, verbose_name="Nome", unique=True)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")
    foto = models.ImageField(blank=True, null=True, upload_to='cursos/%Y/%m/%d', verbose_name="Foto")

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.nome

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name="Curso", default=None)
    nome = models.SlugField(default='', max_length=1500, verbose_name="Nome", unique=True)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")
    foto = models.ImageField(blank=True, null=True, upload_to='modulos/%Y/%m/%d', verbose_name="Foto")
    ordem = models.IntegerField(default=1, verbose_name='Ordem')

    class Meta:
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'

    def __str__(self):
        return self.nome

class Video(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, verbose_name="Módulo")
    nome = models.SlugField(default='', max_length=1500, verbose_name="Nome", unique=True)
    arquivo = models.FileField(upload_to="arquivos_videos/%Y/%m/%d/", verbose_name="Arquivo de Apoio", default=None, blank=True, null=True)
    descricao = models.TextField(max_length=10000, verbose_name="Descrição", default=None, blank=True, null=True)
    link = models.URLField(default=None, max_length=2000, verbose_name="Link", blank=True, null=True)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")
    ordem = models.IntegerField(default=1, verbose_name='Ordem')
    like = models.IntegerField(default=0, verbose_name='Likes')
    deslike = models.IntegerField(default=0, verbose_name='Desikes')

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.nome
    

class LikeVideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Vídeo")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f'{self.video} / {self.usuario}'
    

class DeslikeVideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Vídeo")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")

    class Meta:
        verbose_name = 'Deslike'
        verbose_name_plural = 'Deslikes'

    def __str__(self):
        return f'{self.video} / {self.usuario}'
    

class MarcarVistoVideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Vídeo")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, verbose_name="Módulo", default='')

    class Meta:
        verbose_name = 'Marcar Visto Video'
        verbose_name_plural = 'Marcar Visto Video'

    def __str__(self):
        return f'{self.video} / {self.usuario}'