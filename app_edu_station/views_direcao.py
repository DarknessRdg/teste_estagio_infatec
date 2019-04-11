"""
    Todas as views são referentes a pagina de login/uso da Direcao;
        ex: index refere-se a pagina principal da direcao, o menu com
                'docente', 'aluno', 'direcao', 'disciplina' e 'turma'
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from entidades.direcao import Direcao
from entidades.aluno import Aluno
from entidades.docente import Docente
from entidades.disciplina import Disciplina
from entidades.turma import Turma
from .forms import FormDirecao, FormDocente, FormAluno, FormDisciplina, FormTurma


DIRETORIO = 'direcao/'


def autenticar_user(request):
    """
    Autentica se o usuario logado/ou nao na request pertence ao grupo : direcao
        if True:
            permite entrar na view
        else:
            redireciona para paga inicial da aplicacao Edu Station
    """
    if not Direcao.autentica_sessao(request.user):
        messages.error(request, 'usuario nao autorizado')
        return False
    else:
        return True


# views direcao /
def login_direcao(request):
    if request.POST:
        usuario = request.POST['username']
        senha = request.POST['password']

        if Direcao.autentica_login(usuario, senha):
            Direcao.login(request)
            return redirect('/direcao/')
        else:
            messages.error(request, 'Usuário ou senha inválido.')

    return render(request, DIRETORIO + 'login.html')


@login_required(login_url='login_direcao')
def index(request):
    """ index do login de direcao """
    if not autenticar_user(request):
        return redirect('login_direcao')

    if request.user.is_authenticated:
        return render(request, DIRETORIO + '/index.html')


@login_required(login_url='login_direcao')
def alterar_direcao(request):
    """ Altera os dados do usuario logado na pagina direcao """
    if not autenticar_user(request):
        return redirect('login_direcao')

    direcao = Direcao.get_by_user(request.user, model=False)

    instancia = Direcao.get_by_user(request.user)
    form = FormDirecao(request.POST or None, instance=instancia)

    validacao = ''
    if request.POST:
        if form.is_valid():
            # nao quer altrar sennha
            if request.POST['old_password'] == '':
                form.save()

            # alterar senha
            elif Direcao.autentica_login(request.user, request.POST['old_password']) and \
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


# Views direcao / direcao
@login_required(login_url='login_direcao')
def direcao(request):
    """ view index da pagina de controle de diretores (listagem de direcao) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    direcao = Direcao.get_all()
    return render(request, DIRETORIO + 'direcao.html', {'direcao': direcao})


@login_required(login_url='login_direcao')
def add_direcao(request):
    """ view da pagina de adicionar direcao (botao + da pagina de listagem de direcao) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    form = FormDirecao(request.POST or None)
    validacao = ''
    if request.POST:
        if form.is_valid():
            if request.POST['cpf'].isnumeric() and request.POST['password'] == request.POST['conf_password']:
                criado = Direcao.create_direcao(
                    nome=form.cleaned_data['nome'],
                    cpf=form.cleaned_data['cpf'],
                    email=form.cleaned_data['email'],
                    nascimento=form.cleaned_data['nascimento'],
                    password=request.POST['password']
                )

                if criado is None:  # error na criacao
                    validacao = 'error'
                    messages.error(request, 'Error na criação do usuário. Tente novamente')
                else:
                    validacao = 'validado'
                    form = FormDocente()
                    return redirect('/direcao/direcao/')
            else:
                validacao = 'error'
                messages.error(request, 'Informe um cpf válido! (apenas números)')
        else:
            validacao = 'error'
            messages.error(request, 'Error na criação do usuário. Tente novamente')

    return render(request, DIRETORIO + 'add_direcao.html', {'form': form, 'validacao': validacao})


def direcao_alterar_direcao(request, pk):
    """ view da pagina de alterar um usuario da direcao (link alterar da listagem de direcao) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    isinstance = Direcao.get_by_id(pk)
    form = FormDirecao(request.POST or None, instance=isinstance)

    validacao = ''
    if request.POST:
        if form.is_valid():
            form.save()
            validacao = 'validado'
            return redirect('/direcao/direcao/')
        else:
            validacao = 'error'
            messages.error(request, 'Error na atualização do usuário. Tente novamente')

    return render(request, DIRETORIO + 'alterar_direcao.html', {'form': form, 'validacao': validacao})


@login_required(login_url='login_direcao')
def excluir_direcao(request, pk):
    """ view da pagina de excluir um usuario da direcao (link excluir da listagem de direcao) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    Direcao.get_by_id(pk, model=False).delete()
    return redirect('/direcao/direcao/')


# Views de docente da direcao
@login_required(login_url='login_direcao')
def docente(request):
    """ view index da pagina de controle de docentes (listagem de docentes) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    docentes = Docente.get_all()
    return render(request, DIRETORIO + 'docente.html', {'docentes': docentes})


@login_required(login_url='login_direcao')
def alterar_docente(request, pk):
    """ view da pagina de alterar um docente (link alterar da listagem de docente) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    isinstance = Docente.get_by_id(pk)
    form = FormDocente(request.POST or None, instance=isinstance)

    validacao = ''
    if request.POST:
        if form.is_valid():
            form.save()
            validacao = 'validado'
            return redirect('/direcao/docente/')
        else:
            validacao = 'error'
            messages.error(request, 'Error na atualização do usuário. Tente novamente')

    return render(request, DIRETORIO + 'alterar_docente.html', {'form': form, 'validacao': validacao})


@login_required(login_url='login_direcao')
def add_docente(request):
    """ view da pagina de adicionar um docente (botao + da listagem de docente) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    form = FormDocente(request.POST or None)
    validacao = ''
    if request.POST:
        if form.is_valid():
            if request.POST['cpf'].isnumeric():
                criado = Docente.create_docente(
                    nome=form.cleaned_data['nome'],
                    cpf=form.cleaned_data['cpf'],
                    email=form.cleaned_data['email'],
                    nascimento=form.cleaned_data['nascimento'],
                    password='S3NH4NOV4'
                )

                if criado is None:  # error na criacao
                    validacao = 'error'
                    messages.error(request, 'Error na criação do usuário. Tente novamente')
                else:
                    validacao = 'validado'
                    form = FormDocente()
                    return redirect('/direcao/docente/')
            else:
                validacao = 'error'
                messages.error(request, 'Informe um cpf válido! (apenas números)')
        else:
            validacao = 'error'
            messages.error(request, 'Error na criação do usuário. Tente novamente')

    return render(request, DIRETORIO + 'add_docente.html', {'form': form, 'validacao': validacao})


@login_required(login_url='login_direcao')
def excluir_docente(request, pk):
    """ view da pagina de excluir um docente (link excluir da listagem de docente) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    Docente.get_by_id(pk, model=False).delete()
    return redirect('/direcao/docente/')


# Views direcao / aluno
@login_required(login_url='login_direcao')
def aluno(request):
    """ view index da pagina de controle de alunos (listagem de alunos) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    alunos = Aluno.get_all()
    return render(request, DIRETORIO + 'aluno.html', {'alunos': alunos})


@login_required(login_url='login_direcao')
def add_aluno(request):
    """ view da pagina de adicionar um aluno (botao + da listagem de aluno) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    form = FormAluno(request.POST or None)
    validacao = ''
    if request.POST:
        if form.is_valid():
            if request.POST['cpf'].isnumeric():
                criado = Aluno.create_aluno(
                    nome=form.cleaned_data['nome'],
                    cpf=form.cleaned_data['cpf'],
                    email=form.cleaned_data['email'],
                    nascimento=form.cleaned_data['nascimento'],
                    password='S3NH4NOV4'
                )

                if criado is None:  # error na criacao
                    validacao = 'error'
                    messages.error(request, 'Error na criação do usuário. Tente novamente')
                else:
                    validacao = 'validado'
                    form = FormDocente()
                    return redirect('/direcao/aluno/')
            else:  # cpf nao possuim somente numeros
                validacao = 'error'
                messages.error(request, 'Informe um cpf válido! (apenas números)')
        else:
            validacao = 'error'
            messages.error(request, 'Error na criação do usuário. Tente novamente')

    return render(request, DIRETORIO + 'add_aluno.html', {'form': form, 'validacao': validacao})


@login_required(login_url='login_direcao')
def alterar_aluno(request, pk):
    """ view da pagina de alterar um aluno (link alterar da listagem de aluno) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    instancia = Aluno.get_by_id(pk)
    form = FormAluno(request.POST or None, instance=instancia)

    validacao = ''
    if request.POST:
        if form.is_valid():
            form.save()
            validacao = 'validado'
            return redirect('/direcao/aluno/')
        else:
            validacao = 'error'
            messages.error(request, 'Error na atualização do usuário. Tente novamente')

    return render(request, DIRETORIO + 'alterar_aluno.html', {'form': form, 'validacao': validacao})


@login_required(login_url='login_direcao')
def excluir_aluno(request, pk):
    """ view da pagina de excluir um aluno (link excluir da listagem de aluno) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    Aluno.get_by_id(pk, model=False).delete()
    return redirect('/direcao/aluno/')


# Views direcao / aluno
@login_required(login_url='login_direcao')
def disciplina(request):
    """ view index da pagina de controle de diretores (listagem de direcao) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    disciplinas = Disciplina.get_all()
    return render(request, DIRETORIO + 'disciplina.html', {'disciplinas': disciplinas})


@login_required(login_url='login_direcao')
def add_disciplina(request):
    """ view da pagina de adicionar uma disciplina (botao + da listagem de disciplina) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    form = FormDisciplina(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('/direcao/disciplina/')
        else:
            messages.error(request, 'Error ao criar disciplina')

    return render(request, DIRETORIO + 'add_disciplina.html', {'form': form})


@login_required(login_url='login_direcao')
def alterar_disciplina(request, id):
    """ view da pagina de alterar uma disciplina (link alterar da listagem de disciplina) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    instancia = Disciplina.get_by_id(id)
    form = FormDisciplina(request.POST or None, instance=instancia)

    validacao = ''
    if request.POST:
        if form.is_valid():
            form.save()
            validacao = 'validado'
            return redirect('/direcao/disciplina/')
        else:
            validacao = 'error'
            messages.error(request, 'Error na atualização da disciplina. Tente novamente')

    return render(request, DIRETORIO + 'alterar_disciplina.html', {'form': form, 'validacao': validacao})


@login_required(login_url='login_direcao')
def excluir_disciplina(request, id):
    """ view da pagina de excluir uma disciplina (link excluir da listagem de disciplina) """
    if not autenticar_user(request):
        return redirect('login_direcao')

    Disciplina.get_by_id(id, model=False).delete()
    return redirect('/direcao/disciplina/')


@login_required(login_url='login_direcao')
def turma(request):
    turmas = Turma.get_all()
    turmas_disc = Turma.get_turma_disciplina()
    alunos = Turma.get_aluno_turma()

    for i in alunos:
        print(i.aluno, i.turma)

    return render(request, DIRETORIO + 'turma.html', {
                                                        'turmas': turmas,
                                                        'alunos': alunos,
                                                        'turma_disc': turmas_disc
                                                    })


@login_required(login_url='login_direcao')
def excluir_turma(request, id):
    if not autenticar_user(request):
        return redirect('login_direcao')

    Turma.get_by_id(id).delete()
    return redirect('/direcao/turma/')


@login_required(login_url='login_direcao')
def add_turma(request):
    if not autenticar_user(request):
        return redirect('login_direcao')

    disciplinas = Disciplina.get_all()
    docentes = Docente.get_all()
    alunos = Aluno.get_all()
    form = FormTurma(request.POST or None)
    if request.POST:
        if form.is_valid():
            turma_nova = form.save()

            lista_de_turmas_disciplinas_novas = []
            for docente in docentes:
                cpf = docente.cpf

                for disciplina in disciplinas:
                    id_ = str(disciplina.id)
                    if request.POST.get(cpf + ';' + id_) is not None:
                        turma_dic = Turma.add_turma_disc(turma_nova.id, cpf, disciplina.id)

                        lista_de_turmas_disciplinas_novas.append(turma_dic)

            for aluno in alunos:
                cpf = aluno.cpf
                if request.POST.get(cpf) is not None:
                    for disciplina in lista_de_turmas_disciplinas_novas:
                        Turma.add_aluno_disc(cpf, disciplina.id)

        else:
            messages.error(request, 'Error na criação da turma')

        return redirect('/direcao/turma/')

    return render(request, DIRETORIO + 'add_turma.html',
                  {'form': form,
                   'disciplinas': disciplinas,
                   'docentes': docentes,
                   'alunos': alunos
                   })
