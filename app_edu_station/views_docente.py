from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from app_edu_station.forms import FormDocente, FormAlunoDisciplina
from entidades.docente import Docente
from entidades.turma import Turma


DIRETORIO = 'docente/'


def autenticar_user(request):
    """
    Autentica se o usuario logado/ou nao na request pertence ao grupo : docente
        if True:
            permite entrar na view
        else:
            redireciona para paga inicial da aplicacao Edu Station
    """
    if not Docente.autentica_sessao(request.user):
        messages.error(request, 'usuario nao autorizado')
        return False
    else:
        return True


@login_required(login_url='login_docente')
def index(request):
    """ index do login do docente """
    if not autenticar_user(request):
        return redirect('login_docente')

    docente = Docente.get_by_user(request.user, model=False)

    return render(request, DIRETORIO + 'index.html', {'docente': docente})


def login_docente(request):
    if request.POST:
        if Docente.login(request):
            return redirect('/docente/')
        else:
            messages.error(request, 'Usuário ou senha inválido.')

    return render(request, DIRETORIO + 'login.html')


@login_required(login_url='login_docente')
def alterar_user(request):
    if not autenticar_user(request):
        return redirect('login_docente')

    docente = Docente.get_by_user(request.user)
    form = FormDocente(request.POST or None, instance=docente)

    direcao = Docente.get_by_user(request.user, model=False)

    validacao = ''
    if request.POST:
        if form.is_valid():
            # nao quer altrar sennha
            if request.POST['old_password'] == '':
                form.save()

            # alterar senha
            elif Docente.autentica_login(request.user, request.POST['old_password']) and \
                    request.POST['new_password'] == request.POST['conf_password']:

                direcao.update(
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


@login_required(login_url='login_docente')
def ver_turma(request, id):  # id = id da ta turma
    if not autenticar_user(request):
        return redirect('login_docente')

    turma = Turma.get_by_id(id)
    docente = Docente.get_by_user(request.user, model=False)

    disciplinas = docente.get_disciplinas_por_turma(id)
    alunos = docente.get_alunos_disc_por_turma(id)

    return render(request, DIRETORIO + 'ver_turma.html', {'turma': turma, 'disciplinas': disciplinas, 'alunos': alunos})


@login_required(login_url='login_docente')
def atualizar_medias(request, id_turma, id_disc):  # id = id da ta turma
    if not autenticar_user(request):
        return redirect('login_docente')

    docente = Docente.get_by_user(request.user, model=False)

    alunos = docente.get_alunos_disc_por_turma(id_turma)

    for i in alunos:
        i.nota_1 = str(i.nota_1).replace(',', '.')
        i.nota_2 = str(i.nota_2).replace(',', '.')
        i.nota_recuperacao = str(i.nota_recuperacao).replace(',', '.')

    return render(request, DIRETORIO + 'atualizar_medias.html', {'alunos': alunos})

