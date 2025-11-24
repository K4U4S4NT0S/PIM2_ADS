
# professores_menu_fixed.py - professor só gerencia aulas dos cursos que ele está associado
import os
from integrated_data_store import DataStore
import logger_utils
from admin_menu import manage_lessons_menu as admin_manage_lessons_menu

def _clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def professor_menu(user):
    _clear()
    data = DataStore.get_instance()
    while True:
        print("="*40)
        print("Sys Academy - MENU DO PROFESSOR")
        print("="*40)
        print("1 - Ver meus dados")
        print("2 - Dar nota a um aluno")
        print("3 - Gerenciar minhas aulas (criar/editar/excluir)")
        print("3 - Ver meus cursos")
        print("0 - Sair\n")
        op = input("> ").strip()
        if op == "1":
            _clear()
            print("="*40)
            print("Sys Academy - MEUS DADOS")
            print("="*40)
            try:
                def show(v):
                    return v if v is not None and v != '' else '-'
                print(f"id: {show(user.get('id'))}")
                print(f"nome: {show(user.get('nome'))}")
                print(f"cpf: {show(user.get('cpf'))}")
                print(f"genero: {show(user.get('genero'))}")
                dob = user.get('data_nascimento') or user.get('dob') or user.get('data de nascimento')
                age = calculate_age_from_dob(dob) if dob else None
                if age is not None:
                    print(f"idade: {age} anos (nascido em {dob})")
                else:
                    print(f"idade: {show(user.get('idade'))}")
            except Exception:
                print(f"id: {user.get('id')}")
                print(f"nome: {user.get('nome')}")
            input("ENTER para voltar")
            _clear()
        elif op == "2":
            dar_nota_flow(professor_user=user)
            _clear()
        elif op == "3":
            # chama manage_lessons_menu com admin_mode=False e professor_user=user
            admin_manage_lessons_menu(DataStore.get_instance(), admin_mode=False, professor_user=user)
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
                logger_utils.log("INFO", f"Professor {user.get('id')} efetuou logout", usuario=user.get('id'))
                _clear()
                break
            else:
                _clear()
                continue
        else:
            print("Opção inválida")
            input("ENTER para voltar")
            _clear()


def cadastrar_professor_flow():
    """
    Cadastro de professor (self-service).
    Campos: nome, cpf, genero, data_nascimento (YYYY-MM-DD), senha, confirma senha
    """
    from integrated_data_store import DataStore, encrypt_text
    import getpass, re
    data = DataStore.get_instance()
    print("="*40)
    print("Sys Academy - CADASTRO DE PROFESSOR (AUTO)")
    print("="*40)
    nome = input("Nome completo: ").strip()
    if not nome:
        print("Nome vazio. Cadastro cancelado.")
        return None
    cpf = input("CPF (somente números): ").strip()
    if not cpf or not cpf.isdigit():
        print("CPF inválido. Cadastro cancelado.")
        return None
    genero = input("Gênero (M/F/Outro): ").strip() or "Não informado"
    dob = input("Data de nascimento (DD-MM-AAAA): ").strip()
    # simples validação de data
    if not re.match(r'^\d{2}-\d{2}-\d{4}$', dob):
        print("Data inválida. Use o formato DD-MM-AAAA. Cadastro cancelado.")
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
    except Exception:
        cpf_enc = cpf
    usuario = {"nome": nome, "cpf": cpf_enc, "role": "professor", "senha": senha, "genero": genero, "data_nascimento": dob}
    try:
        data.cadastrar_usuario(usuario)
        criado_user = next((u for u in data.usuarios if u.get('cpf') in (cpf_enc, cpf)), None)
        if criado_user:
            print(f"Professor cadastrado com sucesso! ID usuario = {criado_user.get('id')}")
        else:
            print("Professor cadastrado, mas não foi possível recuperar o ID.")
        return criado_user
    except Exception as e:
        print("Erro ao cadastrar professor:", e)
        return None



from datetime import datetime, date

def calculate_age_from_dob(dob_str):
    """
    Recebe data no formato DD-MM-AAAA e retorna idade inteira.
    """
    try:
        d = datetime.strptime(dob_str, "%d-%m-%Y").date()
        today = date.today()
        age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
        return age
    except Exception:
        return None

def dar_nota_flow(professor_user=None):
    """
    Fluxo simplificado para professor dar nota a um aluno.
    """
    try:
        from integrated_data_store import DataStore, load_alunos, adicionar_nota
    except:
        from integrated_data_store import DataStore
        load_alunos = getattr(DataStore.get_instance(), "alunos", lambda: [])
        adicionar_nota = getattr(DataStore.get_instance(), "adicionar_nota", None)

    data = DataStore.get_instance()
    alunos = getattr(data, 'alunos', []) or []
    if not alunos:
        print("Nenhum aluno cadastrado.")
        input("ENTER para voltar")
        return False
    print("Alunos:")
    for a in alunos:
        print(f"{a.get('id')} - {a.get('nome')}")
    aid = input("Digite o ID do aluno para atribuir nota (ou 0 para cancelar): ").strip()
    if aid in ("0", ""):
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
    # try to call DataStore method or fallback to setting in memory
    try:
        nota = None
        if hasattr(data, 'adicionar_nota'):
            nota = data.adicionar_nota(aluno.get('id'), professor_id, valor, desc)
        elif adicionar_nota:
            nota = adicionar_nota(aluno.get('id'), professor_id, valor, desc)
        if nota:
            print(f"Nota registrada com sucesso. ID nota = {nota.get('id')}")
        else:
            print("Nota registrada (persistência não confirmada).")
    except Exception as e:
        print("Erro ao registrar nota:", e)
    input("ENTER para voltar")
    return True

