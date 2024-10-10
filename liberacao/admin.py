from django.contrib import admin
from .models import LiberacaoModulos, LiberacaoVideos, LiberacaoGradual, LiberacaoTotal

class LiberacaoModulosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'modulo', 'liberacao')
    list_display_links = ('usuario', 'modulo')
    list_editable = ('liberacao',)
    list_filter = ('modulo', 'usuario')
    list_per_page = 10
    search_fields = ('usuario__username', 'modulo__nome')
    
admin.site.register(LiberacaoModulos, LiberacaoModulosAdmin)

class LiberacaoVideosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'video', 'liberacao')
    list_display_links = ('usuario', 'video')
    list_editable = ('liberacao',)
    list_filter = ('video', 'usuario')
    list_per_page = 10
    search_fields = ('usuario__username', 'video__nome')
    
admin.site.register(LiberacaoVideos, LiberacaoVideosAdmin)

class LiberacaoGradualAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'videos_liberados', 'diferenca_periodo', 'data', 'tempo')
    list_display_links = ('usuario', 'curso', 'videos_liberados', 'diferenca_periodo', 'data', 'tempo')
    list_filter = ('curso', 'usuario', 'data', 'tempo')
    list_per_page = 10
    search_fields = ('usuario__username', 'curso__nome', 'tempo')
    
admin.site.register(LiberacaoGradual, LiberacaoGradualAdmin)

class LiberacaoTotalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'data')
    list_display_links = ('usuario', 'curso', 'data')
    list_filter = ('usuario', 'curso', 'data')
    list_per_page = 10
    search_fields = ('usuario__username', 'curso__nome')
    
admin.site.register(LiberacaoTotal, LiberacaoTotalAdmin)