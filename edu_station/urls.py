"""edu_station URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path

import app_edu_station.views_direcao as direcao
import app_edu_station.views_docente as docente
import app_edu_station.views_aluno as aluno
import app_edu_station.views as root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root.index, name='index'),
    path('user/logout', root.user_logout, name='user_logout'),
]

url_direcao = [
    # url da direcao
    path('direcao/', direcao.index, name='direcao'),
    path('login_direcao/', direcao.login_direcao, name='login_direcao'),
    path('alterar_direcao/', direcao.alterar_direcao, name='alterar_direcao'),

    # url da direcao / direcao
    path('direcao/direcao/', direcao.direcao, name='direcao_direcao'),
    path('direcao/direcao/add/', direcao.add_direcao, name='direcao_add_direcao'),
    path('direcao/direcao/alterar/<str:pk>/', direcao.direcao_alterar_direcao, name='direcao_alterar_direcao'),
    path('direcao/direcao/excluir/<str:pk>/', direcao.excluir_direcao, name='direcao_excluir_direcao'),

    # url da direcao / docente
    path('direcao/docente/', direcao.docente, name='direcao_docente'),
    path('direcao/docente/add/', direcao.add_docente, name='add_docente'),
    path('direcao/docente/alterar/<str:pk>/', direcao.alterar_docente, name='direcao_alterar_docente'),
    path('direcao/docente/excluir/<str:pk>/', direcao.excluir_docente, name='direcao_excluir_docente'),

    # url da direcao / aluno
    path('direcao/aluno/', direcao.aluno, name='direcao_aluno'),
    path('direcao/aluno/add/', direcao.add_aluno, name='direcao_add_aluno'),
    path('direcao/aluno/alterar/<str:pk>/', direcao.alterar_aluno, name='direcao_alterar_aluno'),
    path('direcao/aluno/excluir/<str:pk>/', direcao.excluir_aluno, name='direcao_excluir_aluno'),

    # url da direcao / disciplina
    path('direcao/disciplina/', direcao.disciplina, name='direcao_disciplina'),
    path('direcao/disciplina/add', direcao.add_disciplina, name='direcao_add_disciplina'),
    path('direcao/disciplina/alterar/<int:id>', direcao.alterar_disciplina, name='direcao_alterar_disciplina'),
    path('direcao/disciplina/excluir/<int:id>', direcao.excluir_disciplina, name='direcao_excluir_disciplina'),

    # url da direcao / turma
    path('direcao/turma/', direcao.turma, name='direcao_turma'),
    path('direcao/turma/add', direcao.add_turma, name='add_turma'),
    path('direcao/turma/excluir/<int:id>', direcao.excluir_turma, name='direcao_excluir_turma'),

]

url_docente = [
    path('docente/', docente.index, name='docente'),
    path('login_docente/', docente.login_docente, name='login_docente'),
    path('docente/alterar/', docente.alterar_user, name='alterar_docente'),
    path('docente/ver_turma/<int:id>', docente.ver_turma, name='docente_ver_turma'),
    path('docente/altualizar_medias/<int:id_turma>/<int:id_disc>', docente.atualizar_medias, name='atualizar_medias'),
]

url_aluno = [
    path('aluno/', aluno.index, name='aluno'),
    path('login_aluno/', aluno.login, name='login_aluno'),
    path('aluno/alterar/', aluno.alterar_user, name='alterar_aluno'),
    path('aluno/boletim/<str:cpf>/', aluno.boletim, name='boletim'),
]

urlpatterns += url_aluno + url_direcao + url_docente
