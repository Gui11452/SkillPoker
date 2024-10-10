from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
# from faker import Faker
from .models import Curso, Modulo, Video, LikeVideo, DeslikeVideo, MarcarVistoVideo
from perfil.models import Comentarios, Duvidas, Respostas, Perfil
from liberacao.models import LiberacaoModulos, LiberacaoVideos, LiberacaoGradual, LiberacaoTotal  
from django.contrib.auth.models import User
from django.contrib import messages, auth
import random
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q
# import mercadopago
from pprint import pprint
# from contas.settings import PUBLIC_KEY, ACCESS_TOKEN
from plataforma.settings import DOMINIO
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import HttpResponseBadRequest, HttpResponseServerError
import requests
import json
from datetime import datetime, timedelta
from django.utils import timezone
from pprint import pprint

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')
    

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        messages.error(request, 'O seu usuário não está atrelado a nenhum perfil. Por favor, fale com o suporte!')
        return redirect('logout')
    
    liberando_modulos_apresentacao(request)
    liberando_videos(request)
    liberando_modulos_total(request)

    cursos = Curso.objects.filter(visibilidade=True)

    return render(request, 'dashboard.html', {
        'cursos': cursos,
    })
    
def modulos(request, nome_curso):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('dashboard')
	)
        
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not Curso.objects.filter(visibilidade=True, nome=nome_curso).exists():
        messages.error(request, f'O curso "{nome_curso}" não existe!')
        return redirect(http_referer)
    
    liberando_modulos_apresentacao(request)
    liberando_videos(request)
    liberando_modulos_total(request)
    
    curso = Curso.objects.get(visibilidade=True, nome=nome_curso)
    modulos = Modulo.objects.filter(visibilidade=True, curso=curso).order_by('ordem')
    verificacao = []
    lista_zip = []

    if modulos:
        if not Perfil.objects.filter(usuario=request.user).exists():
            messages.error(request, 'O seu usuário não está atrelado a nenhum perfil. Por favor, fale com o suporte!')
            return redirect('logout')
        
        for modulo in modulos:
            if LiberacaoModulos.objects.filter(usuario=request.user, modulo=modulo, liberacao=True).exists():
                videos = Video.objects.filter(modulo=modulo, visibilidade=True)
                contador = False
                for video in videos:
                    if LiberacaoVideos.objects.filter(video=video, usuario=request.user, liberacao=True).exists():
                        contador = True
                        break
                
                if contador:
                    verificacao.append(True)
                else:
                    verificacao.append(False)
            else:
                verificacao.append(False)

        lista_zip = zip(modulos, verificacao)

    return render(request, 'modulos.html', {
        'curso': curso,
        'lista_zip': lista_zip,
        'modulos': modulos,
    })


def redirecionar_video(request, nome_modulo):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('dashboard')
	)
        
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        modulo = get_object_or_404(Modulo, visibilidade=True, nome=nome_modulo)
    except:
        nome = nome_modulo.replace('_', ' ').replace('-', ' ')
        messages.error(request, f'O módulo "{nome}" não existe!')
        return redirect(http_referer)

    if not Video.objects.filter(visibilidade=True, modulo=modulo).exists():
        nome = nome_modulo.replace('_', ' ').replace('-', ' ')
        messages.error(request, f'O módulo "{nome}" ainda não possui vídeos. Por favor, aguarde!')
        return redirect(http_referer)
    
    videos = Video.objects.filter(visibilidade=True, modulo=modulo).order_by('ordem')

    for _video in videos:
        if LiberacaoVideos.objects.filter(video=_video, usuario=request.user).exists():
            return redirect(f'{DOMINIO}/video/{_video.nome}')

    return redirect(http_referer)


def enviar_comentario(request, id):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('dashboard')
	)

    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method != 'POST':
        return redirect(http_referer)
    
    texto = request.POST.get('comentario')

    if not Video.objects.filter(visibilidade=True, id=id).exists():
        return redirect(http_referer)
    
    video = Video.objects.get(visibilidade=True, id=id)

    comentario = Comentarios.objects.create(usuario=request.user, texto=texto, video=video)
    comentario.save()

    return redirect(http_referer)


def enviar_duvida(request, id):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('dashboard')
	)
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method != 'POST':
        return redirect(http_referer)
    
    texto = request.POST.get('duvida')
    arquivo = request.FILES.get('duvida_imagem')

    if not Video.objects.filter(visibilidade=True, id=id).exists():
        return redirect(http_referer)
    
    video = Video.objects.get(visibilidade=True, id=id)

    duvida = Duvidas.objects.create(usuario=request.user, texto=texto, video=video, arquivo=arquivo)
    duvida.save()

    return redirect(http_referer)


def video(request, nome_video):
    if not request.user.is_authenticated:
        return redirect('login')
    
    liberando_modulos_apresentacao(request)
    liberando_videos(request)
    liberando_modulos_total(request)

    video = get_object_or_404(Video, visibilidade=True, nome=nome_video)
    nome_do_video = nome_video.replace('_', ' ').replace('-', ' ')

    if LiberacaoVideos.objects.filter(video=video, usuario=request.user, liberacao=False).exists():
        return redirect('dashboard')
    
    if not LiberacaoVideos.objects.filter(video=video, usuario=request.user).exists():
        return redirect('dashboard')

    comentarios = Comentarios.objects.filter(video=video, visibilidade=True)

    duvidas = Duvidas.objects.filter(video=video, visibilidade=True)
    respostas = []
    for duvida in duvidas:
        if Respostas.objects.filter(duvida=duvida, visibilidade=True).exists():
            resposta = Respostas.objects.get(duvida=duvida, visibilidade=True)
            respostas.append(resposta)
        else:
            respostas.append(False)

    # duvidas_respostas = zip(duvidas, respostas)

    modulo = video.modulo
    if not modulo.visibilidade:
        return redirect('dashboard')
    nome_modulo = modulo.nome
    curso = video.modulo.curso

    qtd_videos = 0
    qtv_videos_vistos = 0

    indice_video_anterior = 0
    indice_video_posterior = 0

    lista_videos_temporaria = []
    todos_os_modulos = Modulo.objects.filter(curso=curso, visibilidade=True).order_by('ordem')
    for o_modulo in todos_os_modulos:
        todos_os_videos = Video.objects.filter(modulo=o_modulo, visibilidade=True).order_by('ordem')
        for o_video in todos_os_videos:
            if LiberacaoVideos.objects.filter(usuario=request.user, video=o_video, liberacao=True).exists():
                lista_videos_temporaria.append(o_video)

    indice = 0
    while indice < len(lista_videos_temporaria):
        if lista_videos_temporaria[indice] == video:
            if indice == 0:
                indice_video_anterior = lista_videos_temporaria[indice].id
            else:
                indice_video_anterior = lista_videos_temporaria[indice - 1].id
            
            if indice == len(lista_videos_temporaria) - 1:
                indice_video_posterior = lista_videos_temporaria[indice].id
            else:
                indice_video_posterior = lista_videos_temporaria[indice + 1].id
            break
        indice+=1


    """ if not LiberacaoVideos.objects.filter(video=video, usuario=request.user).exists():
        return redirect(f'{DOMINIO}/video/video_anterior_posterior/{indice_video_posterior}') """

    if LiberacaoModulos.objects.filter(liberacao=True, usuario=request.user, modulo=modulo).exists():

        modulos = Modulo.objects.filter(visibilidade=True, curso=curso).order_by('ordem')
        verificacao = []
        lista_zip = []
        lista_videos = []
        dicionario = {}
        dicionario_liberacao_videos = {}
        porcentagem_videos_vistos_modulos = []

        if modulos:
            if not Perfil.objects.filter(usuario=request.user).exists():
                messages.error(request, 'O seu usuário não está atrelado a nenhum perfil. Por favor, fale com o suporte!')
                return redirect('logout')
            
            for moduloo in modulos:
                if LiberacaoModulos.objects.filter(usuario=request.user, modulo=moduloo, liberacao=True).exists():
                    verificacao.append(True)
                else:
                    verificacao.append(False)

            # for modulo, verificar in lista_zip:
            for moduloo in modulos:
                videos = Video.objects.filter(visibilidade=True, modulo=moduloo).order_by('ordem')
                qtd_videos += len(videos)
                lista_videos.append(videos)

                """ if verificar:
                    lista_videos.append(videos)
                else:
                    lista_videos.append([]) """
    
                for videooo in videos:
                    if MarcarVistoVideo.objects.filter(video=videooo, usuario=request.user, modulo=moduloo).exists():
                        dicionario[videooo.nome] = True
                    else:
                        dicionario[videooo.nome] = False

                
                for videoooo in videos:
                    if LiberacaoVideos.objects.filter(video=videoooo, usuario=request.user, liberacao=True).exists():
                        dicionario_liberacao_videos[videoooo.nome] = True
                    else:
                        dicionario_liberacao_videos[videoooo.nome] = False


                _videos_vistos = MarcarVistoVideo.objects.filter(usuario=request.user, modulo=moduloo)

                if len(_videos_vistos) and len(videos):
                    porcentagem_videos_vistos_modulos.append(round(len(_videos_vistos) / len(videos) * 100, 2))
                else:
                    porcentagem_videos_vistos_modulos.append(0)

            # pprint(dicionario)
            lista_zip = zip(modulos, verificacao, lista_videos, porcentagem_videos_vistos_modulos)


        if LikeVideo.objects.filter(video=video, usuario=request.user).exists():
            like_video = LikeVideo.objects.get(video=video, usuario=request.user)
        else:
            like_video = ''

        if DeslikeVideo.objects.filter(video=video, usuario=request.user).exists():
            deslike_video = DeslikeVideo.objects.get(video=video, usuario=request.user)
        else:
            deslike_video = ''
        
        if MarcarVistoVideo.objects.filter(video=video, usuario=request.user, modulo=modulo).exists():
            marcar_visto = MarcarVistoVideo.objects.get(video=video, usuario=request.user, modulo=modulo)
        else:
            marcar_visto = ''

        videos_vistos = MarcarVistoVideo.objects.filter(usuario=request.user)
        qtv_videos_vistos = len(videos_vistos)
        porcentagem = round(qtv_videos_vistos / qtd_videos * 100, 2)

        return render(request, 'video.html', {
            'video': video,
            'lista_zip': lista_zip,
            'nome_modulo': nome_modulo,
            'modulo_': modulo,
            'like_video': like_video,
            'deslike_video': deslike_video,
            'marcar_visto': marcar_visto,
            'qtd_videos': qtd_videos,
            'qtv_videos_vistos': qtv_videos_vistos,
            'porcentagem': porcentagem,
            'dicionario': dicionario,
            'indice_video_anterior': indice_video_anterior,
            'indice_video_posterior': indice_video_posterior,
            'comentarios': comentarios,
            'duvidas_respostas': list(zip(duvidas, respostas)),
            'dicionario_liberacao_videos': dicionario_liberacao_videos,
        })
    else:
        return redirect('dashboard')



def video_anterior_posterior(request, id):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('dashboard')
	)

    if not Video.objects.filter(visibilidade=True, id=id).exists():
        return redirect(http_referer)
    
    video = Video.objects.get(visibilidade=True, id=id)

    if not LiberacaoModulos.objects.filter(liberacao=True, usuario=request.user, modulo=video.modulo).exists():
        return redirect(http_referer)

    nome_video = video.nome

    return redirect(f'{DOMINIO}/video/{nome_video}')


def liberacao_gradual(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('dashboard')
    
    validador = True
    cursos = Curso.objects.filter(visibilidade=True)
    perfis = Perfil.objects.filter(verificacao_email=True, usuario__is_staff=False)
    
    if request.method != 'POST':
        return render(request, 'liberacao_gradual.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    nome_usuario = request.POST.get('usuario')
    nome_curso = request.POST.get('curso')
    tempo = request.POST.get('tempo')

    # print(nome_usuario, nome_curso, tempo)

    if not nome_usuario or not nome_curso or not tempo:
        messages.error(request, 'Os campos não podem ficar em branco!')
        return render(request, 'liberacao_gradual.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    if not Curso.objects.filter(nome=nome_curso).exists():
        messages.error(request, 'Erro, o curso foi excluído. Fale com o suporte!')
        return render(request, 'liberacao_gradual.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    curso = Curso.objects.get(nome=nome_curso)

    if not User.objects.filter(username=nome_usuario).exists():
        messages.error(request, 'Erro, o usuário foi excluído. Fale com o suporte!')
        return render(request, 'liberacao_gradual.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    usuario = User.objects.get(username=nome_usuario)
    
    if LiberacaoGradual.objects.filter(usuario=usuario, curso=curso).exists():
        messages.error(request, 'O usuário escolhido já tem uma liberação programada para esse curso!')
        return render(request, 'liberacao_gradual.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    if LiberacaoTotal.objects.filter(usuario=usuario, curso=curso).exists():
        messages.error(request, 'O usuário escolhido já tem esse curso liberado!')
        return render(request, 'liberacao_total.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    liberacao_gradual = LiberacaoGradual.objects.create(usuario=usuario, curso=curso, tempo=tempo)
    liberacao_gradual.save()

    validador = False
    messages.success(request, f'Liberação do usuário: "{usuario}", no curso: "{curso}" foi realizada com sucesso! Os vídeos serão liberados de forma: "{tempo}"')
    return render(request, 'liberacao_gradual.html', {
        'validador': validador,
    })



def liberando_videos(request):
    # perfis = Perfil.objects.filter(verificacao_email=True, usuario__is_staff=False)
    ajuste = timedelta(hours=3)
    data_atual = timezone.now() - ajuste

    liberacoes_gradual = LiberacaoGradual.objects.all()

    for liberacao in liberacoes_gradual:
        data_registro = liberacao.data - ajuste
        delta = data_atual - data_registro

        if liberacao.tempo == 'Diário':
            escala_tempo = 1
        elif liberacao.tempo == 'Dois Dias':
            escala_tempo = 2
        else:
            escala_tempo = 7


        lista_videos = []
        count = 1
        todos_os_modulos = Modulo.objects.filter(curso=liberacao.curso, visibilidade=True).order_by('ordem')
        for o_modulo in todos_os_modulos:

            if not LiberacaoModulos.objects.filter(usuario=liberacao.usuario, modulo=o_modulo).exists():
                liberacao_modulo = LiberacaoModulos.objects.create(usuario=liberacao.usuario, modulo=o_modulo)
                liberacao_modulo.save()

            todos_os_videos = Video.objects.filter(modulo=o_modulo, visibilidade=True).order_by('ordem')
            for o_video in todos_os_videos:
                 lista_videos.append(o_video)
            
            count+=1

        
        if liberacao.videos_liberados == 0:
            for _video in lista_videos:
                if LiberacaoVideos.objects.filter(usuario=liberacao.usuario, video=_video, liberacao=True).exists():
                    liberacao.videos_liberados += 1
                    # liberacao.diferenca_periodo += escala_tempo
                    liberacao.save()
                else:
                    break
        
        # Liberar vídeos adicionados depois de uma longa liberação gradual - Início
        for i in range(liberacao.videos_liberados):
            try:
                if not LiberacaoVideos.objects.filter(usuario=liberacao.usuario, video=lista_videos[i]).exists():
                    liberacao_video = LiberacaoVideos.objects.create(usuario=liberacao.usuario, video=lista_videos[i], liberacao=True)
                    liberacao_video.save()
            except:
                continue
        # Liberar vídeos adicionados depois de uma longa liberação gradual - Fim
        
        # validador_diferenca = False

        """ user = User.objects.get(username='ggaprogramer')
        user.last_name += f'{delta.days} / {len(lista_videos)} / {liberacao.diferenca_periodo} / {delta.days >= liberacao.diferenca_periodo}  -----'
        user.save() """

        while True:
            if delta.days >= liberacao.diferenca_periodo:
                # Corrigir erro quando o admin faz liberação de vídeo manual no meio de uma liberação gradual - Início
                while True:
                    try:
                        if LiberacaoVideos.objects.filter(usuario=liberacao.usuario, video=lista_videos[liberacao.videos_liberados], liberacao=True).exists():
                            liberacao.videos_liberados += 1
                            liberacao.save()
                        else:
                            liberacao_video = LiberacaoVideos.objects.create(usuario=liberacao.usuario, video=lista_videos[liberacao.videos_liberados], liberacao=True)
                            liberacao_video.save()
                            break
                    except:
                        break
                # Corrigir erro quando o admin faz liberação de vídeo manual no meio de uma liberação gradual - Fim

                liberacao.videos_liberados += 1
                liberacao.diferenca_periodo += escala_tempo
                liberacao.save()
            else:
                # validador_diferenca = True
                break

        """ if validador_diferenca:
            break """



def liberando_modulos_apresentacao(request):
    usuarios = User.objects.all()

    for usuario in usuarios:
    
        if not Curso.objects.filter(visibilidade=True).exists():
            return

        cursos = Curso.objects.filter(visibilidade=True)

        for curso in cursos:
            if not Modulo.objects.filter(visibilidade=True).exists():
                return
            
            if not Modulo.objects.filter(visibilidade=True, curso=curso).exists():
                continue
            modulo = Modulo.objects.filter(visibilidade=True, curso=curso).order_by('ordem').first()

            if not LiberacaoModulos.objects.filter(usuario=usuario, modulo=modulo).exists():
                liberacao_modulo = LiberacaoModulos.objects.create(usuario=usuario, modulo=modulo)
                liberacao_modulo.save()

            if not Video.objects.filter(visibilidade=True).exists():
                return
            
            videos = Video.objects.filter(visibilidade=True, modulo=modulo).order_by('ordem')
            for video in videos:
                if not LiberacaoVideos.objects.filter(usuario=usuario, video=video).exists():
                    liberacao_video = LiberacaoVideos.objects.create(usuario=usuario, video=video)
                    liberacao_video.save()


def liberando_modulos_total(request):
    usuarios = User.objects.all()

    for usuario in usuarios:
    
        if not Curso.objects.filter(visibilidade=True).exists():
            return

        cursos = Curso.objects.filter(visibilidade=True)

        for curso in cursos:
            if LiberacaoTotal.objects.filter(usuario=usuario, curso=curso).exists():

                if not Modulo.objects.filter(visibilidade=True).exists():
                    return
                if not Modulo.objects.filter(visibilidade=True, curso=curso).exists():
                    continue

                modulos = Modulo.objects.filter(visibilidade=True, curso=curso).order_by('ordem')
                for modulo in modulos:

                    if not LiberacaoModulos.objects.filter(usuario=usuario, modulo=modulo).exists():
                        liberacao_modulo = LiberacaoModulos.objects.create(usuario=usuario, modulo=modulo)
                        liberacao_modulo.save()

                    if not Video.objects.filter(visibilidade=True).exists():
                        return
                    
                    videos = Video.objects.filter(visibilidade=True, modulo=modulo).order_by('ordem')
                    for video in videos:
                        if not LiberacaoVideos.objects.filter(usuario=usuario, video=video).exists():
                            liberacao_video = LiberacaoVideos.objects.create(usuario=usuario, video=video)
                            liberacao_video.save()


def liberacao_total(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('dashboard')
    
    validador = True
    cursos = Curso.objects.filter(visibilidade=True)
    perfis = Perfil.objects.filter(verificacao_email=True, usuario__is_staff=False)
    
    if request.method != 'POST':
        return render(request, 'liberacao_total.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    nome_usuario = request.POST.get('usuario')
    nome_curso = request.POST.get('curso')

    # print(nome_usuario, nome_curso, tempo)

    if not nome_usuario or not nome_curso:
        messages.error(request, 'Os campos não podem ficar em branco!')
        return render(request, 'liberacao_total.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    if not Curso.objects.filter(nome=nome_curso, visibilidade=True).exists():
        messages.error(request, 'Erro, o curso foi excluído. Fale com o suporte!')
        return render(request, 'liberacao_total.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    curso = Curso.objects.get(nome=nome_curso, visibilidade=True)

    if not User.objects.filter(username=nome_usuario).exists():
        messages.error(request, 'Erro, o usuário foi excluído. Fale com o suporte!')
        return render(request, 'liberacao_total.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    usuario = User.objects.get(username=nome_usuario)
    
    if LiberacaoGradual.objects.filter(usuario=usuario, curso=curso).exists():
        messages.error(request, 'O usuário escolhido já tem uma liberação programada para esse curso!')
        return render(request, 'liberacao_total.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    if LiberacaoTotal.objects.filter(usuario=usuario, curso=curso).exists():
        messages.error(request, 'O usuário escolhido já tem esse curso liberado!')
        return render(request, 'liberacao_total.html', {
            'cursos': cursos,
            'perfis': perfis,
            'validador': validador,
        })
    
    liberacao_total = LiberacaoTotal.objects.create(usuario=usuario, curso=curso)
    liberacao_total.save()

    todos_os_modulos = Modulo.objects.filter(curso=curso, visibilidade=True).order_by('ordem')
    for modulo in todos_os_modulos:

        if not LiberacaoModulos.objects.filter(usuario=usuario, modulo=modulo).exists():
            liberacao_modulo = LiberacaoModulos.objects.create(usuario=usuario, modulo=modulo)
            liberacao_modulo.save()

        todos_os_videos = Video.objects.filter(modulo=modulo, visibilidade=True).order_by('ordem')
        for video in todos_os_videos:
            if not LiberacaoVideos.objects.filter(usuario=usuario, video=video, liberacao=True).exists():
                liberacao_video = LiberacaoVideos.objects.create(usuario=usuario, video=video, liberacao=True)
                liberacao_video.save()

    validador = False
    messages.success(request, f'Liberação Total do usuário: "{usuario}", no curso: "{curso}" foi realizada com sucesso!')
    return render(request, 'liberacao_total.html', {
        'validador': validador,
    })


def liberacao_video(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('dashboard')
    
    validador = True
    videos = Video.objects.filter(visibilidade=True)
    perfis = Perfil.objects.filter(verificacao_email=True, usuario__is_staff=False)
    
    if request.method != 'POST':
        return render(request, 'liberacao_video.html', {
            'videos': videos,
            'perfis': perfis,
            'validador': validador,
        })
    
    nome_usuario = request.POST.get('usuario')
    nome_video = request.POST.get('video')

    # print(nome_usuario, nome_curso, tempo)

    if not nome_usuario or not nome_video:
        messages.error(request, 'Os campos não podem ficar em branco!')
        return render(request, 'liberacao_video.html', {
            'videos': videos,
            'perfis': perfis,
            'validador': validador,
        })
    
    if not Video.objects.filter(nome=nome_video, visibilidade=True).exists():
        messages.error(request, 'Erro, o vídeo foi excluído. Fale com o suporte!')
        return render(request, 'liberacao_video.html', {
            'videos': videos,
            'perfis': perfis,
            'validador': validador,
        })
    
    video = Video.objects.get(nome=nome_video, visibilidade=True)

    if not User.objects.filter(username=nome_usuario).exists():
        messages.error(request, 'Erro, o usuário foi excluído. Fale com o suporte!')
        return render(request, 'liberacao_video.html', {
            'videos': videos,
            'perfis': perfis,
            'validador': validador,
        })
    
    usuario = User.objects.get(username=nome_usuario)
    
    nome_video = nome_video.replace('_', ' ').replace('-', ' ')

    if LiberacaoVideos.objects.filter(usuario=usuario, video=video).exists():
        messages.error(request, f'O video "{nome_video}" já está liberado para esse usuário!')
        return render(request, 'liberacao_video.html', {
            'videos': videos,
            'perfis': perfis,
            'validador': validador,
        })

    if not LiberacaoVideos.objects.filter(usuario=usuario, video=video, liberacao=True).exists():
        liberacao_video = LiberacaoVideos.objects.create(usuario=usuario, video=video, liberacao=True)
        liberacao_video.save()

        if not LiberacaoModulos.objects.filter(usuario=usuario, modulo=video.modulo, liberacao=True).exists():
            liberacao_modulo = LiberacaoModulos.objects.create(usuario=usuario, modulo=video.modulo, liberacao=True)
            liberacao_modulo.save()

    validador = False
    messages.success(request, f'Liberação do usuário: "{usuario}", no vídeo: "{nome_video}" foi realizada com sucesso!')
    return render(request, 'liberacao_video.html', {
        'validador': validador,
    })


def like(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('dashboard')
	)

    if not Video.objects.filter(id=id).exists():
        return redirect(http_referer)
    
    video = Video.objects.get(id=id)

    if DeslikeVideo.objects.filter(video=video).exists():
        deslike_video = DeslikeVideo.objects.get(video=video, usuario=request.user)
        deslike_video.delete()

        video.deslike -= 1
        video.save()

    if not LikeVideo.objects.filter(video=video).exists():
        like_video = LikeVideo.objects.create(video=video, usuario=request.user)
        like_video.save()

        video.like += 1
        video.save()
    else:
        like_video = LikeVideo.objects.get(video=video, usuario=request.user)
        like_video.delete()

        video.like -= 1
        video.save()


    return redirect(http_referer)


def deslike(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('dashboard')
	)

    if not Video.objects.filter(id=id).exists():
        return redirect(http_referer)
    
    video = Video.objects.get(id=id)

    if LikeVideo.objects.filter(video=video).exists():
        like_video = LikeVideo.objects.get(video=video, usuario=request.user)
        like_video.delete()

        video.like -= 1
        video.save()

    if not DeslikeVideo.objects.filter(video=video).exists():
        deslike_video = DeslikeVideo.objects.create(video=video, usuario=request.user)
        deslike_video.save()

        video.deslike += 1
        video.save()
    else:
        deslike_video = DeslikeVideo.objects.get(video=video, usuario=request.user)
        deslike_video.delete()

        video.deslike -= 1
        video.save()

    return redirect(http_referer)


def marcar_visto(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('dashboard')
	)

    if not Video.objects.filter(id=id).exists():
        return redirect(http_referer)
    
    video = Video.objects.get(id=id)

    if not MarcarVistoVideo.objects.filter(video=video, usuario=request.user, modulo=video.modulo).exists():
        marcar_visto = MarcarVistoVideo.objects.create(video=video, usuario=request.user, modulo=video.modulo)
        marcar_visto.save()
    else:
        marcar_visto = MarcarVistoVideo.objects.get(video=video, usuario=request.user, modulo=video.modulo)
        marcar_visto.delete()

    return redirect(http_referer)


def not_found(request, exception):
    return render(request, 'not_found.html')