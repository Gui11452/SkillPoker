from django import template
from liberacao.models import LiberacaoModulos
from cursos.models import Modulo, Video, Curso, MarcarVistoVideo

register = template.Library()

@register.filter(name='formata_slug_string')
def formata_slug_string(nome):
    return nome.replace('_', ' ').replace('-', ' ')


@register.filter(name='formata_numero_video')
def formata_numero_video(ordem):
    ordem = f'0{ordem}. ' if len(str(ordem)) == 1 else f'{ordem}. '
    return ordem


@register.filter(name='length_aulas')
def length_aulas(aulas):
    qtd = len(aulas)
    return f'{qtd} aula' if qtd == 1 else f'{qtd} aulas'


@register.filter(name='formata_aulas')
def formata_aulas(qtd):
    return f'{qtd} aula' if qtd == 1 else f'{qtd} aulas'


@register.filter(name='filtrar_aulas_vistas_1')
def filtrar_aulas_vistas_1(video):
    queryset = MarcarVistoVideo.objects.filter(video=video, modulo=video.modulo)
    return queryset
