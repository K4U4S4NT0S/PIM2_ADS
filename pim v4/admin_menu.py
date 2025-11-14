# admin_menu.py
import time
import os
import json
import logger_utils
from integrated_data_store import (
    load_cursos, criar_curso, atualizar_curso, deletar_curso,
    load_aulas, criar_aula, atualizar_aula, deletar_aula,
    cadastrar_usuario, atualizar_usuario, decrypt_text
)

# Garante que o diretório data/ exista
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def _clear():
    """Limpa a tela de forma portátil."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def _load(path):
    """Carrega JSON com segurança, evitando crashes."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


# ========================= MENU PRINCIPAL DO ADMIN ========================= #

def admin_menu(user):
    """
    Menu principal do admin.
    Recebe o objeto 'user' (usuário logado) para logs/contexto.
    """
    while True:
        _clear()
        logger_utils.registrar_evento("INFO", "Admin abriu menu", usuario=user.get("email") if user else "admin")
        print("--- Menu Admin ---")
        print("1 - Gerenciar usuários")
        print("2 - Gerenciar cursos")
        print("3 - Gerenciar aulas")
        print("4 - Gerar diagramas UML (PlantUML)")
        print("0 - Logout")
        op = input("> ").strip()

        if op == "1":
            manage_users_menu()

        elif op == "2":
            manage_courses_menu()

        elif op == "3":
            manage_lessons_menu()

        elif op == "4":
            try:
                from generate_diagrams import generate_all
                files = generate_all()
                print("Diagramas gerados:")
                for fpath in files:
                    print(" -", fpath)
            except Exception as e:
                print("Erro ao gerar diagramas:", e)
            input("ENTER para voltar")

        
        elif op == "9":
            _clear()
            print("\n===== EDITAR/ADICIONAR USUÁRIO =====")
            identificador = input("Digite Email ou CPF do usuário a editar (ou novo): ").strip()
            if not identificador:
                print("Identificador vazio. Abortando.")
                input("ENTER para voltar")
                _clear()
                continue
            # tentar localizar por email ou cpf
            usuarios = data.usuarios
            target = next((u for u in usuarios if u.get("email")==identificador or u.get("cpf")==identificador), None)
            if not target:
                print("Usuário não encontrado. Deseja criar novo usuário com este identificador? (S/N)")
                resp = input("> ").strip().lower()
                if resp not in ("s","sim"):
                    input("ENTER para voltar")
                    _clear()
                    continue
                # criar novo usuário mínimo
                nome = input("Nome: ").strip()
                email = input("Email (ou deixe vazio): ").strip()
                cpf = input("CPF (ou deixe vazio): ").strip()
                senha = input("Senha (ou deixe vazio): ").strip()
                genero = input("Gênero (opcional): ").strip()
                idade = input("Idade (opcional): ").strip()
                role = input("Role (aluno/professor/admin): ").strip() or "aluno"
                if genero: novo["genero"] = genero
                if idade: novo["idade"] = int(idade) if idade.isdigit() else idade
                novo = {k:v for k,v in [("nome",nome),("email",email),("cpf",cpf),("role",role),("senha",senha)] if v}
                try:
                    cadastrar_usuario(novo)
                    logger_utils.registrar_evento("INFO","Admin criou usuário", usuario="admin")
                    print("Usuário criado com sucesso.")
                except Exception as e:
                    print("Erro ao criar usuário:", str(e))
                input("ENTER para voltar")
                _clear()
                continue
            # se encontrado, permitir alterar campos
            print("Usuário encontrado:", target.get('id'), target.get('nome'))
            novo_nome = input(f"Nome [{target.get('nome')}]: ").strip()
            novo_email = input(f"Email [{target.get('email') or ''}]: ").strip()
            novo_cpf = input(f"CPF [{target.get('cpf') or ''}]: ").strip()
            novo_role = input(f"Role [{target.get('role')}]: ").strip()
            novo_senha = input("Senha (deixe em branco para manter): ").strip()
            novo_genero = input(f"Gênero [{target.get('genero') or ""}]: ").strip()
            novo_idade = input(f"Idade [{target.get('idade') or ""}]: ").strip()
            patch = {}
            if novo_genero: patch["genero"] = novo_genero
            if novo_idade: patch["idade"] = int(novo_idade) if novo_idade.isdigit() else novo_idade
            if novo_nome: patch['nome'] = novo_nome
            if novo_email: patch['email'] = novo_email
            if novo_cpf: patch['cpf'] = novo_cpf
            if novo_role: patch['role'] = novo_role
            if novo_senha: patch['senha'] = novo_senha
            try:
                atualizar_usuario(target.get('id'), patch)
                logger_utils.registrar_evento("INFO","Admin atualizou usuário", usuario="admin")
                print("Usuário atualizado com sucesso.")
            except Exception as e:
                print("Erro ao atualizar usuário:", str(e))
            input("ENTER para voltar")
            _clear()
        elif op == "0":
            # confirmação de logout
            conf = input("Deseja realmente sair/efetuar logout? (S/N): ").strip().lower()
            if conf in ("s", "sim"):
                return
            else:
                continue

        else:
            print("Opção inválida")
            time.sleep(1)


# ============================= GERENCIAR USUÁRIOS ============================= #

def manage_users_menu():
    while True:
        _clear()
        print("=== Gerenciar Usuários ===")
        print("1 - Listar usuários")
        print("2 - Editar usuário")
        print("3 - Excluir usuário")
        print("0 - Voltar")
        op = input("> ").strip()

        # LISTAR USUÁRIOS
        if op == "1":
            users = _load(os.path.join(DATA_DIR, "usuarios.json"))
            if not users:
                print("Nenhum usuário cadastrado.")
            else:
                for u in users:
                    # usa 'nome' se disponível, fallback para 'name'
                    nome = u.get('nome') or u.get('name') or "(sem nome)"
                    email = decrypt_text(u.get('email') or "") if u.get('email') else u.get('email') or ""
                    cpf = decrypt_text(u.get('cpf') or "") if u.get('cpf') else u.get('cpf') or ""
                    print(f"ID:{u.get('id')} - Nome:{nome} - Role:{u.get('role')} - Email:{email} - CPF:{cpf}")
            input("ENTER para voltar")

        # EDITAR USUÁRIO
        elif op == "2":
            try:
                uid = int(input("ID do usuário: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue

            users = _load(os.path.join(DATA_DIR, "usuarios.json"))
            target = next((u for u in users if u.get("id") == uid), None)

            if not target:
                print("Usuário não encontrado")
                time.sleep(1)
                continue

            novo = input("Novo nome (enter para manter): ").strip()
            if novo:
                # atualizar_usuario espera 'nome' ou 'name' dependendo da estrutura
                atualizar_usuario(uid, {"nome": novo})

            print("Atualizado")
            time.sleep(1)

        # EXCLUIR USUÁRIO
        elif op == "3":
            try:
                uid = int(input("ID do usuário para excluir: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue

            users = _load(os.path.join(DATA_DIR, "usuarios.json"))
            new_list = [u for u in users if u.get('id') != uid]

            path = os.path.join(DATA_DIR, "usuarios.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(new_list, f, indent=2, ensure_ascii=False)

            print("Usuário excluído")
            time.sleep(1)

        elif op == "0":
            return

        else:
            print("Opção inválida")
            time.sleep(1)


# ============================= GERENCIAR CURSOS ============================= #

def manage_courses_menu():
    while True:
        _clear()
        print("=== Gerenciar Cursos ===")
        print("1 - Listar cursos")
        print("2 - Criar curso")
        print("3 - Editar curso")
        print("4 - Excluir curso")
        print("0 - Voltar")

        op = input("> ").strip()

        # LISTAR
        if op == "1":
            cursos = load_cursos()
            if not cursos:
                print("Nenhum curso cadastrado.")
            else:
                for c in cursos:
                    nome = c.get('nome') or c.get('titulo') or "(sem nome)"
                    print(f"ID:{c.get('id')} - {nome} - {c.get('descricao','')}")
            input("ENTER para voltar")

        # CRIAR
        elif op == "2":
            nome = input("Nome do curso: ").strip()
            if not nome:
                print("Nome do curso vazio. Operação cancelada.")
                time.sleep(1)
                continue
            desc = input("Descrição: ").strip()
            # criar_curso espera um dict ou pode variar conforme implementação; tenta suportar ambas
            try:
                # se a função do datastore espera um dict:
                criar_curso({"nome": nome, "descricao": desc})
            except Exception:
                # fallback para assinatura antiga
                try:
                    criar_curso(nome, desc)
                except Exception as e:
                    print("Erro ao criar curso:", e)
                    time.sleep(1)
                    continue
            logger_utils.registrar_evento("INFO", "Admin criou curso", usuario="admin")
            print("Curso criado")
            time.sleep(1)

        # EDITAR
        elif op == "3":
            try:
                cid = int(input("ID do curso: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue

# continue file...
