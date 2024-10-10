from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),
    path('', views.perfil, name='perfil'),
    path('liberacao_primeiros_modulos/<str:username>/', views.liberacao_primeiros_modulos, name='liberacao_primeiros_modulos'),
    path('esqueceu_senha/', views.esqueceu_senha, name='esqueceu_senha'),
    path('recuperar_senha/<str:codigo>/', views.recuperar_senha, name='recuperar_senha'),
    path('verificacao_email/<str:username>/', views.verificacao_email, name='verificacao_email'),
    path('alterar_dados/', views.alterar_dados, name='alterar_dados'),
    path('confirmacao_email/<str:codigo>/', views.confirmacao_email, name='confirmacao_email'),
]