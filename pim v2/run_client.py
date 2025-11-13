import socket, json, os, sys
from getpass import getpass
SERVER = ('127.0.0.1',9001)
def send(msg):
    try:
        s = socket.socket(); s.connect(SERVER); s.send(json.dumps(msg).encode('utf-8')); data=s.recv(10_000_000); s.close(); return json.loads(data.decode('utf-8'))
    except Exception as e:
        return {'status':'error','msg':str(e)}
def input_hidden(prompt='Senha: '):
    try: return getpass(prompt)
    except: return input(prompt)
def register_aluno_flow():
    nome = input('Nome: '); email = input('Email: '); nascimento = input('Nascimento YYYY-MM-DD: '); genero = input('Genero: ')
    while True:
        s = input_hidden('Senha: '); s2 = input_hidden('Confirmar: ')
        if s!=s2: print('Nao conferem.'); continue
        break
    # send to server by creating DB entry via separate setup (server here doesn't handle register); for demo we just save locally by asking admin to run setup_db
    print('Registro local - para demo, rode setup_db.py previamente.')
    print('Auto-login simulado. Entrando como Aluno...')
    student_menu({'nome':nome,'email':email})
def login_flow():
    print('1-Aluno(email) 2-Professor(cpf)')
    op = input('> ').strip()
    if op=='1':
        email = input('Email: '); senha = input_hidden('Senha: ')
        print('Tentando logar... (demonstracao: use usuarios do DB criado por setup_db.py)')
    elif op=='2':
        cpf = input('CPF: '); senha = input_hidden('Senha: ')
        print('Tentando logar... (demonstracao: use usuarios do DB criado por setup_db.py)')
    else:
        return None
def student_menu(user):
    while True:
        print('\n=== Menu Aluno ==='); print('1-Meus Dados 2-Gerar graficos (genero/idade) 3-Download grafico 0-Sair')
        op = input('> ').strip()
        if op=='1': print(user)
        elif op=='2':
            print('1-Genero 2-Idade'); k = input('> ').strip()
            if k=='1': r = send({'cmd':'report','kind':'gender'})
            else: r = send({'cmd':'report','kind':'age'})
            if r.get('status')=='ok': print('Grafico gerado no servidor:', r.get('path'))
            else: print('Erro:', r)
        elif op=='3':
            fname = input('Nome do arquivo no servidor (ex: gender_dist_...) : ').strip()
            print('Para baixar, gere primeiro e copie o nome.')
        elif op=='0': break
        else: print('Opcao invalida')
def professor_menu(user):
    while True:
        print('\n=== Menu Professor ==='); print('1-Criar turma (nao implementado no demo) 2- Gerar grafico: media/box/presenca 0-Sair')
        op = input('> ').strip()
        if op=='1': print('Funcao disponivel no servidor (use admin/setup).')
        elif op=='2':
            print('1-Media por turma 2-BoxNotas 3-Presenca'); k = input('> ').strip()
            if k=='1': r = send({'cmd':'report','kind':'avg','turma':None})
            elif k=='2': r = send({'cmd':'report','kind':'box','turma':None})
            else: r = send({'cmd':'report','kind':'trend','turma':None})
            print('Resposta:', r.get('status'), r.get('path') if r.get('status')=='ok' else r.get('msg'))
        elif op=='0': break
        else: print('Opcao invalida')
def main():
    print('PIM v3 - Client (demonstracao)')
    while True:
        print('\n1-Entrar (demo) 2-Sair')
        o = input('> ').strip()
        if o=='1': login_flow()
        elif o=='2': break
if __name__=='__main__': main()
