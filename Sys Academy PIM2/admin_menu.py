
# admin_menu_fixed.py - admin com associação professor->curso
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
    data = DataStore.get_instance()
    while True:
        _clear()
        logger_utils.log("INFO", "Admin abriu o menu", usuario=user.get("email") if user else "admin")
        print("="*40)
        print("Sys Academy - MENU ADMIN")
        print("="*40)
        print("1 - Gerenciar usuários")
        print("2 - Gerenciar cursos")
        print("3 - Gerenciar aulas")
        print("4 - Associar professor a curso")
        print("5 - Gerar diagramas UML (PlantUML)")
        print("0 - Logout")
        op = input("> ").strip()

        if op == "1":
            manage_users_menu(data)

        elif op == "2":
            manage_courses_menu(data)

        elif op == "3":
            manage_lessons_menu(data, admin_mode=True)

        elif op == "4":
            associate_professor_to_course(data)

        elif op == "5":
            try:
                from generate_diagrams import generate_all
                files = generate_all()
                print("Diagramas gerados:")
                for fpath in files:
                    print(" -", fpath)
                logger_utils.log("INFO", "Admin gerou diagramas", usuario=user.get("email") if user else "admin")
            except Exception as e:
                logger_utils.log("ERROR", f"Erro ao gerar diagramas: {e}", usuario=user.get("email") if user else "admin")
                print("Erro ao gerar diagramas:", e)
            input("ENTER para voltar")

        elif op == "0":
            conf = input("Deseja realmente sair/efetuar logout? (S/N): ").strip().lower()
            if conf in ("s", "sim"):
                logger_utils.log("INFO", "Admin efetuou logout", usuario=user.get("email") if user else "admin")
                return
            else:
                continue
        else:
            print("Opção inválida")
            time.sleep(1)

def associate_professor_to_course(data):
    _clear()
    print("="*40)
    print("Sys Academy - ASSOCIAR PROFESSOR A CURSO")
    print("="*40)
    cursos = getattr(data, "cursos", []) or []
    usuarios = getattr(data, "usuarios", []) or []
    professores = [u for u in usuarios if u.get("role") == "professor"]
    if not cursos:
        print("Nenhum curso cadastrado.")
        input("ENTER para voltar")
        return
    if not professores:
        print("Nenhum professor cadastrado.")
        input("ENTER para voltar")
        return
    print("Cursos:")
    for c in cursos:
        print(f"{c.get('id')} - {c.get('nome')}")
    try:
        cid = int(input("ID do curso: ").strip())
    except:
        print("ID inválido.")
        input("ENTER para voltar")
        return
    curso = next((c for c in cursos if c.get("id") == cid), None)
    if not curso:
        print("Curso não encontrado.")
        input("ENTER para voltar")
        return
    print("Professores:")
    for p in professores:
        print(f"{p.get('id')} - {p.get('nome')}")
    try:
        pid = int(input("ID do professor: ").strip())
    except:
        print("ID inválido.")
        input("ENTER para voltar")
        return
    prof = next((p for p in professores if p.get("id") == pid), None)
    if not prof:
        print("Professor não encontrado.")
        input("ENTER para voltar")
        return
    # associar
    try:
        data.atualizar_curso(cid, {"professor_id": pid})
        logger_utils.log("INFO", f"Curso {cid} associado ao professor {pid}", usuario="admin")
        print("Professor associado ao curso com sucesso.")
    except Exception as e:
        logger_utils.log("ERROR", f"Erro ao associar professor ao curso: {e}", usuario="admin")
        print("Erro ao associar:", e)
    input("ENTER para voltar")

# Reuso das funções gerenciar usuários/curso/aula do admin anterior, com pequeno ajuste para admin_mode flag
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
                logger_utils.log("INFO", f"Admin atualizou nome do usuário {uid} para {novo}", usuario="admin")
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
            if hasattr(data, 'save_usuarios'):
                data.save_usuarios(usuarios)
            else:
                os.makedirs(DATA_DIR, exist_ok=True)
                with open(usuarios_path, "w", encoding="utf-8") as f:
                    import json
                    json.dump(usuarios, f, indent=2, ensure_ascii=False)
            logger_utils.log("WARN", f"Admin excluiu usuário {uid}", usuario="admin")
            print("Usuário excluído")
            time.sleep(1)

        elif op == "0":
            return
        else:
            print("Opção inválida")
            time.sleep(1)

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
                    prof = c.get('professor_id', '-')
                    print(f"ID:{c.get('id')} - {nome} - Prof:{prof} - {c.get('descricao','')}")
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
                logger_utils.log("INFO", "Admin criou curso", usuario="admin")
                print("Curso criado (ID: {})".format(novo.get('id') if novo else '?'))
            except Exception as e:
                logger_utils.log("ERROR", f"Erro ao criar curso: {e}", usuario="admin")
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
                logger_utils.log("INFO", f"Admin atualizou curso {cid}", usuario="admin")
                print("Curso atualizado")
            except Exception as e:
                logger_utils.log("ERROR", f"Erro ao atualizar curso: {e}", usuario="admin")
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
                logger_utils.log("WARN", f"Admin excluiu curso {cid}", usuario="admin")
                print("Curso excluído")
            except Exception as e:
                logger_utils.log("ERROR", f"Erro ao excluir curso: {e}", usuario="admin")
                print("Erro ao excluir curso:", e)
            time.sleep(1)

        elif op == "0":
            return
        else:
            print("Opção inválida")
            time.sleep(1)

def manage_lessons_menu(data, admin_mode=False, professor_user=None):
    while True:
        _clear()
        title = "GERENCIAR AULAS (ADMIN)" if admin_mode else "GERENCIAR AULAS (PROFESSOR)"
        print("="*40)
        print(f"Sys Academy - {title}")
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
                    print(f"ID:{a.get('id')} - {a.get('titulo')} - Curso:{a.get('curso_id')} - Prof:{a.get('professor_id')}")
            input("ENTER para voltar")

        elif op == "2":
            titulo = input("Titulo da aula: ").strip()
            if not titulo:
                print("Titulo vazio. Cancelado.")
                time.sleep(1)
                continue
            curso_id_raw = input("ID do curso associado: ").strip()
            if not curso_id_raw.isdigit():
                print("ID do curso inválido.")
                time.sleep(1)
                continue
            curso_id = int(curso_id_raw)
            # se não for admin, validar se professor está associado ao curso
            if not admin_mode and professor_user:
                curso = next((c for c in (getattr(data,'cursos',[]) or []) if c.get('id')==curso_id), None)
                if not curso or int(curso.get('professor_id', -1)) != int(professor_user.get('id', -1)):
                    print("Você não tem permissão para criar aulas neste curso.")
                    logger_utils.log("WARN", f"Professor {professor_user.get('id')} tentou criar aula em curso {curso_id} sem permissão", usuario=professor_user.get('id'))
                    input("ENTER para voltar")
                    continue
            prof_id = input("ID do professor (opcional, será seu ID se não preencher): ").strip()
            descricao = input("Descrição (opcional): ").strip()
            payload = {"titulo": titulo, "curso_id": curso_id, "professor_id": int(prof_id) if prof_id.isdigit() else (professor_user.get('id') if professor_user else None), "descricao": descricao}
            try:
                data.criar_aula(payload)
                logger_utils.log("INFO", f"Aula criada: {titulo} (curso {curso_id})", usuario=professor_user.get('id') if professor_user else 'admin')
                print("Aula criada")
            except Exception as e:
                logger_utils.log("ERROR", f"Erro ao criar aula: {e}", usuario=professor_user.get('id') if professor_user else 'admin')
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
            # se não admin, validar permissão
            if not admin_mode and professor_user:
                if int(aula.get('professor_id', -1)) != int(professor_user.get('id', -1)):
                    print("Você não tem permissão para editar esta aula.")
                    logger_utils.log("WARN", f"Professor {professor_user.get('id')} tentou editar aula {aid} sem permissão", usuario=professor_user.get('id'))
                    input("ENTER para voltar")
                    continue
            novo_titulo = input(f"Titulo [{aula.get('titulo')}]: ").strip()
            novo_desc = input(f"Descricao [{aula.get('descricao','')}]: ").strip()
            patch = {}
            if novo_titulo: patch['titulo'] = novo_titulo
            if novo_desc: patch['descricao'] = novo_desc
            try:
                data.atualizar_aula(aid, patch)
                logger_utils.log("INFO", f"Aula {aid} atualizada", usuario=professor_user.get('id') if professor_user else 'admin')
                print("Aula atualizada")
            except Exception as e:
                logger_utils.log("ERROR", f"Erro ao atualizar aula: {e}", usuario=professor_user.get('id') if professor_user else 'admin')
                print("Erro ao atualizar aula:", e)
            time.sleep(1)

        elif op == "4":
            try:
                aid = int(input("ID da aula a excluir: ").strip())
            except Exception:
                print("ID inválido")
                time.sleep(1)
                continue
            aula = next((x for x in (getattr(data,'aulas',[]) or []) if x.get('id') == aid), None)
            if not aula:
                print("Aula não encontrada")
                time.sleep(1)
                continue
            if not admin_mode and professor_user:
                if int(aula.get('professor_id', -1)) != int(professor_user.get('id', -1)):
                    print("Você não tem permissão para excluir esta aula.")
                    logger_utils.log("WARN", f"Professor {professor_user.get('id')} tentou excluir aula {aid} sem permissão", usuario=professor_user.get('id'))
                    input("ENTER para voltar")
                    continue
            try:
                data.deletar_aula(aid)
                logger_utils.log("WARN", f"Aula {aid} excluída", usuario=professor_user.get('id') if professor_user else 'admin')
                print("Aula excluída")
            except Exception as e:
                logger_utils.log("ERROR", f"Erro ao excluir aula: {e}", usuario=professor_user.get('id') if professor_user else 'admin')
                print("Erro ao excluir aula:", e)
            time.sleep(1)

        elif op == "0":
            return
        else:
            print("Opção inválida")
            time.sleep(1)
