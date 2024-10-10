from django.contrib import admin
from .models import Perfil, Duvidas, Respostas, Comentarios, RecuperacaoSenha

class PerfilAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'nome', 'email', 'verificacao_email')
	list_display_links = ('usuario', 'nome', 'email', 'verificacao_email')
	list_filter = ('verificacao_email',)
	list_per_page = 10
	search_fields = ('usuario__username', 'nome', 'email', 'verificacao_email')

admin.site.register(Perfil, PerfilAdmin)


class RecuperacaoSenhaAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'codigo', 'data', 'recuperacao')
	list_display = ('usuario', 'codigo', 'data', 'recuperacao')
	list_filter = ('data',)
	list_per_page = 10
	search_fields = ('usuario__username',)

admin.site.register(RecuperacaoSenha, RecuperacaoSenhaAdmin)


class DuvidasAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'video', 'texto', 'arquivo', 'data', 'visibilidade')
	list_display_links = ('usuario', 'video', 'texto', 'arquivo', 'data')
	list_filter = ('data',)
	list_editable = ('visibilidade',)
	list_per_page = 10
	search_fields = ('usuario__username', 'video.nome', 'texto')

admin.site.register(Duvidas, DuvidasAdmin)

class ComentariosAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'video', 'texto', 'data', 'visibilidade')
	list_display_links = ('usuario', 'video', 'texto', 'data')
	list_filter = ('data',)
	list_editable = ('visibilidade',)
	list_per_page = 10
	search_fields = ('usuario__username', 'video.nome', 'texto')

admin.site.register(Comentarios, ComentariosAdmin)

class RespostasAdmin(admin.ModelAdmin):
	list_display = ('duvida', 'texto', 'data', 'visibilidade')
	list_display_links = ('duvida', 'texto', 'data')
	list_filter = ('data',)
	list_editable = ('visibilidade',)
	list_per_page = 10
	search_fields = ('usuario__username', 'texto')

admin.site.register(Respostas, RespostasAdmin)
