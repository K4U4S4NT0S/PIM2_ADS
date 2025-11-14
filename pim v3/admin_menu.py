# admin_menu.py
import time, os, json
import logger_utils
from integrated_data_store import (
    load_cursos, criar_curso, update_curso, delete_curso,
    load_aulas, criar_aula, update_aula, delete_aula,
    add_usuario, update_usuario, decrypt_text
)

# Garante que o diretório data/ exista
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def _load(path):
    """Carrega JSON com segurança, evitando crashes."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# ========================= MENU PRINCIPAL DO ADMIN ========================= #

def admin_menu(user):
    def clear(): os.system("cls" if os.name == "nt" else "clear")

    while True:
        clear()
        logger_utils.registrar_evento("INFO", "Admin abriu menu", usuario="admin")
        print("--- Menu Admin ---")
        print("1 - Gerenciar usuarios")
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
            from generate_diagrams import generate_all
            files = generate_all()
            print("Diagramas gerados:")
            for fpath in files:
                print(" -", fpath)
            input("ENTER para voltar")

        elif op == "0":
            return

        else:
            print("Opcao invalida")
            time.sleep(1)


# ============================= GERENCIAR USUÁRIOS ============================= #

def manage_users_menu():
    while True:
        clear = lambda: os.system("cls" if os.name == 'nt' else 'clear'); clear()
        print("1 - Listar usuarios")
        print("2 - Editar usuario")
        print("3 - Excluir usuario")
        print("0 - Voltar")

        op = input("> ").strip()

        # LISTAR USUÁRIOS
        if op == "1":
            users = _load(os.path.join(DATA_DIR, "usuarios.json"))
            for u in users:
                print(
                    f"ID:{u.get('id')} - Nome:{u.get('name')} - Role:{u.get('role')}"
                    f" - Email:{decrypt_text(u.get('email') or '')}"
                    f" - CPF:{decrypt_text(u.get('cpf') or '')}"
                )
            input("ENTER para voltar")

        # EDITAR USUÁRIO
        elif op == "2":
            try:
                uid = int(input("ID do usuario: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue

            users = _load(os.path.join(DATA_DIR, "usuarios.json"))
            target = None
            for u in users:
                if u.get("id") == uid:
                    target = u
                    break

            if not target:
                print("Usuario nao encontrado")
                time.sleep(1)
                continue

            novo = input("Novo nome (enter para manter): ").strip()
            if novo:
                update_usuario(uid, {"name": novo})

            print("Atualizado")
            time.sleep(1)

        # EXCLUIR USUÁRIO
        elif op == "3":
            try:
                uid = int(input("ID do usuario para excluir: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue

            users = _load(os.path.join(DATA_DIR, "usuarios.json"))
            new_list = [u for u in users if u.get("id") != uid]

            path = os.path.join(DATA_DIR, "usuarios.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(new_list, f, indent=2, ensure_ascii=False)

            print("Usuario excluido")
            time.sleep(1)

        elif op == "0":
            return

        else:
            print("Opcao invalida")
            time.sleep(1)


# ============================= GERENCIAR CURSOS ============================= #

def manage_courses_menu():
    while True:
        clear = lambda: os.system("cls" if os.name=='nt' else 'clear'); clear()
        print("1 - Listar cursos")
        print("2 - Criar curso")
        print("3 - Editar curso")
        print("4 - Excluir curso")
        print("0 - Voltar")

        op = input("> ").strip()

        # LISTAR
        if op == "1":
            cursos = load_cursos()
            for c in cursos:
                print(f"ID:{c.get('id')} - {c.get('nome')} - {c.get('descricao')}")
            input("ENTER para voltar")

        # CRIAR
        elif op == "2":
            nome = input("Nome do curso: ").strip()
            desc = input("Descricao: ").strip()
            criar_curso(nome, desc)
            logger_utils.registrar_evento("INFO", "Admin criou curso", usuario="admin")
            print("Curso criado")
            time.sleep(1)

        # EDITAR
        elif op == "3":
            try:
                cid = int(input("ID do curso: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue

            novo = input("Novo nome (enter para manter): ").strip()
            if novo:
                update_curso(cid, {"nome": novo})

            print("Atualizado")
            time.sleep(1)

        # EXCLUIR
        elif op == "4":
            try:
                cid = int(input("ID do curso para excluir: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue

            delete_curso(cid)
            logger_utils.registrar_evento("INFO", "Admin excluiu curso", usuario="admin")
            print("Curso excluido")
            time.sleep(1)

        elif op == "0":
            return

        else:
            print("Opcao invalida")
            time.sleep(1)


# ============================= GERENCIAR AULAS ============================= #

def manage_lessons_menu():
    while True:
        clear = lambda: os.system("cls" if os.name=='nt' else 'clear'); clear()
        print("1 - Listar aulas")
        print("2 - Criar aula")
        print("3 - Editar aula")
        print("4 - Excluir aula")
        print("0 - Voltar")

        op = input("> ").strip()

        # LISTAR
        if op == "1":
            aulas = load_aulas()
            for a in aulas:
                print(f"ID:{a.get('id')} - {a.get('titulo')} - Curso:{a.get('curso_id')}")
            input("ENTER para voltar")

        # CRIAR
        elif op == "2":
            titulo = input("Titulo aula: ").strip()
            desc = input("Descricao: ").strip()

            try:
                cid = int(input("Curso ID: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue

            criar_aula(cid, titulo, desc, "admin")
            logger_utils.registrar_evento("INFO", "Admin criou aula", usuario="admin")
            print("Aula criada")
            time.sleep(1)

        # EDITAR
        elif op == "3":
            try:
                aid = int(input("ID da aula: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue

            novo = input("Novo titulo (enter para manter): ").strip()
            if novo:
                update_aula(aid, {"titulo": novo})

            print("Atualizado")
            time.sleep(1)

        # EXCLUIR
        elif op == "4":
            try:
                aid = int(input("ID da aula para excluir: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue

            delete_aula(aid)
            logger_utils.registrar_evento("INFO", "Admin excluiu aula", usuario="admin")
            print("Aula excluida")
            time.sleep(1)

        elif op == "0":
            return

        else:
            print("Opcao invalida")
            time.sleep(1)
