from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from app_edu_station.forms import FormAluno
from app_edu_station.views_docente import autenticar_user as autenticar_docente
from app_edu_station.views_direcao import autenticar_user as autenticar_direcao
from entidades.aluno import Aluno


DIRETORIO = 'aluno/'


def autenticar_user(request):
    """
    Autentica se o usuario logado/ou nao na request pertence ao grupo : direcao
        if True:
            permite entrar na view
        else:
            redireciona para paga inicial da aplicacao Edu Station
    """
    if not Aluno.autentica_sessao(request.user):
        messages.error(request, 'usuario nao autorizado')
        return False
    else:
        return True


def login(request):
    if request.POST:
        if Aluno.login(request):
            return redirect('/aluno/')
        else:
            messages.error(request, 'Usuário ou senha inválido.')

    return render(request, DIRETORIO + 'login.html')


@login_required(login_url='login_aluno')
def index(request):
    if not autenticar_user(request):
        return redirect('login_aluno')

    aluno = Aluno.get_by_user(request.user, model=False)
    return render(request, DIRETORIO + 'index.html', {'aluno': aluno})


def alterar_user(request):
    if not autenticar_user(request):
        return redirect('login_aluno')

    docente = Aluno.get_by_user(request.user)
    form = FormAluno(request.POST or None, instance=docente)

    aluno = Aluno.get_by_user(request.user, model=False)

    validacao = ''
    if request.POST:
        if form.is_valid():
            # nao quer altrar sennha
            if request.POST['old_password'] == '':
                form.save()

            # alterar senha
            elif Aluno.autentica_login(request.user, request.POST['old_password']) and \
                    request.POST['new_password'] == request.POST['conf_password']:

                aluno.update(
                    nome=form.cleaned_data['nome'],
                    cpf=form.cleaned_data['cpf'],
                    email=form.cleaned_data['email'],
                    nascimento=form.cleaned_data['nascimento'],
                    password=request.POST['new_password']
                )
            validacao = 'validado'

        else:
            validacao = 'error'
            messages.error(request, 'Error na atualização do usuário. Tente novamente')

    return render(request, DIRETORIO + 'alterar.html', {'form': form, 'validacao': validacao})


@login_required(login_url='login_aluno')
def boletim(request, cpf):
    if not autenticar_user(request) and not autenticar_direcao(request) and not autenticar_docente(request):
        return redirect('login_aluno')

    aluno = Aluno.get_by_id(cpf, model=False)

    return render(request, DIRETORIO + 'boletim.html', {'aluno': aluno})
