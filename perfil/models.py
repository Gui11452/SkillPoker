from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from cursos.models import Video
from django.utils import timezone

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário", default=True)
    nome = models.CharField(default=None, max_length=255, verbose_name="Nome")
    email = models.CharField(default=None, max_length=255, verbose_name="Email")
    verificacao_email = models.BooleanField(default=False, verbose_name="Verificou o E-mail?")
    codigo = models.CharField(default='', max_length=2000, verbose_name="Código", blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'{self.nome}'
    

class RecuperacaoSenha(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    codigo = models.CharField(default='', max_length=2000, verbose_name="Código")
    # recuperacao = models.BooleanField(default=False, verbose_name="Foi feita a recuperação?")
    data = models.DateTimeField(verbose_name="Data", default=timezone.now)
    recuperacao = models.CharField(default='pending', max_length=30, verbose_name="Foi feita a recuperação?", 
        choices=[
			("approved", "approved"),
			("pending", "pending"),
			("reject", "reject"),
		])

    class Meta:
        verbose_name = 'Recuperação de Senha'
        verbose_name_plural = 'Recuperação de Senhas'

    def __str__(self):
        return f'{self.usuario} / {self.data}'
    

class Comentarios(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Vídeo")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    texto = models.TextField(default='', max_length=5000, verbose_name="Texto")
    data = models.DateTimeField(verbose_name="Data", default=timezone.now)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'{self.usuario}'
    

class Duvidas(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Vídeo")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    texto = models.TextField(default='', max_length=5000, verbose_name="Texto")
    arquivo = models.FileField(upload_to="duvidas/%Y/%m/%d/", verbose_name="Arquivo", default=None, blank=True, null=True)
    data = models.DateTimeField(verbose_name="Data", default=timezone.now)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")

    class Meta:
        verbose_name = 'Duvida'
        verbose_name_plural = 'Duvidas'

    def __str__(self):
        return f'{self.texto}'
    

class Respostas(models.Model):
    duvida = models.OneToOneField(Duvidas, on_delete=models.CASCADE, verbose_name="Dúvida")
    texto = models.TextField(default='', max_length=5000, verbose_name="Texto")
    data = models.DateTimeField(verbose_name="Data", default=timezone.now)
    visibilidade = models.BooleanField(default=True, verbose_name="Visibilidade")

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'

    def __str__(self):
        return f'{self.id}'