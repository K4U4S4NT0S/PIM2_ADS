import json
import os
from getpass import getpass
import bcrypt
from datetime import datetime
from typing import Optional
from log_utils import log_action

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
BACKUP_USERS_DIR = os.path.join(BACKUP_DIR, "users")
os.makedirs(BACKUP_USERS_DIR, exist_ok=True)

MAX_LOGIN_ATTEMPTS = 5

def hash_password(plain_password: str) -> str:
    pw = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw, salt)
    return hashed.decode("utf-8")

def check_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    # Criar arquivo users.json com admin default se nao existir
    if not os.path.exists(USERS_FILE):
        default_admin = {
            "users": [
                {
                    "id": "admin_1",
                    "role": "admin",
                    "username": "admin",
                    "nome": "Administrador",
                    "password": hash_password("admin"),
                    "created_at": datetime.utcnow().isoformat()
                }
            ]
        }
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_admin, f, indent=2, ensure_ascii=False)

def load_users():
    ensure_data_dir()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    ensure_data_dir()
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def register_student():
    data = load_users()
    users = data["users"]

    nome = input("Nome: ").strip()
    email = input("Email: ").strip().lower()
    data_nasc = input("Data de nascimento (YYYY-MM-DD): ").strip()
    genero = input("Gênero: ").strip()

    while True:
        senha = getpass("Senha: ")
        senha2 = getpass("Confirme a senha: ")
        if senha != senha2:
            print("Senhas nao conferem. Tente novamente.")
        elif len(senha) < 6:
            print("Senha deve ter ao menos 6 caracteres.")
        else:
            break

    # valida unicidade email
    if any(u.get("email") == email for u in users):
        print("Email ja cadastrado.")
        return None

    hashed = hash_password(senha)
    user = {
        "id": f"user_{int(datetime.utcnow().timestamp())}",
        "role": "aluno",
        "nome": nome,
        "email": email,
        "data_nasc": data_nasc,
        "genero": genero,
        "password": hashed,
        "created_at": datetime.utcnow().isoformat()
    }
    users.append(user)
    save_users(data)
    print("Cadastro de aluno concluido. Acesando menu de aluno...")
    # log
    log_action(actor_id=user["id"], actor_name=user["nome"], role="aluno", action="create", target_type="user", target_id=user["id"], details={"role":"aluno"})
    return user

def register_teacher():
    data = load_users()
    users = data["users"]

    nome = input("Nome: ").strip()
    cpf = input("CPF (somente numeros): ").strip()
    data_nasc = input("Data de nascimento (YYYY-MM-DD): ").strip()
    genero = input("Gênero: ").strip()

    while True:
        senha = getpass("Senha: ")
        senha2 = getpass("Confirme a senha: ")
        if senha != senha2:
            print("Senhas nao conferem. Tente novamente.")
        elif len(senha) < 6:
            print("Senha deve ter ao menos 6 caracteres.")
        else:
            break

    if any(u.get("cpf") == cpf for u in users):
        print("CPF ja cadastrado.")
        return None

    hashed = hash_password(senha)
    user = {
        "id": f"user_{int(datetime.utcnow().timestamp())}",
        "role": "professor",
        "nome": nome,
        "cpf": cpf,
        "data_nasc": data_nasc,
        "genero": genero,
        "password": hashed,
        "created_at": datetime.utcnow().isoformat()
    }
    users.append(user)
    save_users(data)
    print("Cadastro de professor concluido. Acesando menu de professor...")
    log_action(actor_id=user["id"], actor_name=user["nome"], role="professor", action="create", target_type="user", target_id=user["id"], details={"role":"professor"})
    return user

def login_by_email():
    data = load_users()
    users = data["users"]
    email = input("Email: ").strip().lower()
    user = next((u for u in users if u.get("email") == email and u.get("role") == "aluno"), None)
    if not user:
        print("Aluno nao encontrado.")
        return None
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        senha = getpass("Senha: ")
        if check_password(senha, user["password"]):
            print("Login bem sucedido.")
            log_action(actor_id=user["id"], actor_name=user["nome"], role="aluno", action="login", target_type="self", target_id=user["id"])
            return user
        attempts += 1
        print(f"Senha incorreta ({attempts}/{MAX_LOGIN_ATTEMPTS})")
    print("Numero maximo de tentativas atingido. Conta bloqueada temporariamente.")
    log_action(actor_id=user.get("id","unknown"), actor_name=user.get("nome","unknown"), role="aluno", action="failed_login", target_type="self", target_id=user.get("id","unknown"), details={"attempts": attempts})
    return None

def login_by_cpf():
    data = load_users()
    users = data["users"]
    cpf = input("CPF (somente numeros): ").strip()
    user = next((u for u in users if u.get("cpf") == cpf and u.get("role") == "professor"), None)
    if not user:
        print("Professor nao encontrado.")
        return None
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        senha = getpass("Senha: ")
        if check_password(senha, user["password"]):
            print("Login bem sucedido.")
            log_action(actor_id=user["id"], actor_name=user["nome"], role="professor", action="login", target_type="self", target_id=user["id"])
            return user
        attempts += 1
        print(f"Senha incorreta ({attempts}/{MAX_LOGIN_ATTEMPTS})")
    print("Numero maximo de tentativas atingido. Conta bloqueada temporariamente.")
    log_action(actor_id=user.get("id","unknown"), actor_name=user.get("nome","unknown"), role="professor", action="failed_login", target_type="self", target_id=user.get("id","unknown"), details={"attempts": attempts})
    return None

def admin_login():
    """
    Agora o admin tambem eh um usuario com role 'admin' armazenado em users.json.
    O login pede 'username' e verifica a senha hash.
    """
    data = load_users()
    users = data["users"]
    username = input("Admin Usuario: ").strip()
    user = next((u for u in users if u.get("username") == username and u.get("role") == "admin"), None)
    if not user:
        print("Admin nao encontrado.")
        return None
    senha = getpass("Senha: ")
    if check_password(senha, user["password"]):
        print("Login admin bem sucedido.")
        log_action(actor_id=user["id"], actor_name=user.get("nome","admin"), role="admin", action="login", target_type="self", target_id=user["id"])
        return user
    print("Credenciais admin invalidas.")
    log_action(actor_id=user.get("id","unknown"), actor_name=user.get("nome","unknown"), role="admin", action="failed_login", target_type="self", target_id=user.get("id","unknown"))
    return None

# Backup utilities (usuarios)
def backup_user(user_obj):
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"user_backup_{user_obj.get('id','unknown')}_{ts}.json"
    path = os.path.join(BACKUP_USERS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(user_obj, f, indent=2, ensure_ascii=False)
    return path

# Função para excluir usuário (com backup e log). Retorna True se excluído.
def delete_user_by_index(index: int) -> bool:
    data = load_users()
    users = data["users"]
    if index < 0 or index >= len(users):
        return False
    user = users[index]
    backup_path = backup_user(user)
    # remover
    users.pop(index)
    save_users(data)
    # log
    log_action(actor_id="system", actor_name="admin_action", role="admin", action="delete", target_type="user", target_id=user.get("id","unknown"), details={"backup": backup_path, "deleted_user_name": user.get("nome")})
    return True

# função utilitária para encontrar user index por id
def find_user_index_by_id(uid: str) -> Optional[int]:
    data = load_users()
    users = data["users"]
    for i,u in enumerate(users):
        if u.get("id") == uid:
            return i
    return None
