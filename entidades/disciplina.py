from app_edu_station.models import Disciplina as ModelDisciplina


class Disciplina:
    def __init__(self, id, nome, data_criacao):
        self.id = id
        self.nome = nome
        self.data_criacao = data_criacao

    def save(self):
        model = ModelDisciplina(
            id=self.id,
            nome=self.nome,
            data_criacao=self.data_criacao
        )
        model.save()

    def delete(self):
        model = Disciplina.get_by_id(self.id)
        model.delete()

    @staticmethod
    def get_by_id(pk, model=True):
        model = ModelDisciplina.objects.get(id=pk)

        if model:
            return model
        else:
            return Disciplina(model.id, model.nome, model.data_criacao)

    @staticmethod
    def get_all():
        return ModelDisciplina.objects.all().order_by('nome')
