import os

def _clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# main.py - entrada do sistema v11 (compatível com nova DataStore)
import os, time, getpass
from integrated_data_store import DataStore
import logger_utils
from integrated_data_store import backup_data, migrate_passwords
from alunos_menu import cadastrar_aluno_flow, aluno_menu
from professores_menu import cadastrar_professor_flow, professor_menu
from admin_menu import admin_menu

# ----------------------
# Função de login unificada
# ----------------------
def unified_login(data, ident_prompt="Identificador", role_expected=None, allow_admin=False):
    """
    data: DataStore instance
    ident_prompt: prompt shown to user (ex: 'Email' or 'CPF' or 'CPF ou Email')
    role_expected: if provided, ensures the returned user has this role
    allow_admin: if True, special-case admin/admin login accepted
    Returns authenticated user dict or None
    """
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        ident = input(f"{ident_prompt}: ").strip()
        senha = getpass.getpass("Senha: ").strip()
        if not ident or not senha:
            print("Identificador ou senha vazios. Tente novamente.")
            attempts += 1
            time.sleep(1)
            continue

        # admin quick-login if allowed
        if allow_admin and ident == "admin" and senha == "admin":
            logger_utils.registrar_evento("INFO", "Login bem-sucedido (admin)", usuario="admin")
            return {"id": 0, "role": "admin", "name": "Administrator", "email": "admin"}

        user = data.autenticar(ident, senha)
        if user is None:
            # verificar se existe o identificador
            identificador_existe = any((u.get("email") == ident or u.get("cpf") == ident) for u in data.usuarios)
            if identificador_existe:
                logger_utils.registrar_evento("WARN", "Falha de login - senha incorreta", usuario=ident)
                print("\\n❌ Senha incorreta. Tente novamente.\\n")
            else:
                logger_utils.registrar_evento("WARN", "Falha de login - usuário não encontrado", usuario=ident)
                print("\\n❌ Usuário não encontrado. Verifique o identificador digitado.\\n")
            attempts += 1
            time.sleep(1)
            continue

        if role_expected and user.get("role") != role_expected:
            logger_utils.registrar_evento("ERROR", "Falha login - role incorreto", usuario=ident)
            print("Credenciais inválidas para este tipo de usuário.")
            return None

        # sucesso
        logger_utils.registrar_evento("INFO", f"Login bem-sucedido ({user.get('role')})", usuario=user.get("email") or user.get("cpf") or user.get("nome"))
        return user

    # se esgotou tentativas
    print("Número máximo de tentativas excedido. Voltando ao menu.")
    logger_utils.registrar_evento("ERROR", "Bloqueio temporário por tentativas excedidas", usuario=None)
    return None



# instancia unica do DataStore
# data store singleton moved to integrated_data_store compatibility wrappers

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    _clear()
    logger_utils.registrar_evento("INFO", "Aplicacao iniciada", usuario=None)
    # backup automatico e migracao de senhas antigas
    try:
        b = backup_data()
        if b:
            logger_utils.registrar_evento('INFO', f'Backup automatico criado: {b}', usuario=None)
    except Exception:
        pass
    try:
        changed = migrate_passwords()
        if changed:
            logger_utils.registrar_evento('INFO', f'Migradas {changed} senhas para hash', usuario=None)
    except Exception:
        pass

    while True:
        clear()
        print("\n" + "="*50 + "\n=== PIM2 ADS ===\nMENU PRINCIPAL\n" + "="*50 + "\n")
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
                print("\n" + "="*50 + "\nMENU PRINCIPAL\n" + "="*50 + "\n === Cadastro ===")
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
                    print("Opção inválida"); time.sleep(1)

        # ----------------------------------------------------------------------
        # 2 - LOGIN
        # ----------------------------------------------------------------------
        elif c == "2":
            # LOGIN - identificador (email ou cpf) unificado
            data = DataStore.get_instance()
            user = unified_login(data, ident_prompt="CPF ou Email", allow_admin=True)
            if user:
                data.login(user)
                role = user.get("role")
                if role == "aluno":
                    aluno_menu(user)
                elif role == "professor":
                    professor_menu(user)
                elif role == "admin":
                    admin_menu(user)
                else:
                    print("Role desconhecido; retornando ao menu principal.")
            # fim do loop de tentativas


            # ----------------------------------------------------------------------
        # 0 - SAIR
        # ----------------------------------------------------------------------
        elif c == "0":
            logger_utils.registrar_evento("INFO", "Aplicacao encerrada", usuario=None)
            print("Saindo...")
            break

        else:
            print("Opção inválida"); time.sleep(1)


if __name__ == "__main__":
    main()
