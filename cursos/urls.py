from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.home, name=''),
    path('modulos/<slug:nome_curso>/', views.modulos, name='modulos'),
    path('redirecionar_video/<slug:nome_modulo>/', views.redirecionar_video, name='redirecionar_video'),
    path('video/<slug:nome_video>/', views.video, name='video'),
    path('video_anterior_posterior/<int:id>/', views.video_anterior_posterior, name='video_anterior_posterior'),
    path('like/<int:id>/', views.like, name='like'),
    path('deslike/<int:id>/', views.deslike, name='deslike'),
    path('marcar_visto/<int:id>/', views.marcar_visto, name='marcar_visto'),
    path('enviar_comentario/<int:id>/', views.enviar_comentario, name='enviar_comentario'),
    path('enviar_duvida/<int:id>/', views.enviar_duvida, name='enviar_duvida'),
    path('liberacao_gradual/', views.liberacao_gradual, name='liberacao_gradual'),
    path('liberacao_total/', views.liberacao_total, name='liberacao_total'),
    path('liberacao_video/', views.liberacao_video, name='liberacao_video'),
    path('liberando_videos/', views.liberando_videos, name='liberando_videos'),
]