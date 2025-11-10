
from admin import manager_alunos, manager_turmas
from user import professor_ops, aluno_ops
from ia import ia_core
from utils.logs import info, error
from rede import cliente, servidor
import threading
import sys

def menu_principal():
    while True:
        print('\n=== Sistema Acadêmico (Prompt) ===')
        print('1. Administrador')
        print('2. Professor')
        print('3. Aluno')
        print('4. Iniciar servidor local (background)')
        print('5. Sair')
        opt = input('Opção: ').strip()
        if opt == '1':
            menu_admin()
        elif opt == '2':
            menu_professor()
        elif opt == '3':
            menu_aluno()
        elif opt == '4':
            threading.Thread(target=servidor.start_server, daemon=True).start()
            print('Servidor iniciado em background.')
        elif opt == '5':
            print('Saindo...'); break
        else:
            print('Opção inválida')

def menu_admin():
    while True:
        print('\n--- Admin ---')
        print('1. Listar alunos')
        print('2. Cadastrar aluno')
        print('3. Voltar')
        opt = input('Opção: ').strip()
        if opt == '1':
            alunos = manager_alunos.listar_alunos()
            for a in alunos:
                print(f"{a['ra']} - {a['nome']} (id:{a['id']})")
        elif opt == '2':
            nome = input('Nome: ')
            ra = input('RA: ')
            email = input('Email: ')
            novo = manager_alunos.cadastrar_aluno(nome, ra, email)
            print('Cadastrado:', novo)
        elif opt == '3':
            return
        else:
            print('Inválido')

def menu_professor():
    while True:
        print('\n--- Professor ---')
        print('1. Lançar atividade')
        print('2. Registrar aula')
        print('3. Voltar')
        opt = input('Opção: ').strip()
        if opt == '1':
            turma = input('Código da turma: ')
            titulo = input('Título: ')
            desc = input('Descrição: ')
            data_ent = input('Data entrega (YYYY-MM-DD): ')
            professor_ops.lancar_atividade(turma,titulo,desc,data_ent)
            print('Atividade lançada.')
        elif opt == '2':
            turma = input('Código da turma: ')
            data = input('Data (YYYY-MM-DD): ')
            conteudo = input('Conteúdo da aula: ')
            professor_ops.registrar_aula(turma,data,conteudo)
            print('Aula registrada.')
        elif opt == '3':
            return
        else:
            print('Inválido')

def menu_aluno():
    while True:
        print('\n--- Aluno ---')
        print('1. Listar atividades por turma')
        print('2. Enviar entrega')
        print('3. Perguntar IA')
        print('4. Voltar')
        opt = input('Opção: ').strip()
        if opt == '1':
            turma = input('Código da turma: ')
            listas = aluno_ops.listar_atividades(turma)
            if not listas:
                print('Sem atividades.')
            for a in listas:
                print(f"ID:{a['id']} - {a['titulo']} (Entrega: {a['data_entrega']})")
        elif opt == '2':
            aid = input('ID da atividade: ')
            aluno_id = input('Seu aluno_id: ')
            ref = input('Referência da entrega (arquivo nome): ')
            aluno_ops.enviar_entrega(aid, aluno_id, ref)
            print('Entrega enviada.')
        elif opt == '3':
            pergunta = input('Pergunta para IA: ')
            print('IA:', ia_core.resposta_simples(pergunta))
        elif opt == '4':
            return
        else:
            print('Inválido')

if __name__ == '__main__':
    try:
        menu_principal()
    except KeyboardInterrupt:
        print('\nEncerrando...')
        sys.exit(0)
