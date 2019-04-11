from django.contrib.auth.models import User, Group


def criar_grupos():
    direcao = Group.objects.get_or_create(name='direcao')
    aluno = Group.objects.get_or_create(name='aluno')
    docente = Group.objects.get_or_create(name='docente')


def criar_diretor_geral():
    User.objects.create_user('admin', 'admin@admin', 'admin', first_name='admin')
    user = User.objects.get(username='admin')

    group = Group.objects.get(name='direcao')
    group.user_set.add(user)

    group.save()
    user.save()


if __name__ == '__main__':
    criar_grupos()
    criar_diretor_geral()
