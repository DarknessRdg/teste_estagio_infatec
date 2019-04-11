from django.contrib.auth import login as login_django, logout as logout_django, authenticate
from django.contrib.auth.models import User, Group
from .pessoa import Pessoa
from app_edu_station.models import Aluno as ModelAlnuo
from app_edu_station.models import AlunoDisciplina, AlunoTurma


class Aluno(Pessoa):
    def __init__(self, nome, cpf, nascimento, email, user):
        super().__init__(nome, cpf, nascimento, email)
        self.user = user
        self.minhas_disciplinas = []
        self.__set_minha_turma()
        self.__set_disciplinas()

    def __set_disciplinas(self):
        aluno = ModelAlnuo.objects.get(cpf=self.cpf)
        self.minhas_disciplinas = AlunoDisciplina.objects.filter(aluno=aluno)

    def __set_minha_turma(self):
        aluno = ModelAlnuo.objects.get(cpf=self.cpf)
        if AlunoTurma.objects.filter(aluno=aluno).exists():
            self.minha_turma = AlunoTurma.objects.get(aluno=aluno).turma
        else:
            self.minha_turma = None

    def update(self, nome, cpf, nascimento, email, password=None):
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.email = email
        if password is not None:
            self.user.set_password(password)
        self.save()

    def save(self):
        obj = Aluno.get_by_user(username=self.user)
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
            return user.groups.filter(name="aluno").exists()
        else:
            return False

    @staticmethod
    def autentica_sessao(usuario):
        user = User.objects.get(username=usuario)
        if user is not None:
            return user.groups.filter(name='aluno').exists()
        else:
            return False

    @staticmethod
    def login(request):
        username, password = request.POST['username'], request.POST['password']

        if Aluno.autentica_login(username, password):
            user = authenticate(username=username, password=password)
            login_django(request, user)
            return True
        else:
            return False

    @staticmethod
    def logout(request):
        logout_django(request)

    @staticmethod
    def get_by_user(username, model=True):
        user = User.objects.get(username=username)
        aluno = ModelAlnuo.objects.get(user=user)

        if model:
            return aluno
        else:
            return Aluno(aluno.nome, aluno.cpf, aluno.nascimento, aluno.email, user)

    @staticmethod
    def get_by_id(pk, model=True):
        aluno = ModelAlnuo.objects.get(cpf=pk)

        if model:
            return aluno
        else:
            return Aluno(aluno.nome, aluno.cpf, aluno.nascimento, aluno.email, aluno.user)

    @staticmethod
    def get_all():
        return ModelAlnuo.objects.all().order_by('nome')

    @staticmethod
    def create_aluno(nome, cpf, nascimento, email, password):
        if len(str(cpf)) != 11 and not str(cpf).isnumeric():
            return None
        User.objects.create_user(cpf, email, password, first_name=nome.split()[0])
        user = User.objects.get(username=cpf)

        group = Group.objects.get(name='aluno')
        group.user_set.add(user)
        group.save()

        direcao = ModelAlnuo(nome=nome, cpf=cpf, nascimento=nascimento, email=email, user=user)
        direcao.save()

        return direcao
