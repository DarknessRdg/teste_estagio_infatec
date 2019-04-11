from django.contrib import admin
from .models import Aluno, Direcao, Docente, Turma, Disciplina, TurmaDisciplina, AlunoDisciplina, AlunoTurma


admin.site.register(Aluno)
admin.site.register(Direcao)
admin.site.register(Docente)
admin.site.register(Turma)
admin.site.register(Disciplina)
admin.site.register(TurmaDisciplina)
admin.site.register(AlunoDisciplina)
admin.site.register(AlunoTurma)
