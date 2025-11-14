import os
import getpass
from integrated_data_store import DataStore, load_alunos, adicionar_nota, encrypt_text

def _clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def _input_nonempty(prompt):
    val = input(prompt).strip()
    if not val:
        print("Entrada vazia — operação cancelada.")
        return None
    return val

def cadastrar_professor_flow():
    data = DataStore.get_instance()
    _clear()
    print("="*40)
    print("CADASTRO DE PROFESSOR")
    print("="*40)
    nome = input("Nome completo: ").strip()
    if not nome:
        print("Nome vazio. Cadastro cancelado.")
        return None
    cpf = input("CPF (somente números): ").strip()
    if not cpf or not cpf.isdigit():
        print("CPF inválido. Cadastro cancelado.")
        return None
    genero = input("Gênero (M/F/Outro) — deixe em branco se preferir não informar: ").strip()
    if not genero:
        genero = "Não informado"
    idade_raw = input("Idade (apenas números): ").strip()
    try:
        idade = int(idade_raw)
        if idade < 18 or idade > 120:
            print("Idade inválida para professor. Cadastro cancelado.")
            return None
    except:
        print("Idade inválida. Cadastro cancelado.")
        return None
    senha = getpass.getpass("Senha (mínimo 6 caracteres): ").strip()
    if len(senha) < 6:
        print("Senha muito curta. Cadastro cancelado.")
        return None
    senha2 = getpass.getpass("Confirme a senha: ").strip()
    if senha != senha2:
        print("Senhas não conferem. Cadastro cancelado.")
        return None
    try:
        cpf_enc = encrypt_text(cpf)
    except:
        cpf_enc = cpf
    usuario = {"nome": nome, "cpf": cpf_enc, "role": "professor", "senha": senha}
    data.cadastrar_usuario(usuario)
    criado_user = next((u for u in data.usuarios if (u.get('cpf') == cpf_enc or u.get('cpf') == cpf)), None)
    if criado_user:
        print(f"Professor cadastrado com sucesso! ID usuario = {criado_user.get('id')}")
    input("ENTER para voltar")
    return criado_user

def dar_nota_flow(professor_user=None):
    data = DataStore.get_instance()
    _clear()
    print("="*40)
    print("DAR NOTA A UM ALUNO")
    print("="*40)
    alunos = load_alunos()
    if not alunos:
        print("Não há alunos cadastrados.")
        input("ENTER para voltar")
        return False
    for a in alunos:
        print(f"{a.get('id')} - {a.get('nome', 'Sem nome')}")
    aid = input("Digite o ID do aluno que deseja avaliar (ou 0 para cancelar): ").strip()
    if aid == "0" or aid == "":
        print("Operação cancelada.")
        input("ENTER para voltar")
        return False
    try:
        aid = int(aid)
    except:
        print("ID inválido.")
        input("ENTER para voltar")
        return False
    aluno = next((x for x in alunos if int(x.get('id', -1)) == aid), None)
    if not aluno:
        print("Aluno não encontrado.")
        input("ENTER para voltar")
        return False
    valor_raw = input("Digite a nota (0-10): ").strip()
    try:
        valor = float(valor_raw.replace(',','.'))
        if valor < 0 or valor > 10:
            print("Valor inválido.")
            input("ENTER para voltar")
            return False
    except:
        print("Valor inválido.")
        input("ENTER para voltar")
        return False
    desc = input("Descrição/observações (opcional): ").strip()
    professor_id = professor_user.get('id') if isinstance(professor_user, dict) else None
    nota = adicionar_nota(aluno.get('id'), professor_id, valor, desc)
    if nota:
        print(f"Nota registrada com sucesso. ID nota = {nota.get('id')}")
    else:
        print("Erro ao registrar nota.")
    input("ENTER para voltar")
    return True

def professor_menu(user):
    _clear()
    data = DataStore.get_instance()
    while True:
        print("\n===== MENU DO PROFESSOR =====")
        print("1 - Ver meus dados")
        print("2 - Dar nota a um aluno")
        print("3 - Ver meus cursos")
        print("0 - Sair\n")
        op = input("> ").strip()
        if op == "1":
            _clear()
            print("\n===== MEUS DADOS =====")
            try:
                # Mostrar apenas os campos esperados para professor
                def show(v):
                    return v if v is not None and v != '' else '-'
                print(f"id: {show(user.get('id'))}")
                print(f"nome: {show(user.get('nome'))}")
                print(f"cpf: {show(user.get('cpf'))}")
                print(f"genero: {show(user.get('genero'))}")
                print(f"idade: {show(user.get('idade'))}")
            except Exception:
                # fallback mínimo
                print(f"id: {user.get('id')}")
                print(f"nome: {user.get('nome')}")
            input("ENTER para voltar")
            _clear()

            dar_nota_flow(professor_user=user)
            _clear()
        elif op == "3":
            _clear()
            cursos = getattr(data, 'cursos', [])
            cursos_prof = [c for c in cursos if int(c.get('professor_id', -1)) == int(user.get('id', -1))] if cursos else []
            if not cursos_prof:
                print("Você não está associado a nenhum curso.")
            else:
                for c in cursos_prof:
                    print(f"{c.get('id')} - {c.get('nome') or c.get('titulo','(sem nome)')}")
            input("ENTER para voltar")
            _clear()
        elif op == "0":
            conf = input("Deseja realmente sair do menu do professor? (S/N): ").strip().lower()
            if conf in ('s','sim'):
                _clear()
                break
            else:
                _clear()
                continue
        else:
            print("Opção inválida")
            input("ENTER para voltar")
            _clear()
