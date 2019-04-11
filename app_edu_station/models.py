from django.db import models
from django.contrib.auth.models import User


class Direcao(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100, blank=False, null=False)
    nascimento = models.DateField(blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nome.title())


class Docente(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=100, blank=False, null=False)
    nascimento = models.DateField(blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nome.title())


class Turma(models.Model):
    nome = models.CharField(max_length=10, blank=False, null=False)
    ano = models.PositiveIntegerField(blank=False, null=False)
    data_criacao = models.DateField(blank=False, null=False)
    turma_ativa = models.BooleanField(default=True)  # campo para verificar se a turma ainda permance ativa(tendo aulas)

    def __str__(self):
        return '{}'.format(self.nome)


class Aluno(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100, blank=False, null=False)
    nascimento = models.DateField(blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nome.title())


class Disciplina(models.Model):
    nome = models.CharField(max_length=20, unique=True, blank=False, null=False)
    data_criacao = models.DateField(blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nome)


class TurmaDisciplina(models.Model):
    """
        Relação N para N entra turma, docente e disciplina;
    """

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, blank=False, null=False)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, blank=False, null=False)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return 'Tuma: {}; Disciplina: {}'.format(self.turma, self.disciplina)


class AlunoDisciplina(models.Model):
    """
        Relacao N para N entra as tablelas Aluno e TURMAR_DISCIPLINA

        precisao das notas:
            2 casas decimais;
            3  casas fracionarias.

        Caso as notas estejam nulas, significa zero
    """

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, blank=False, null=False)
    turma_disciplina = models.ForeignKey(TurmaDisciplina, on_delete=models.CASCADE, blank=False, null=False)
    nota_1 = models.DecimalField(max_digits=5, decimal_places=2, default=00.000)
    nota_2 = models.DecimalField(max_digits=5, decimal_places=2, default=00.000)
    media = models.DecimalField(max_digits=5, decimal_places=2, default=00.000)
    aprovado = models.BooleanField(default=False)
    nota_recuperacao = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '{} - Disciplina: {}'.format(self.aluno, self.turma_disciplina)


class AlunoTurma(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return 'Aluno: {}; Turma: {}'.format(self.aluno, self.turma)
