# Edu Station

> autor: Luan da Silva Rodrigues  
> Teste de estágio


## Configuração de ambiente

* #### Ativar o ambiente virtual
	
      # Windows 
      
      C:/diretorio_do_app:
      
      >> cd venv
      >> cd Scripts
      >> activate
      
      # Linux 
      
      /diretorio_do_app:
      
      source venv/bin/activate
      

* #### Ativar o ambiente virtual
		>> (venv) diretorio_do_app: 
		>> py manage.py runserver
		
        System check identified no issues (0 silenced).
		April 10, 2019 - 16:41:50
		Django version 2.2, using settings 'edu_station.settings'
		Starting development server at http://127.0.0.1:8000/
		Quit the server with CTRL-BREAK.
        

* #### No navegador
		
		entrar na url: localhost:8000 ou
        na url retornada pelo terminal (Ex: Starting development server at http://127.0.0.1:8000)
        
* #### Obs
por padrão, somente usuários da direção podem criar outros usuários / turmas / disciplinas, portanto existe um diretor geral, do grupo de direçao:
	
    	usuário : diretor
        senha: senhadono


## Tarefas realizadas

* #### Módulo de direcão

	* Login autorizado somente para usuários da direcao;
	* Navegação nas paginas somente para usuários logados e da direção;
	* Alterar os dados do usuário logado;
	* Deslogar do usuário autal;
	* Visualizar, adicionar, alterar e excluir um usuárido da direção;
	* Visualizar, adicionar, alterar e excluir um docente;
	* Visualizar, adicionar, alterar e excluir um aluno;
	* Visualizar, adicionar, alterar e excluir uma disciplina;
	* Visualizar, adicionar, alterar e  excluir uma turma com seus Docentes vinculados as diciplinas e Alunos vinculados a turma;
	* Emitir boletim do aluno selecionado no menu de "Turma > Ver alunos";


 * #### Módulo de docente
 	* Login autorizado somente para usuários docente;
 	* Navegação nas paginas somente para usuários logados e da direção;
 	* Alterar os dados do usuário logado;
 	* Visualizar as turmas que o docente está vinculado a alguma disciplina;
 	* Visualizar turma selecionada (ver resumo de cada aluno por disciplina ministrada na turma);

* #### Módulo de aluno
 	* Login autorizado somente para usuários aluno;
 	* Navegação nas paginas somente para usuários logados e aluno;
 	* Alterar os dados do usuário logado;
 	* Ver boletim do aluno

