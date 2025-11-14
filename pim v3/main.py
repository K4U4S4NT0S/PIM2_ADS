# main.py - entrada do sistema v11 (compatível com nova DataStore)
import os, time, getpass
from integrated_data_store import DataStore
import logger_utils
from alunos_menu import cadastrar_aluno_flow, aluno_menu
from professores_menu import cadastrar_professor_flow, professor_menu
from admin_menu import admin_menu

# instancia unica do DataStore
data = DataStore()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    logger_utils.registrar_evento("INFO", "Aplicacao iniciada", usuario=None)

    while True:
        clear()
        print("=== PIM2 ADS ===")
        print("1 - Cadastro")
        print("2 - Login")
        print("0 - Sair")
        c = input("> ").strip()

        # ----------------------------------------------------------------------
        # 1 - CADASTRO
        # ----------------------------------------------------------------------
        if c == "1":
            while True:
                clear()
                print("=== Cadastro ===")
                print("1 - Cadastrar Aluno")
                print("2 - Cadastrar Professor")
                print("0 - Voltar")
                op = input("> ").strip()

                if op == "1":
                    user = cadastrar_aluno_flow()
                    if user:
                        aluno_menu(user)

                elif op == "2":
                    user = cadastrar_professor_flow()
                    if user:
                        professor_menu(user)

                elif op == "0":
                    break

                else:
                    print("Opcao invalida"); time.sleep(1)

        # ----------------------------------------------------------------------
        # 2 - LOGIN
        # ----------------------------------------------------------------------
        elif c == "2":
            while True:
                clear()
                print("=== Login ===")
                print("1 - Login Aluno (email)")
                print("2 - Login Professor (CPF)")
                print("3 - Login Admin (admin/admin)")
                print("0 - Voltar")
                op = input("> ").strip()

                # login aluno (email)
                if op == "1":
                    email = input("Email: ").strip()
                    senha = getpass.getpass("Senha: ")
                    
                    user = data.autenticar(email, senha)
                    if user and user.get("role") == "aluno":
                        data.login(user)
                        aluno_menu(user)
                    else:
                        logger_utils.registrar_evento("ERROR", "Falha login aluno", usuario=email)
                        print("Credenciais invalidas"); time.sleep(1)

                # login professor (cpf)
                elif op == "2":
                    cpf = input("CPF: ").strip()
                    senha = getpass.getpass("Senha: ")

                    user = data.autenticar(cpf, senha)
                    if user and user.get("role") == "professor":
                        data.login(user)
                        professor_menu(user)
                    else:
                        logger_utils.registrar_evento("ERROR", "Falha login professor", usuario=cpf)
                        print("Credenciais invalidas"); time.sleep(1)

                # login admin
                elif op == "3":
                    user = input("Usuario: ").strip()
                    senha = getpass.getpass("Senha: ")

                    if user == "admin" and senha == "admin":
                        admin_menu({"id":0,"role":"admin","name":"Administrator","email":"admin"})
                    else:
                        logger_utils.registrar_evento("ERROR", "Falha login admin", usuario=user)
                        print("Credenciais invalidas"); time.sleep(1)

                elif op == "0":
                    break

                else:
                    print("Opcao invalida"); time.sleep(1)

        # ----------------------------------------------------------------------
        # 0 - SAIR
        # ----------------------------------------------------------------------
        elif c == "0":
            logger_utils.registrar_evento("INFO", "Aplicacao encerrada", usuario=None)
            print("Saindo...")
            break

        else:
            print("Opcao invalida"); time.sleep(1)


if __name__ == "__main__":
    main()
