# alunos_menu.py
import time, getpass, os
import logger_utils
from integrated_data_store import find_usuario_por_email, add_usuario, verify_credentials_email, decrypt_text, load_cursos, aulas_por_curso, calcular_media_aula, adicionar_avaliacao, update_usuario

def aluno_menu(user):
    def clear(): os.system("cls" if os.name=="nt" else "clear")
    while True:
        clear()
        logger_utils.registrar_evento("INFO", "Aluno abriu menu", usuario=decrypt_text(user.get("email")))
        print("--- Menu Aluno ---")
        print("1 - Perfil")
        print("2 - Cursos disponiveis")
        print("3 - Assistente IA")
        print("0 - Voltar")
        op = input("> ").strip()
        if op == "1":
            perfil_submenu_aluno(user)
        elif op == "2":
            cursos = load_cursos()
            for c in cursos:
                print(f"ID:{c.get('id')} - {c.get('nome')} - {c.get('descricao')}")
            cid = input("Digite ID do curso para ver aulas (ou enter para voltar): ").strip()
            if cid:
                try: cid = int(cid)
                except: print("ID invalido"); time.sleep(1); continue
                aulas = aulas_por_curso(cid)
                for a in aulas:
                    print(f"ID:{a.get('id')} - {a.get('titulo')} - Prof:{a.get('professor_id')} - Media:{calcular_media_aula(a.get('id'))}")
                escolha = input("Digite ID da aula para avaliar (ou enter para voltar): ").strip()
                if escolha:
                    try:
                        aid = int(escolha)
                        avaliar_aula_flow(user, aid)
                    except:
                        print("ID invalido"); time.sleep(1)
                input("ENTER para voltar")
        elif op == "3":
            from ai_module import answer_faq, recommend_courses_for_user, log_query
            clear()
            print('--- Assistente IA ---')
            print('1 - Perguntas frequentes (FAQ)')
            print('2 - Recomendar cursos')
            print('0 - Voltar')
            sub = input('> ').strip()
            if sub == '1':
                q = input('Digite sua pergunta: ').strip()
                resp = answer_faq(q)
                log_query(user, q)
                print('\\n' + resp)
                input('ENTER para voltar')
            elif sub == '2':
                recs = recommend_courses_for_user(user)
                if not recs:
                    print('Sem cursos para recomendar')
                else:
                    print('Cursos recomendados:')
                    for c in recs:
                        print(f"ID:{c.get('id')} - {c.get('nome')} - {c.get('descricao')}")
                input('ENTER para voltar')
            elif sub == '0':
                pass
        elif op == "0":
            return
        else:
            print("Opcao invalida"); time.sleep(1)

def cadastrar_aluno_flow():
    clear = lambda: os.system("cls" if os.name=="nt" else "clear")
    clear()
    print("--- Cadastro de Aluno ---")
    name = input("Nome completo: ").strip()
    email = input("Email: ").strip()
    dob = input("Data nascimento (YYYY-MM-DD): ").strip()
    genero = input("Genero (masculino/feminino/outro): ").strip().lower()
    senha = getpass.getpass("Senha: ")
    co = getpass.getpass("Confirmar senha: ")
    if senha != co:
        logger_utils.registrar_evento("ERROR", "Cadastro aluno - co-senha diferente", usuario=email)
        print("Senhas diferentes. Cancelando.")
        time.sleep(1); return None
    if find_usuario_por_email(email):
        logger_utils.registrar_evento("ERROR", "Cadastro aluno - email duplicado", usuario=email)
        print("Email ja cadastrado."); time.sleep(1); return None
    u = add_usuario({"role":"aluno","name":name,"email":email,"dob":dob,"genero":genero,"password":senha})
    logger_utils.registrar_evento("INFO", "Cadastro aluno efetuado", usuario=email)
    print("Cadastro realizado com sucesso!"); time.sleep(1)
    return u

def perfil_submenu_aluno(user):
    while True:
        clear = lambda: os.system("cls" if os.name=="nt" else "clear"); clear()
        print("=== PERFIL DO ALUNO ===")
        print("1. Ver meus dados")
        print("2. Alterar e-mail")
        print("3. Alterar senha")
        print("4. Alterar data de nascimento")
        print("5. Alterar genero")
        print("0. Voltar")
        op = input("> ").strip()
        if op == "1":
            print("ID:", user.get("id"))
            print("Nome:", user.get("name"))
            print("Email:", decrypt_text(user.get("email")))
            print("Data Nasc:", user.get("dob"))
            print("Genero:", user.get("genero"))
            input("ENTER para voltar")
        elif op == "2":
            novo = input("Novo email: ").strip()
            if find_usuario_por_email(novo):
                print("Email em uso."); logger_utils.registrar_evento("ERROR", "Perfil aluno - email duplicado", usuario=decrypt_text(user.get("email"))); time.sleep(1); continue
            update_usuario(user.get("id"), {"email": novo})
            logger_utils.registrar_evento("INFO", "Perfil aluno - email alterado", usuario=novo)
            print("Email atualizado."); time.sleep(1)
        elif op == "3":
            atual = getpass.getpass("Senha atual: ")
            if not verify_credentials_email(decrypt_text(user.get("email")), atual):
                print("Senha atual incorreta."); logger_utils.registrar_evento("ERROR", "Perfil aluno - senha atual incorreta", usuario=decrypt_text(user.get("email"))); time.sleep(1); continue
            nova = getpass.getpass("Nova senha: "); co = getpass.getpass("Confirmar nova senha: ")
            if nova != co: print("Confirmacao nao confere."); logger_utils.registrar_evento("ERROR", "Perfil aluno - co-senha diferente", usuario=decrypt_text(user.get("email"))); time.sleep(1); continue
            update_usuario(user.get("id"), {"password": nova}); logger_utils.registrar_evento("INFO", "Perfil aluno - senha alterada", usuario=decrypt_text(user.get("email"))); print("Senha alterada."); time.sleep(1)
        elif op == "4":
            novo = input("Nova data de nascimento (YYYY-MM-DD): ").strip(); update_usuario(user.get("id"), {"dob": novo}); logger_utils.registrar_evento("INFO", "Perfil aluno - dob alterada", usuario=decrypt_text(user.get("email"))); print("Atualizado."); time.sleep(1)
        elif op == "5":
            novo = input("Genero (masculino/feminino/outro): ").strip().lower(); update_usuario(user.get("id"), {"genero": novo}); logger_utils.registrar_evento("INFO", "Perfil aluno - genero alterado", usuario=decrypt_text(user.get("email"))); print("Atualizado."); time.sleep(1)
        elif op == "0": return
        else: print("Opcao invalida"); time.sleep(1)

def avaliar_aula_flow(user, aula_id):
    try: nota = int(input("Nota (1-5): ").strip())
    except: print("Nota invalida"); time.sleep(1); return
    comentario = input("Comentario (opcional): ").strip()
    adicionar_avaliacao(aula_id, user.get("id"), nota, comentario)
    media = calcular_media_aula(aula_id)
    logger_utils.registrar_evento("INFO", f"Aluno avaliou aula {aula_id} com {nota}", usuario=decrypt_text(user.get("email")))
    print(f"Avaliacao registrada. Media atual: {media}"); input("ENTER para voltar")