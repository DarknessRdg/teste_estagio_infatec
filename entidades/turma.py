from app_edu_station.models import Turma as ModelTurma
from app_edu_station.models import Docente as ModelDocente
from app_edu_station.models import TurmaDisciplina, AlunoDisciplina, AlunoTurma
from entidades.disciplina import Disciplina
from entidades.aluno import Aluno


class Turma:
    def __init__(self, id, nome, ano, data_criacao):
        self.id = id
        self.nome = nome
        self.ano = ano
        self.data_criacao = data_criacao
        self.alunos = []
        self.disciplinas = []
        self.__set_alunos_da_turma()
        self.__set_disciplinas_da_turma()

    def __set_disciplinas_da_turma(self):
        turma_disc = TurmaDisciplina.objects.all()

        for relacao in turma_disc:
            if self.id == relacao.turma.id:
                if relacao.disciplina not in self.disciplinas:
                    self.disciplinas.append(relacao.disciplina)

    def __set_alunos_da_turma(self):

        turma_disc = AlunoDisciplina.objects.all()

        for relacao in turma_disc:
            if self.id == relacao.turma_disciplina.turma.id:
                if relacao.aluno not in self.alunos:
                    self.alunos.append(relacao.aluno)

    def delete(self):
        model = Turma.get_by_id(self.id)
        model.delete()


    @staticmethod
    def get_all():
        return ModelTurma.objects.all()

    @staticmethod
    def get_turma_disciplina():
        return TurmaDisciplina.objects.all()

    @staticmethod
    def get_aluno_disciplina():
        return AlunoDisciplina.objects.all()

    @staticmethod
    def get_aluno_turma():
        return AlunoTurma.objects.all()

    @staticmethod
    def get_alunos():
        return AlunoDisciplina.objects.all()

    @staticmethod
    def get_by_id(id, model=True):
        turma = ModelTurma.objects.get(id=id)

        if model:
            return turma
        else:
            return Turma(turma.id, turma.nome, turma.ano, turma.data_criacao)

    @staticmethod
    def add_turma_disc(turma, cpf_docente, id_disiplina):
        docente = ModelDocente.objects.get(cpf=cpf_docente)
        disciplina = Disciplina.get_by_id(id_disiplina)
        _turma = Turma.get_by_id(turma)

        nova = TurmaDisciplina(turma=_turma, docente=docente, disciplina=disciplina)
        nova.save()

        return nova

    @staticmethod
    def add_aluno_disc(cpf_aluno, id_turma_dis):
        aluno = Aluno.get_by_id(cpf_aluno)
        turma_disc = TurmaDisciplina.objects.get(id=id_turma_dis)

        if not AlunoTurma.objects.filter(aluno=aluno, turma=turma_disc.turma).exists():
            aluno_turma = AlunoTurma(aluno=aluno, turma=turma_disc.turma)
            aluno_turma.save()

        novo = AlunoDisciplina(aluno=aluno, turma_disciplina=turma_disc)
        novo.save()
        return novo
