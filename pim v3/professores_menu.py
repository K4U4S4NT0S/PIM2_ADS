# professores_menu.py
import time, getpass, os
import logger_utils
from integrated_data_store import find_usuario_por_cpf, add_usuario, verify_credentials_cpf, decrypt_text, load_cursos, load_aulas, criar_aula, update_aula, delete_aula, aulas_por_curso, get_avaliacoes_por_aula, calcular_media_aula, update_usuario

def professor_menu(user):
    def clear(): os.system("cls" if os.name=="nt" else "clear")
    while True:
        clear()
        logger_utils.registrar_evento("INFO", "Professor abriu menu", usuario=decrypt_text(user.get("cpf")))
        print("--- Menu Professor ---")
        print("1 - Perfil")
        print("2 - Minhas aulas")
        print("0 - Voltar")
        op = input("> ").strip()
        if op == "1": perfil_submenu_professor(user)
        elif op == "2": minhas_aulas_submenu(user)
        elif op == "0": return
        else: print("Opcao invalida"); time.sleep(1)

def cadastrar_professor_flow():
    clear = lambda: os.system("cls" if os.name=="nt" else "clear"); clear()
    print("--- Cadastro de Professor ---")
    name = input("Nome completo: ").strip()
    cpf = input("CPF: ").strip()
    genero = input("Genero (masculino/feminino/outro): ").strip().lower()
    senha = getpass.getpass("Senha: "); co = getpass.getpass("Confirmar senha: ")
    if senha != co:
        logger_utils.registrar_evento("ERROR", "Cadastro professor - co-senha diferente", usuario=cpf)
        print("Senhas diferentes. Cancelando."); time.sleep(1); return None
    if find_usuario_por_cpf(cpf):
        logger_utils.registrar_evento("ERROR", "Cadastro professor - CPF duplicado", usuario=cpf)
        print("CPF ja cadastrado."); time.sleep(1); return None
    u = add_usuario({"role":"professor","name":name,"cpf":cpf,"genero":genero,"password":senha})
    logger_utils.registrar_evento("INFO", "Cadastro professor efetuado", usuario=cpf)
    print("Cadastro realizado com sucesso!"); time.sleep(1)
    return u

def perfil_submenu_professor(user):
    while True:
        clear = lambda: os.system("cls" if os.name=="nt" else "clear"); clear()
        print("=== PERFIL DO PROFESSOR ===")
        print("1. Ver meus dados")
        print("2. Alterar CPF")
        print("3. Alterar senha")
        print("4. Alterar data de nascimento")
        print("5. Alterar genero")
        print("0. Voltar")
        op = input("> ").strip()
        if op == "1":
            print("ID:", user.get("id"))
            print("Nome:", user.get("name"))
            print("CPF:", decrypt_text(user.get("cpf")))
            print("Data Nasc:", user.get("dob"))
            print("Genero:", user.get("genero"))
            input("ENTER para voltar")
        elif op == "2":
            novo = input("Novo CPF: ").strip()
            if find_usuario_por_cpf(novo):
                print("CPF em uso.")
                logger_utils.registrar_evento("ERROR", "Perfil professor - CPF duplicado", usuario=decrypt_text(user.get("cpf")))
                time.sleep(1)
                continue
            update_usuario(user.get("id"), {"cpf": novo})
            logger_utils.registrar_evento("INFO", "Perfil professor - CPF alterado", usuario=decrypt_text(user.get("cpf")))
            print("CPF atualizado."); time.sleep(1)
        elif op == "3":
            atual = getpass.getpass("Senha atual: ")
            if not verify_credentials_cpf(decrypt_text(user.get("cpf")), atual):
                print("Senha atual incorreta.")
                logger_utils.registrar_evento("ERROR", "Perfil professor - senha atual incorreta", usuario=decrypt_text(user.get("cpf")))
                time.sleep(1)
                continue
            nova = getpass.getpass("Nova senha: "); co = getpass.getpass("Confirmar nova senha: ")
            if nova != co:
                print("Confirmacao nao confere.")
                logger_utils.registrar_evento("ERROR", "Perfil professor - co-senha diferente", usuario=decrypt_text(user.get("cpf")))
                time.sleep(1)
                continue
            update_usuario(user.get("id"), {"password": nova})
            logger_utils.registrar_evento("INFO", "Perfil professor - senha alterada", usuario=decrypt_text(user.get("cpf")))
            print("Senha alterada."); time.sleep(1)
        elif op == "4":
            novo = input("Nova data de nascimento (YYYY-MM-DD): ").strip()
            update_usuario(user.get("id"), {"dob": novo})
            logger_utils.registrar_evento("INFO", "Perfil professor - dob alterada", usuario=decrypt_text(user.get("cpf")))
            print("Atualizado."); time.sleep(1)
        elif op == "5":
            novo = input("Genero (masculino/feminino/outro): ").strip().lower()
            update_usuario(user.get("id"), {"genero": novo})
            logger_utils.registrar_evento("INFO", "Perfil professor - genero alterado", usuario=decrypt_text(user.get("cpf")))
            print("Atualizado."); time.sleep(1)
        elif op == "0":
            return
        else: print("Opcao invalida"); time.sleep(1)

def minhas_aulas_submenu(user):
    while True:
        clear = lambda: os.system("cls" if os.name=='nt' else 'clear'); clear()
        print("=== MINHAS AULAS ===")
        print("1. Listar minhas aulas")
        print("2. Criar nova aula")
        print("3. Editar aula")
        print("4. Excluir aula")
        print("5. Ver avaliacoes das minhas aulas")
        print("0. Voltar")
        op = input("> ").strip()
        if op == "1":
            aulas = load_aulas(); mycpf = decrypt_text(user.get("cpf"))
            for a in aulas:
                if a.get("professor_id") == mycpf:
                    print(f"ID:{a.get('id')} - {a.get('titulo')} - Curso:{a.get('curso_id')}")
            input("ENTER para voltar")
        elif op == "2":
            titulo = input("Titulo: ").strip(); desc = input("Descricao: ").strip()
            cursos = load_cursos()
            for c in cursos: print(f"ID:{c.get('id')} - {c.get('nome')}")
            try:
                cid = int(input("Curso ID: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue
            criar_aula(cid, titulo, desc, decrypt_text(user.get("cpf"))); logger_utils.registrar_evento("INFO", "Professor criou aula", usuario=decrypt_text(user.get("cpf"))); print("Aula criada."); input("ENTER para voltar")
        elif op == "3":
            try:
                aid = int(input("ID da aula: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue
            titulo = input("Novo titulo (enter para manter): ").strip(); desc = input("Nova descricao (enter para manter): ").strip(); updates = {}
            if titulo: updates["titulo"]=titulo
            if desc: updates["descricao"]=desc
            try:
                update_aula(aid, updates); logger_utils.registrar_evento("INFO", "Professor atualizou aula", usuario=decrypt_text(user.get("cpf"))); print("Aula atualizada.")
            except Exception as e:
                print("Erro:", e); logger_utils.registrar_evento("ERROR", "Professor - erro atualizar aula: "+str(e), usuario=decrypt_text(user.get("cpf")))
            input("ENTER para voltar")
        elif op == "4":
            try:
                aid = int(input("ID da aula para excluir: ").strip())
            except:
                print("ID invalido"); time.sleep(1); continue
            confirm = input("Tem certeza? (S/N): ").strip().lower()
            if confirm == "s":
                delete_aula(aid)
                logger_utils.registrar_evento("INFO", "Professor excluiu aula", usuario=decrypt_text(user.get("cpf")))
                print("Aula excluida.")
            input("ENTER para voltar")
        elif op == "5":
            ver_avaliacoes_minhas_aulas(user)
        elif op == "0": return
        else: print("Opcao invalida"); time.sleep(1)

def ver_avaliacoes_minhas_aulas(user):
    clear = lambda: os.system("cls" if os.name=="nt" else "clear"); clear()
    mycpf = decrypt_text(user.get("cpf")); aulas = load_aulas()
    for a in aulas:
        if a.get("professor_id") == mycpf:
            avs = get_avaliacoes_por_aula(a.get("id")); media = calcular_media_aula(a.get("id")) if avs else 0
            print(f"Aula ID:{a.get('id')} - {a.get('titulo')} - Media:{media} - Avaliacoes:{len(avs)}")
            for av in avs:
                print(f"  - Usuario:{av.get('usuario_id')} Nota:{av.get('nota')} Coment:{av.get('comentario')}")
    input("ENTER para voltar")