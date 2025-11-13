from users import register_student, register_teacher, login_by_email, login_by_cpf, admin_login
from student_menu import student_menu
from teacher_menu import teacher_menu
from admin_menu import admin_menu

def initial_menu():
    while True:
        print("\n=== MENU INICIAL ===")
        print("1. Realizar cadastro")
        print("2. Realizar login")
        print("3. Sair")
        opc = input("Escolha: ").strip()
        if opc == "1":
            # oferecer opção aluno/professor
            tipo = input("Cadastrar como (1) Aluno ou (2) Professor? ")
            if tipo == "1":
                user = register_student()
                if user:
                    student_menu(user)
            elif tipo == "2":
                user = register_teacher()
                if user:
                    teacher_menu(user)
            else:
                print("Opcao invalida.")
        elif opc == "2":
            # oferecer opção email ou cpf para identificar
            metodo = input("Entrar como (1) Aluno (email) ou (2) Professor (cpf) ou (3) Admin: ")
            if metodo == "1":
                user = login_by_email()
                if user:
                    student_menu(user)
            elif metodo == "2":
                user = login_by_cpf()
                if user:
                    teacher_menu(user)
            elif metodo == "3":
                admin = admin_login()
                if admin:
                    admin_menu(admin)
            else:
                print("Opcao invalida.")
        elif opc == "3":
            print("Saindo...")
            break
        else:
            print("Opcao invalida.")

if __name__ == "__main__":
    initial_menu()
