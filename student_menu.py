from uml_and_graphs import generate_course_graphs
from ai_chat import ask_ai
from log_utils import log_action

def student_menu(user):
    while True:
        print(f"\n=== MENU ALUNO ({user.get('nome')}) ===")
        print("1. Ver agenda de aulas")
        print("2. Perfil")
        print("3. Notas")
        print("4. Chat de IA (simulado)")
        print("5. Cursos -> ver cursos e aulas -> avaliar cursos e aulas")
        print("6. Logout")
        opc = input("Escolha: ").strip()
        if opc == "1":
            print("[AGENDA] Aqui seria listada agenda - integrar com dados do seu projeto.")
        elif opc == "2":
            print("Perfil:")
            print(user)
            editar = input("Alterar nome/genero? (s/n) ")
            if editar.lower() == "s":
                old_name = user.get('nome')
                user['nome'] = input("Novo nome: ")
                user['genero'] = input("Novo genero: ")
                print("Perfil atualizado (em memória). Salve no arquivo se desejar.")
                log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="aluno", action="edit", target_type="user", target_id=user.get("id"), details={"field":"nome/genero","old_name":old_name,"new_name":user.get("nome")})
        elif opc == "3":
            print("[NOTAS] Funcionalidade de notas - integrar com seu backend de cursos.")
        elif opc == "4":
            prompt = input("Pergunte algo para a IA: ")
            resp = ask_ai(prompt)
            print("IA:", resp)
            log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="aluno", action="ask_ai", target_type="ai", target_id="local", details={"prompt": prompt})
        elif opc == "5":
            print("[CURSOS] Listar cursos e permitir avaliar (placeholder).")
            generate_course_graphs()
        elif opc == "6":
            confirm = input("Confirmar logout? (s/n) ")
            if confirm.lower() == "s":
                log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="aluno", action="logout", target_type="self", target_id=user.get("id"))
                print("Logout realizado.")
                break
        else:
            print("Opcao invalida.")
