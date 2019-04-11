from django import forms

from .models import Direcao, Docente, Aluno, Disciplina, Turma, AlunoDisciplina


class FormDirecao(forms.ModelForm):

    class Meta:
        model = Direcao
        fields = ['nome', 'cpf', 'nascimento', 'email']


class FormDocente(forms.ModelForm):

    class Meta:
        model = Docente
        fields = ['nome', 'cpf', 'nascimento', 'email']


class FormAluno(forms.ModelForm):

    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'nascimento', 'email']


class FormDisciplina(forms.ModelForm):

    class Meta:
        model = Disciplina
        fields = ['nome', 'data_criacao']


class FormTurma(forms.ModelForm):

    class Meta:
        model = Turma
        fields = ['nome', 'ano', 'data_criacao']


class FormAlunoDisciplina(forms.ModelForm):
    class Meta:
        model = AlunoDisciplina
        fields = ['aluno', 'nota_1', 'nota_2', 'nota_recuperacao']
