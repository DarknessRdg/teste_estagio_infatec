from django.contrib.auth import login as login_django, logout as logout_django, authenticate
from django.contrib.auth.models import User, Group
from .pessoa import Pessoa
from entidades.turma import Turma
from app_edu_station.models import Docente as ModelDocente
from app_edu_station.models import TurmaDisciplina as ModelTurmaDisciplina
from app_edu_station.models import AlunoDisciplina


class Docente(Pessoa):
    def __init__(self, nome, cpf, nascimento, email, user):
        super().__init__(nome, cpf, nascimento, email)
        self.user = user
        self.__set_minhas_turmas()
        self.__set_minhas_disciplinas()

    def __set_minhas_turmas(self):
        self.minhas_turmas = []

        for turma in Turma.get_all():
            self.minhas_turmas.append(
                TurmaQntalunosDisciplinas(turma))

    def __set_minhas_disciplinas(self):
        self.minhas_disciplinas = []

        for turma in self.minhas_turmas:
            id = turma.turma.id
            self.minhas_disciplinas += ModelTurmaDisciplina.objects.filter(turma=id, docente=self.cpf)

    def get_disciplinas_por_turma(self, id_turma):
        lista = []

        for i in ModelTurmaDisciplina.objects.filter(turma=id_turma, docente=self.cpf).order_by('turma'):
            lista.append(i.disciplina)
        return lista

    def get_alunos_disc_por_turma(self, id_turma):
        disciplinas_ministadas = ModelTurmaDisciplina.objects.filter(turma=id_turma, docente=self.cpf).order_by('turma')

        lista = []
        for i in disciplinas_ministadas:
            lista += AlunoDisciplina.objects.filter(turma_disciplina=i).order_by('aluno')

        return lista

    def update(self, nome, cpf, nascimento, email, password=None):
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.email = email
        if password is not None:
            self.user.set_password(password)
        self.save()

    def save(self):
        obj = Docente.get_by_user(username=self.user)
        obj.nome = self.nome
        obj.cpf = self.cpf
        obj.nascimento = self.nascimento
        obj.email = self.email
        obj.save()
        self.user.save()

    def delete(self):
        user = User.objects.get(username=self.user)
        user.delete()

    @staticmethod
    def autentica_login(usuario, senha):
        user = authenticate(username=usuario, password=senha)
        if user is not None:
            return user.groups.filter(name="docente").exists()
        else:
            return False

    @staticmethod
    def login(request):
        username, password = request.POST['username'], request.POST['password']

        if Docente.autentica_login(username, password):
            user = authenticate(username=username, password=password)
            login_django(request, user)
            return True
        else:
            return False

    @staticmethod
    def autentica_sessao(usuario):
        user = User.objects.get(username=usuario)
        if user is not None:
            return user.groups.filter(name="docente").exists()
        else:
            return False

    @staticmethod
    def logout(request):
        logout_django(request)

    @staticmethod
    def get_by_user(username, model=True):
        user = User.objects.get(username=username)
        docente = ModelDocente.objects.get(user=user)

        if model:
            return docente
        else:
            return Docente(docente.nome, docente.cpf, docente.nascimento, docente.email, user)

    @staticmethod
    def get_by_id(pk, model=True):
        docente = ModelDocente.objects.get(cpf=pk)

        if model:
            return docente
        else:
            return Docente(docente.nome, docente.cpf, docente.nascimento, docente.email, docente.user)

    @staticmethod
    def get_all():
        return ModelDocente.objects.all().order_by('nome')

    @staticmethod
    def create_docente(nome, cpf, nascimento, email, password):
        if len(str(cpf)) != 11 and not str(cpf).isnumeric():
            return None
        User.objects.create_user(cpf, email, password, first_name=nome.split()[0])
        user = User.objects.get(username=cpf)

        group = Group.objects.get(name='docente')
        group.user_set.add(user)
        group.save()

        docente = ModelDocente(nome=nome, cpf=cpf, nascimento=nascimento, email=email, user=user)
        docente.save()

        return docente


class TurmaQntalunosDisciplinas:
    def __init__(self, turma):
        if isinstance(turma, int):
            turma = Turma.get_by_id(turma)

        self.turma = turma
        self.quantidade_alunos = 0
        self.disciplinas = []

        self.set_quantidade_alunos()
        self.set_disciplinas()

    def set_quantidade_alunos(self):
        self.quantidade_alunos = len(Turma.get_by_id(self.turma.id, model=False).alunos)

    def set_disciplinas(self):
        self.disciplinas = Turma.get_by_id(self.turma.id, model=False).disciplinas
