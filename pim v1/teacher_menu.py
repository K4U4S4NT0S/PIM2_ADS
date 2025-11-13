from log_utils import log_action

def teacher_menu(user):
    while True:
        print(f"\n=== MENU PROFESSOR ({user.get('nome')}) ===")
        print("1. Ver turmas")
        print("2. Agendar aulas")
        print("3. Lancar notas")
        print("4. Lancar atividades")
        print("5. Registrar/listar aulas")
        print("6. Criar/editar/excluir aulas de acordo com o curso")
        print("7. Perfil")
        print("8. Logout")
        opc = input("Escolha: ").strip()
        if opc == "1":
            print("[TURMAS] - implementar com dados reais.")
        elif opc == "2":
            print("[AGENDAR AULAS] - formulario de agendamento.")
        elif opc == "3":
            print("[LANCAR NOTAS] - selecione turma/aluno/nota.")
        elif opc == "4":
            print("[LANCAR ATIVIDADES] - vincular a aula.")
        elif opc == "5":
            print("[REGISTRO DE AULAS] - adicionar/listar.")
        elif opc == "6":
            # exemplo simples de criar aula e logar a acao
            course_id = input("Course ID (exemplo): ")
            aula_id = f"aula_{int(__import__('time').time())}"
            titulo = input("Titulo da aula: ")
            # não há persistência direta aqui sem integrar com courses.json
            log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="professor", action="create", target_type="aula", target_id=aula_id, details={"course_id": course_id, "titulo": titulo})
            print("Aula criada (em memória).")
        elif opc == "7":
            new_name = input("Novo nome (enter para nao alterar): ").strip()
            new_gender = input("Novo genero (enter para nao alterar): ").strip()
            if new_name:
                old = user.get("nome")
                user['nome'] = new_name
                log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="professor", action="edit", target_type="user", target_id=user.get("id"), details={"field":"nome","old":old,"new":new_name})
            if new_gender:
                user['genero'] = new_gender
            print("Perfil atualizado localmente.")
        elif opc == "8":
            confirm = input("Confirmar logout? (s/n) ")
            if confirm.lower() == "s":
                log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="professor", action="logout", target_type="self", target_id=user.get("id"))
                break
        else:
            print("Opcao invalida.")
