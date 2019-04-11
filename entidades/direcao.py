from django.contrib.auth import login as login_django, logout as logout_django, authenticate
from django.contrib.auth.models import User, Group
from .pessoa import Pessoa
from app_edu_station.models import Direcao as ModelDirecao


class Direcao(Pessoa):
    def __init__(self, nome, cpf, nascimento, email, user):
        super().__init__(nome, cpf, nascimento, email)
        self.user = user

    def update(self, nome, cpf, nascimento, email, password=None):
        self.nome = nome
        self.cpf = cpf
        self.nascimento = nascimento
        self.email = email

        if password is not None:
            self.user.set_password(password)
        self.save()

    def save(self):
        obj = Direcao.get_by_user(username=self.user)
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
            return user.groups.filter(name="direcao").exists()
        else:
            return False

    @staticmethod
    def autentica_sessao(usuario):
        user = User.objects.get(username=usuario)
        if user is not None:
            return user.groups.filter(name="direcao").exists()
        else:
            return False

    @staticmethod
    def login(request):
        username, password = request.POST['username'], request.POST['password']

        if Direcao.autentica_login(username, password):
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
        direcao = ModelDirecao.objects.get(user=user)

        if model:
            return direcao
        else:
            return Direcao(direcao.nome, direcao.cpf, direcao.nascimento, direcao.email, user)

    @staticmethod
    def get_by_id(pk, model=True):
        direcao = ModelDirecao.objects.get(cpf=pk)

        if model:
            return direcao
        else:
            return Direcao(direcao.nome, direcao.cpf, direcao.nascimento, direcao.email, direcao.user)


    @staticmethod
    def get_all():
        return ModelDirecao.objects.all().order_by('nome')

    @staticmethod
    def create_direcao(nome, cpf, nascimento, email, password):
        if len(str(cpf)) != 11 and not str(cpf).isnumeric():
            return None
        User.objects.create_user(cpf, email, password, first_name=nome.split()[0])
        user = User.objects.get(username=cpf)

        group = Group.objects.get(name='direcao')
        group.user_set.add(user)
        group.save()

        direcao = ModelDirecao(nome=nome, cpf=cpf, nascimento=nascimento, email=email, user=user)
        direcao.save()

        return direcao
