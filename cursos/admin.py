from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Video, Modulo, Curso, LikeVideo, DeslikeVideo, MarcarVistoVideo

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'modulo', 'visibilidade', 'ordem', 'like', 'arquivo')
    list_display_links = ('nome', 'modulo', 'ordem', 'like', 'arquivo')
    list_editable = ('visibilidade',)
    list_filter = ('modulo', 'visibilidade')
    list_per_page = 10
    # summernote_fields = ('descricao',)
    search_fields = ('nome', 'modulo__nome')
    
admin.site.register(Video, VideoAdmin)

class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso', 'ordem', 'visibilidade')
    list_display_links = ('nome', 'ordem','curso')
    list_editable = ('visibilidade',)
    list_filter = ('curso', 'visibilidade')
    list_per_page = 10
    search_fields = ('nome', 'curso__nome')
    
admin.site.register(Modulo, ModuloAdmin)

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'visibilidade')
    list_display_links = ('nome',)
    list_editable = ('visibilidade',)
    list_filter = ('visibilidade',)
    list_per_page = 10
    search_fields = ('nome',)
    
admin.site.register(Curso, CursoAdmin)

class LikeVideoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'video')
    list_display_links = ('usuario', 'video')
    list_per_page = 10
    search_fields = ('usuario__username', 'video__nome')
    
admin.site.register(LikeVideo, LikeVideoAdmin)

class DeslikeVideoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'video')
    list_display_links = ('usuario', 'video')
    list_per_page = 10
    search_fields = ('usuario__username', 'video__nome')
    
admin.site.register(DeslikeVideo, DeslikeVideoAdmin)

class MarcarVistoVideoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'video', 'modulo')
    list_display_links = ('usuario', 'video', 'modulo')
    list_per_page = 10
    search_fields = ('usuario__username', 'video__nome', 'modulo__nome')
    
admin.site.register(MarcarVistoVideo, MarcarVistoVideoAdmin)

