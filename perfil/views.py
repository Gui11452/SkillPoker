from django.shortcuts import render, redirect, reverse
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .models import Perfil, RecuperacaoSenha
from cursos.models import Modulo, Curso, Video
from liberacao.models import LiberacaoModulos, LiberacaoVideos
import copy
from django.db import connection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string	
from django.utils.html import strip_tags	
from django.conf import settings
from plataforma.settings import RECAPTCHA_FRONT, RECAPTCHA_BACK
from plataforma.settings import DOMINIO
from pprint import pprint
from django.core.mail import EmailMultiAlternatives	
from django.template.loader import render_to_string								
from django.utils.html import strip_tags			
from django.conf import settings
import random
import requests
import string

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method != 'POST':
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    email = request.POST.get('email')
    senha = request.POST.get('senha')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not Perfil.objects.filter(email=email).exists() or not User.objects.filter(email=email).exists():
        messages.error(request, 'O E-mail informado não está atrelado a nenhuma conta!')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    username = User.objects.get(email=email).username

    user = auth.authenticate(request, username=username, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': RECAPTCHA_BACK,
            'response': recaptcha,
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao se cadastrar! Você é um robô?')
        return render(request, 'login.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    auth.login(request, user)
    
    if Perfil.objects.filter(email=email, verificacao_email=False).exists():
        messages.error(request, 'O seu e-mail ainda não foi verificado.')
        return redirect('perfil')
    else:
        return redirect('dashboard')
    


def logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    auth.logout(request)
    # messages.success(request, 'Você fez o logout com sucesso!')
    return redirect('login')


def registro(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method != 'POST':
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    username = request.POST.get('username')
    email = request.POST.get('email')
    nome = request.POST.get('name')
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')
    recaptcha = request.POST.get('g-recaptcha-response')

    if not email or not nome or not username:
        messages.error(request, 'Nenhum campo pode ficar vazio!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    if Perfil.objects.filter(email=email, verificacao_email=False).exists():
        _perfil = Perfil.objects.filter(email=email, verificacao_email=False).exists()
        messages.error(request, 'Esse e-mail já foi cadastrado, mas ainda não foi confirmado.')
        return redirect(f'{DOMINIO}/perfil/verificacao_email/{_perfil.usuario.username}/')
    
    if len(username) > 8:
        messages.error(request, 'Digite um usuário com 8 caracteres ou menos!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    if senha1 != senha2:
        messages.error(request, 'As senhas precisam ser iguais!')
        return render(request, 'registro.html', {
            # 'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    if len(senha1) < 8:
        messages.error(request, 'A senha precisa ter no mínimo 8 caracteres!')
        return render(request, 'registro.html', {
            # 'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    if len(username) > 20:
        messages.error(request, 'A senha precisa ter no máximo 20 caracteres!')
        return render(request, 'registro.html', {
            # 'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    """ link = f'https://api.usebouncer.com/v1/email/verify?email={email}&timeout=10'
    headers = {
        "Accept": "application/json",
        'x-api-key': KEY_API_USEBOUNCER,
    }
    requisicao = requests.get(link, headers=headers)

    if str(requisicao) != '<Response [200]>':
        messages.error(request, 'No momento não foi possível criar a sua conta. Tente novamente mais tarde!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    status = dict(requisicao.json())['reason']
    if status != 'accepted_email':
        messages.error(request, 'O E-mail informado NÃO existe!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        }) """

    if User.objects.filter(email=email).exists() or Perfil.objects.filter(email=email).exists():
        messages.error(request, 'O E-mail informado já está sendo utilizado!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    if User.objects.filter(username=username).exists():
        messages.error(request, 'O usuário informado já está sendo utilizado!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })
    
    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': RECAPTCHA_BACK,
            'response': recaptcha
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao se cadastrar! Você é um robô?')
        return render(request, 'registro.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    messages.success(request, 'Registrado com sucesso!')

    usuario = User.objects.create_user(email=email, username=username, password=senha1)
    usuario.save()
    perfil = Perfil.objects.create(usuario=usuario, email=email, nome=nome) 
    perfil.save()

    # auth.login(request, usuario)
    return redirect(f'{DOMINIO}/perfil/verificacao_email/{usuario.username}/')


def alterar_dados(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method != 'POST':
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    username = request.POST.get('username')
    """ email = request.POST.get('email') """
    nome = request.POST.get('name')
    recaptcha = request.POST.get('g-recaptcha-response')

    if len(username) > 20:
        messages.error(request, 'Digite um usuário com 20 caracteres ou menos!')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    if not recaptcha:
        messages.error(request, 'Por favor, marque a caixa "Não sou um robô"!')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    recaptcha_request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': RECAPTCHA_BACK,
            'response': recaptcha,
        }
    )

    recaptcha_result = recaptcha_request.json()

    if not recaptcha_result.get('success'):
        messages.error(request, 'Erro ao se cadastrar! Você é um robô?')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    if User.objects.filter(username=username).exists():
        messages.error(request, f'O usuário: "{username}" já está sendo usado.')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        })

    """ if User.objects.filter(email=email).exists() or Perfil.objects.filter(email=email).exists():
        messages.error(request, f'O e-mail: "{email}" já está sendo usado.')
        return render(request, 'alterar_dados.html', {
            'RECAPTCHA_FRONT': RECAPTCHA_FRONT,
        }) """

    
    perfil = Perfil.objects.get(usuario=request.user)
    usuario = User.objects.get(username=request.user.username)

    # perfil.email = email
    perfil.nome = nome
    perfil.save()

    usuario.username = username
    # usuario.email = email
    usuario.save()

    messages.success(request, f'Os seus dados foram alterados com sucesso!')
    return redirect('perfil')


def verificacao_email(request, username):
    http_referer = request.META.get(
		'HTTP_REFERER',
		reverse('dashboard')
	)

    if not User.objects.filter(username=username).exists() or not Perfil.objects.filter(usuario__username=username).exists():
        return redirect('registro')
    
    if Perfil.objects.filter(verificacao_email=True, usuario__username=username).exists():
        messages.success(request, 'O seu e-mail já foi confirmado. Faça login na sua conta.')
        return redirect('logout')

    perfil = Perfil.objects.get(usuario__username=username)

    letras = string.ascii_letters
    digitos = string.digits
    # caracteres = string.punctuation

    geral = letras + digitos
    codigo = ''.join(random.choices(geral, k=50))

    link = f'{DOMINIO}/perfil/confirmacao_email/{codigo}/'

    perfil.codigo = codigo
    perfil.save()

    html_content = render_to_string('email_confirmacao.html', {'link': link, 'nome': perfil.nome})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives('Confirmação de Email - Bem-vindo(a) à SkillPoker!', text_content, 
    settings.EMAIL_HOST_USER, [perfil.usuario.email])
    email.attach_alternative(html_content, 'text/html')
    email.send()

    messages.success(request, f"Para concluir o processo de confirmação e acessar a plataforma, basta acessar o link enviado para o seu e-mail!")
    return render(request, 'confirmacao_email.html', {'username': username})


def confirmacao_email(request, codigo):
    if not Perfil.objects.filter(codigo=codigo).exists():
        return redirect('registro')
    
    perfil = Perfil.objects.get(codigo=codigo)
    perfil.verificacao_email = True
    perfil.save()

    return redirect(f'{DOMINIO}/perfil/liberacao_primeiros_modulos/{perfil.usuario.username}/')


def liberacao_primeiros_modulos(request, username):

    usuario = User.objects.get(username=username)
    
    if not Curso.objects.filter(visibilidade=True).exists():
        messages.error(request, f'Nenhum curso foi cadastrado ainda. Por favor, fale com o suporte!')
        messages.success(request, f'Parabéns {username}, o seu e-mail foi confirmado. Agora, faça login no nosso site e aproveite!')
        return redirect('logout')

    cursos = Curso.objects.filter(visibilidade=True)

    for curso in cursos:
        if not Modulo.objects.filter(visibilidade=True).exists():
            messages.error(request, f'Nenhum módulo de nenhum curso foi cadastrado ainda. Por favor, fale com o suporte!')
            messages.success(request, f'Parabéns {username}, o seu e-mail foi confirmado. Agora, faça login no nosso site e aproveite!')
            return redirect('logout')
        
        if not Modulo.objects.filter(visibilidade=True, curso=curso).exists():
            continue
        modulo = Modulo.objects.filter(visibilidade=True, curso=curso).order_by('ordem').first()

        if not LiberacaoModulos.objects.filter(usuario=usuario, modulo=modulo).exists():
            liberacao_modulo = LiberacaoModulos.objects.create(usuario=usuario, modulo=modulo)
            liberacao_modulo.save()

        if not Video.objects.filter(visibilidade=True).exists():
            messages.error(request, f'Nenhum módulo de nenhum curso possui vídeos ainda. Por favor, fale com o suporte!')
            messages.success(request, f'Parabéns {username}, o seu e-mail foi confirmado. Agora, faça login no nosso site e aproveite!')
            return redirect('logout')
        
        videos = Video.objects.filter(visibilidade=True, modulo=modulo).order_by('ordem')
        for video in videos:
            if not LiberacaoVideos.objects.filter(usuario=usuario, video=video).exists():
                liberacao_video = LiberacaoVideos.objects.create(usuario=usuario, video=video)
                liberacao_video.save()

    messages.success(request, f'Parabéns {username}, o seu e-mail foi confirmado. Agora, faça login no nosso site e aproveite!')
    return redirect('logout')


def esqueceu_senha(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method != 'POST':
        return render(request, 'esqueceu_senha.html')
    
    email = request.POST.get('email')

    if not email:
        messages.error(request, 'O campo abaixo não pode ficar vazio!')
        return render(request, 'esqueceu_senha.html')
    
    if not User.objects.filter(email=email).exists() or not Perfil.objects.filter(email=email, verificacao_email=True).exists():
        messages.error(request, f"O email: '{email}' não está atrelado a nenhum perfil ou o e-mail não foi verificado!")
        return render(request, 'esqueceu_senha.html')
    
    usuario = User.objects.get(email=email)
    perfil = Perfil.objects.get(email=email, verificacao_email=True)

    letras = string.ascii_letters
    digitos = string.digits
    # caracteres = string.punctuation

    geral = letras + digitos
    codigo = ''.join(random.choices(geral, k=50))

    if RecuperacaoSenha.objects.filter(usuario=usuario, recuperacao='pending').exists():
        messages.success(request, f"O seu pedido de recuperação de senha foi renovado. Verifique o novo e-mail enviado para você e troque a sua senha!")

        _recuperacao = RecuperacaoSenha.objects.get(usuario=usuario, recuperacao='pending')
        _recuperacao.delete()
    else:
        messages.success(request, f"O seu pedido de recuperação de senha foi feito com sucesso! Verifique o e-mail enviado para você e troque a sua senha!")

    recuperacao = RecuperacaoSenha.objects.create(usuario=usuario, codigo=codigo)
    recuperacao.save()

    link = f'{DOMINIO}/perfil/recuperar_senha/{codigo}/'

    html_content = render_to_string('email_recuperacao_senha.html', {'link': link, 'nome': perfil.nome})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives('Recuperação de Senha - SkillPoker', text_content, 
    settings.EMAIL_HOST_USER, [usuario.email])
    email.attach_alternative(html_content, 'text/html')
    email.send()

    return render(request, 'esqueceu_senha.html', {
        'validador': True,
    })


def recuperar_senha(request, codigo):
    if not RecuperacaoSenha.objects.filter(recuperacao='pending', codigo=codigo).exists():
        return redirect('esqueceu_senha')
    
    recuperacao = RecuperacaoSenha.objects.get(recuperacao='pending', codigo=codigo)
    user = recuperacao.usuario

    if request.method != 'POST':
        return render(request, 'recuperacao_senha.html', {
            'codigo': codigo,
        })
    
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')

    if not senha1 or not senha2:
        messages.error(request, 'Os campos abaixos não podem ficar vazios!')
        return render(request, 'esqueceu_senha.html', {
            'codigo': codigo,
        })
    
    if senha1 != senha2:
        messages.error(request, 'As senhas precisam ser iguais!')
        return render(request, 'esqueceu_senha.html', {
            'codigo': codigo,
        })

    if len(senha1) < 8:
        messages.error(request, 'A senha não pode ter menos que 8 caracteres!')
        return render(request, 'esqueceu_senha.html', {
            'codigo': codigo,
        })

    user.set_password(senha1)
    auth.logout(request)
    user.save()

    recuperacao.recuperacao = 'approved'
    recuperacao.save()
    
    messages.success(request, f'Olá {user}, a sua senha foi trocada!')
    return redirect('login')


def perfil(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not Perfil.objects.filter(usuario=request.user).exists():
        return redirect('registro')
    
    perfil = Perfil.objects.get(usuario=request.user)

    return render(request, 'perfil.html', {
        'perfil': perfil,
    })


