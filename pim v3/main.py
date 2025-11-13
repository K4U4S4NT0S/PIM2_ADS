# main.py - entrada do sistema v10 (sem acentos)
import os, time, getpass
from integrated_data_store import verify_credentials_email, verify_credentials_cpf
import logger_utils
from alunos_menu import cadastrar_aluno_flow, aluno_menu
from professores_menu import cadastrar_professor_flow, professor_menu
from admin_menu import admin_menu

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
        elif c == "2":
            while True:
                clear()
                print("=== Login ===")
                print("1 - Login Aluno (email)")
                print("2 - Login Professor (CPF)")
                print("3 - Login Admin (admin/admin)")
                print("0 - Voltar")
                op = input("> ").strip()
                if op == "1":
                    email = input("Email: ").strip(); senha = getpass.getpass("Senha: ")
                    user = verify_credentials_email(email, senha)
                    if user: aluno_menu(user)
                    else:
                        logger_utils.registrar_evento("ERROR", "Falha login aluno", usuario=email)
                        print("Credenciais invalidas"); time.sleep(1)
                elif op == "2":
                    cpf = input("CPF: ").strip(); senha = getpass.getpass("Senha: ")
                    user = verify_credentials_cpf(cpf, senha)
                    if user: professor_menu(user)
                    else:
                        logger_utils.registrar_evento("ERROR", "Falha login professor", usuario=cpf)
                        print("Credenciais invalidas"); time.sleep(1)
                elif op == "3":
                    user = input("Usuario: ").strip(); senha = getpass.getpass("Senha: ")
                    if user == "admin" and senha == "admin":
                        admin_menu({"id":0,"role":"admin","name":"Administrator","email":"admin"})
                    else:
                        logger_utils.registrar_evento("ERROR", "Falha login admin", usuario=user)
                        print("Credenciais invalidas"); time.sleep(1)
                elif op == "0":
                    break
                else:
                    print("Opcao invalida"); time.sleep(1)
        elif c == "0":
            logger_utils.registrar_evento("INFO", "Aplicacao encerrada", usuario=None)
            print("Saindo...")
            break
        else:
            print("Opcao invalida"); time.sleep(1)

if __name__ == "__main__":
    main()