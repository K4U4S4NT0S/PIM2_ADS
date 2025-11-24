# admin_menu_fixed.py - versão corrigida e simplificada do menu do administrador
import time
import os
from integrated_data_store import DataStore, decrypt_text
import logger_utils

def _clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def admin_menu(user):
    """
    Menu principal do admin.
    Usa DataStore para operações e logger_utils para registrar eventos.
    """
    data = DataStore.get_instance()
    while True:
        _clear()
        logger_utils.registrar_evento("INFO", "Admin abriu menu", usuario=user.get("email") if user else "admin")
        print("="*40)
        print("Sys Academy - MENU ADMIN")
        print("="*40)
        print("1 - Gerenciar usuários")
        print("2 - Gerenciar cursos")
        print("3 - Gerenciar aulas")
        print("4 - Gerar diagramas UML (PlantUML)")
        print("0 - Logout")
        op = input("> ").strip()

        if op == "1":
            manage_users_menu(data)

        elif op == "2":
            manage_courses_menu(data)

        elif op == "3":
            manage_lessons_menu(data)

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

        elif op == "0":
            conf = input("Deseja realmente sair/efetuar logout? (S/N): ").strip().lower()
            if conf in ("s", "sim"):
                return
            else:
                continue
        else:
            print("Opção inválida")
            time.sleep(1)

# ----------------- Gerenciar Usuários ----------------- #
def manage_users_menu(data):
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    usuarios_path = os.path.join(DATA_DIR, "usuarios.json")

    while True:
        _clear()
        print("="*40)
        print("Sys Academy - GERENCIAR USUÁRIOS")
        print("="*40)
        print("1 - Listar usuários")
        print("2 - Editar usuário")
        print("3 - Excluir usuário")
        print("0 - Voltar")
        op = input("> ").strip()

        if op == "1":
            usuarios = data.usuarios if hasattr(data, 'usuarios') else []
            if not usuarios:
                print("Nenhum usuário cadastrado.")
            else:
                for u in usuarios:
                    nome = u.get('nome') or u.get('name') or "(sem nome)"
                    email = decrypt_text(u.get('email')) if u.get('email') else ""
                    cpf = decrypt_text(u.get('cpf')) if u.get('cpf') else ""
                    print(f"ID:{u.get('id')} - Nome:{nome} - Role:{u.get('role')} - Email:{email} - CPF:{cpf}")
            input("ENTER para voltar")

        elif op == "2":
            try:
                uid = int(input("ID do usuário: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue
            target = next((u for u in (data.usuarios or []) if u.get("id") == uid), None)
            if not target:
                print("Usuário não encontrado")
                time.sleep(1)
                continue
            novo = input("Novo nome (enter para manter): ").strip()
            if novo:
                data.atualizar_usuario(uid, {"nome": novo})
            print("Atualizado")
            time.sleep(1)

        elif op == "3":
            try:
                uid = int(input("ID do usuário para excluir: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue
            usuarios = [u for u in (data.usuarios or []) if u.get('id') != uid]
            # persiste diretamente se DataStore disponibilizar
            if hasattr(data, 'save_usuarios'):
                data.save_usuarios(usuarios)
            else:
                # fallback: grava arquivo
                os.makedirs(DATA_DIR, exist_ok=True)
                with open(usuarios_path, "w", encoding="utf-8") as f:
                    import json
                    json.dump(usuarios, f, indent=2, ensure_ascii=False)
            print("Usuário excluído")
            time.sleep(1)

        elif op == "0":
            return
        else:
            print("Opção inválida")
            time.sleep(1)

# ----------------- Gerenciar Cursos ----------------- #
def manage_courses_menu(data):
    while True:
        _clear()
        print("="*40)
        print("Sys Academy - GERENCIAR CURSOS")
        print("="*40)
        print("1 - Listar cursos")
        print("2 - Criar curso")
        print("3 - Editar curso")
        print("4 - Excluir curso")
        print("0 - Voltar")
        op = input("> ").strip()

        if op == "1":
            cursos = getattr(data, 'cursos', []) or []
            if not cursos:
                print("Nenhum curso cadastrado.")
            else:
                for c in cursos:
                    nome = c.get('nome') or c.get('titulo') or "(sem nome)"
                    print(f"ID:{c.get('id')} - {nome} - {c.get('descricao','')}")
            input("ENTER para voltar")

        elif op == "2":
            nome = input("Nome do curso: ").strip()
            if not nome:
                print("Nome do curso vazio. Operação cancelada.")
                time.sleep(1)
                continue
            desc = input("Descrição: ").strip()
            try:
                novo = data.criar_curso({"nome": nome, "descricao": desc})
                logger_utils.registrar_evento("INFO", "Admin criou curso", usuario="admin")
                print("Curso criado (ID: {})".format(novo.get('id') if novo else '?'))
            except Exception as e:
                print("Erro ao criar curso:", e)
            time.sleep(1)

        elif op == "3":
            try:
                cid = int(input("ID do curso: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue
            cursos = getattr(data, 'cursos', []) or []
            target = next((c for c in cursos if c.get('id') == cid), None)
            if not target:
                print("Curso não encontrado")
                time.sleep(1)
                continue
            novo_nome = input(f"Nome [{target.get('nome')}]: ").strip()
            novo_desc = input(f"Descrição [{target.get('descricao','')}]: ").strip()
            patch = {}
            if novo_nome: patch['nome'] = novo_nome
            if novo_desc: patch['descricao'] = novo_desc
            try:
                data.atualizar_curso(cid, patch)
                print("Curso atualizado")
            except Exception as e:
                print("Erro ao atualizar curso:", e)
            time.sleep(1)

        elif op == "4":
            try:
                cid = int(input("ID do curso a excluir: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue
            try:
                data.deletar_curso(cid)
                print("Curso excluído")
            except Exception as e:
                print("Erro ao excluir curso:", e)
            time.sleep(1)

        elif op == "0":
            return
        else:
            print("Opção inválida")
            time.sleep(1)

# ----------------- Gerenciar Aulas ----------------- #
def manage_lessons_menu(data):
    while True:
        _clear()
        print("="*40)
        print("Sys Academy - GERENCIAR AULAS")
        print("="*40)
        print("1 - Listar aulas")
        print("2 - Criar aula")
        print("3 - Editar aula")
        print("4 - Excluir aula")
        print("0 - Voltar")
        op = input("> ").strip()

        if op == "1":
            aulas = getattr(data, 'aulas', []) or []
            if not aulas:
                print("Nenhuma aula cadastrada.")
            else:
                for a in aulas:
                    titulo = a.get('titulo') or a.get('nome') or "(sem titulo)"
                    print(f"ID:{a.get('id')} - {titulo} - Curso:{a.get('curso_id')} - Prof:{a.get('professor_id')}")
            input("ENTER para voltar")

        elif op == "2":
            titulo = input("Titulo da aula: ").strip()
            if not titulo:
                print("Titulo vazio. Cancelado.")
                time.sleep(1)
                continue
            curso_id = input("ID do curso associado: ").strip()
            prof_id = input("ID do professor (opcional): ").strip()
            descricao = input("Descrição (opcional): ").strip()
            payload = {"titulo": titulo, "curso_id": int(curso_id) if curso_id.isdigit() else curso_id, "professor_id": int(prof_id) if prof_id.isdigit() else prof_id, "descricao": descricao}
            try:
                data.criar_aula(payload)
                print("Aula criada")
            except Exception as e:
                print("Erro ao criar aula:", e)
            time.sleep(1)

        elif op == "3":
            try:
                aid = int(input("ID da aula: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue
            aula = next((x for x in (getattr(data,'aulas',[]) or []) if x.get('id') == aid), None)
            if not aula:
                print("Aula não encontrada")
                time.sleep(1)
                continue
            novo_titulo = input(f"Titulo [{aula.get('titulo')}]: ").strip()
            novo_desc = input(f"Descricao [{aula.get('descricao','')}]: ").strip()
            patch = {}
            if novo_titulo: patch['titulo'] = novo_titulo
            if novo_desc: patch['descricao'] = novo_desc
            try:
                data.atualizar_aula(aid, patch)
                print("Aula atualizada")
            except Exception as e:
                print("Erro ao atualizar aula:", e)
            time.sleep(1)

        elif op == "4":
            try:
                aid = int(input("ID da aula a excluir: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue
            try:
                data.deletar_aula(aid)
                print("Aula excluída")
            except Exception as e:
                print("Erro ao excluir aula:", e)
            time.sleep(1)

        elif op == "0":
            return
        else:
            print("Opção inválida")
            time.sleep(1)
