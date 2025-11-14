# professores_menu.py CORRIGIDO - compatível com DataStore v11

import time, getpass, os
import logger_utils
from integrated_data_store import (
    DataStore,
    decrypt_text,
    encrypt_text
)

# Usa a instância global criada no main.py
data = DataStore.get_instance()

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def professor_menu(user):
    while True:
        clear()
        try:
            usuario_log = decrypt_text(user.get("cpf"))
        except:
            usuario_log = user.get("cpf", "")

        logger_utils.registrar_evento("INFO", "Professor abriu menu", usuario=usuario_log)

        print("--- Menu Professor ---")
        print("1 - Perfil")
        print("2 - Minhas aulas")
        print("0 - Voltar")
        op = input("> ").strip()

        if op == "1":
            perfil_submenu_professor(user)
        elif op == "2":
            minhas_aulas_submenu(user)
        elif op == "0":
            return
        else:
            print("Opcao invalida"); time.sleep(1)


def cadastrar_professor_flow():
    clear()
    print("--- Cadastro de Professor ---")

    name = input("Nome completo: ").strip()
    cpf = input("CPF: ").strip()
    genero = input("Genero (masculino/feminino/outro): ").strip().lower()

    senha = getpass.getpass("Senha: ")
    co = getpass.getpass("Confirmar senha: ")

    if senha != co:
        logger_utils.registrar_evento("ERROR", "Cadastro professor - co-senha diferente", usuario=cpf)
        print("Senhas diferentes. Cancelando."); time.sleep(1)
        return None

    if data.find_user_by_cpf(cpf):
        logger_utils.registrar_evento("ERROR", "Cadastro professor - CPF duplicado", usuario=cpf)
        print("CPF já cadastrado."); time.sleep(1)
        return None

    novo_id = data.proximo_user_id()

    user = {
        "id": novo_id,
        "role": "professor",
        "name": name,
        "cpf": encrypt_text(cpf),
        "genero": genero,
        "senha": senha,
        "dob": ""
    }

    data.add_user(user)

    logger_utils.registrar_evento("INFO", "Cadastro professor efetuado", usuario=cpf)
    print("Cadastro realizado com sucesso!")
    time.sleep(1)
    return user


def perfil_submenu_professor(user):
    while True:
        clear()
        print("=== PERFIL DO PROFESSOR ===")
        print("1. Ver meus dados")
        print("2. Alterar CPF")
        print("3. Alterar senha")
        print("4. Alterar data de nascimento")
        print("5. Alterar genero")
        print("0. Voltar")
        op = input("> ").strip()

        if op == "1":
            print("ID:", user["id"])
            print("Nome:", user["name"])
            try:
                print("CPF:", decrypt_text(user["cpf"]))
            except:
                print("CPF:", user["cpf"])
            print("Data Nasc:", user.get("dob"))
            print("Genero:", user.get("genero"))
            input("ENTER para voltar")

        elif op == "2":
            novo = input("Novo CPF: ").strip()

            if data.find_user_by_cpf(novo):
                print("CPF já está sendo usado!")
                time.sleep(1)
                continue

            data.update_user(user["id"], {"cpf": encrypt_text(novo)})
            print("CPF atualizado!")
            time.sleep(1)

        elif op == "3":
            atual = getpass.getpass("Senha atual: ")

            cpf_dec = decrypt_text(user["cpf"])
            if not data.verify_credentials(cpf_dec, atual):
                print("Senha incorreta."); time.sleep(1)
                continue

            nova = getpass.getpass("Nova senha: ")
            co = getpass.getpass("Confirmar nova senha: ")

            if nova != co:
                print("Confirmacao incorreta."); time.sleep(1)
                continue

            data.update_user(user["id"], {"senha": nova})
            print("Senha alterada!"); time.sleep(1)

        elif op == "4":
            nova = input("Nova data (YYYY-MM-DD): ").strip()
            data.update_user(user["id"], {"dob": nova})
            print("Atualizado!"); time.sleep(1)

        elif op == "5":
            nova = input("Genero: ").strip().lower()
            data.update_user(user["id"], {"genero": nova})
            print("Genero atualizado!"); time.sleep(1)

        elif op == "0":
            return

        else:
            print("Opcao invalida"); time.sleep(1)


def minhas_aulas_submenu(user):
    while True:
        clear()
        print("=== MINHAS AULAS ===")
        print("1. Listar minhas aulas")
        print("2. Criar nova aula")
        print("3. Editar aula")
        print("4. Excluir aula")
        print("5. Ver avaliacoes")
        print("0. Voltar")
        op = input("> ").strip()

        try:
            mycpf = decrypt_text(user["cpf"])
        except:
            mycpf = user["cpf"]

        if op == "1":
            for a in data.aulas:
                if str(a["professor_id"]) == str(mycpf):
                    print(f"ID:{a['id']} - {a['titulo']} (Curso {a['curso_id']})")
            input("ENTER para voltar")

        elif op == "2":
            titulo = input("Titulo: ").strip()
            desc = input("Descricao: ").strip()

            for c in data.cursos:
                print(f"ID:{c['id']} - {c['nome']}")

            try:
                cid = int(input("ID do curso: "))
            except:
                print("Invalido"); time.sleep(1); continue

            aid = data.proximo_aula_id()

            aula = {
                "id": aid,
                "curso_id": cid,
                "titulo": titulo,
                "descricao": desc,
                "professor_id": mycpf
            }

            data.criar_aula(aula)
            print("Aula criada!"); input("ENTER para voltar")

        elif op == "3":
            try:
                aid = int(input("ID da aula: "))
            except:
                print("ID invalido"); time.sleep(1); continue

            titulo = input("Novo titulo (enter mantém): ").strip()
            desc = input("Nova descricao (enter mantém): ").strip()

            updates = {}
            if titulo: updates["titulo"] = titulo
            if desc: updates["descricao"] = desc

            data.update_aula(aid, updates)
            print("Aula atualizada!"); input("ENTER para voltar")

        elif op == "4":
            try:
                aid = int(input("Excluir ID: "))
            except:
                print("Invalido"); time.sleep(1); continue

            if input("Confirmar? (s/n): ").lower() == "s":
                data.delete_aula(aid)
                print("Aula excluída!")
            input("ENTER para voltar")

        elif op == "5":
            ver_avaliacoes_minhas_aulas(user)

        elif op == "0":
            return

        else:
            print("Opcao invalida"); time.sleep(1)


def ver_avaliacoes_minhas_aulas(user):
    clear()

    try:
        mycpf = decrypt_text(user["cpf"])
    except:
        mycpf = user["cpf"]

    for a in data.aulas:
        if str(a["professor_id"]) != str(mycpf):
            continue

        avs = [x for x in data.avaliacoes if x["aula_id"] == a["id"]]
        media = data.media_aula(a["id"]) if avs else 0

        print(f"Aula {a['id']} - {a['titulo']} | Média: {media}")

        for av in avs:
            print(f"  Usuário:{av['usuario_id']} Nota:{av['nota']} Coment:{av.get('comentario','')}")

    input("ENTER para voltar")
