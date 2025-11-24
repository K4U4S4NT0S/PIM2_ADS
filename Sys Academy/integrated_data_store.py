import json
import os
import base64
import shutil as _shutil
import datetime as _dt

# ---------------------------
# BACKUP
# ---------------------------
def backup_data(dest_dir='backups'):
    base = os.path.dirname(__file__)
    data_dir = os.path.join(base, 'data')
    if not os.path.isdir(data_dir):
        return None
    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(base, dest_dir, timestamp)
    try:
        _shutil.copytree(data_dir, dest)
        return dest
    except Exception:
        return None


# ======================================================
# CRIPTOGRAFIA (Fernet ou fallback base64)
# ======================================================
KEY_FILE = "secret.key"

try:
    from cryptography.fernet import Fernet, InvalidToken

    def _load_key():
        if not os.path.exists(KEY_FILE):
            key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as f:
                f.write(key)
        with open(KEY_FILE, "rb") as f:
            return f.read()

    FERNET = Fernet(_load_key())

    def encrypt_text(text: str) -> str:
        try:
            return FERNET.encrypt(text.encode()).decode()
        except Exception:
            return text

    def decrypt_text(text: str) -> str:
        try:
            return FERNET.decrypt(text.encode()).decode()
        except Exception:
            return text

except Exception:
    # fallback (sem cryptography)
    def encrypt_text(text: str) -> str:
        try:
            return base64.b64encode(text.encode()).decode()
        except:
            return text

    def decrypt_text(text: str) -> str:
        try:
            return base64.b64decode(text.encode()).decode()
        except:
            return text


# ======================================================
# SENHAS PBKDF2
# ======================================================
import os as _os
import hashlib as _hashlib
import binascii as _binascii

def hash_password(password: str, rounds: int = 100000):
    salt = _os.urandom(16)
    dk = _hashlib.pbkdf2_hmac("sha256", password.encode(), salt, rounds)
    return _binascii.hexlify(salt).decode(), _binascii.hexlify(dk).decode()

def verify_password(password: str, salt_hex: str, hash_hex: str, rounds: int = 100000):
    salt = _binascii.unhexlify(salt_hex)
    dk = _hashlib.pbkdf2_hmac("sha256", password.encode(), salt, rounds)
    return _binascii.hexlify(dk).decode() == hash_hex


# ======================================================
# JSON / PATHS
# ======================================================
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "usuarios.json")
ALUNOS_FILE = os.path.join(DATA_DIR, "alunos.json")
CURSOS_FILE = os.path.join(DATA_DIR, "cursos.json")
AULAS_FILE = os.path.join(DATA_DIR, "aulas.json")
AVALIACOES_FILE = os.path.join(DATA_DIR, "avaliacoes.json")
MATRICULAS_FILE = os.path.join(DATA_DIR, "matriculas.json")
NOTAS_FILE = os.path.join(DATA_DIR, "notas.json")

def _load_json(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            return json.loads(raw) if raw else []
    except:
        return []

def _save_json(path: str, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    try:
        os.replace(tmp, path)
    except:
        try:
            os.remove(tmp)
        except:
            pass


# ======================================================
# DATASTORE (Singleton)
# ======================================================
class DataStore:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DataStore()
        return cls._instance

    def __init__(self):
        if DataStore._instance is not None:
            return

        self.usuarios = _load_json(USERS_FILE)
        self.alunos = _load_json(ALUNOS_FILE)
        self.cursos = _load_json(CURSOS_FILE)
        self.aulas = _load_json(AULAS_FILE)
        self.avaliacoes = _load_json(AVALIACOES_FILE)
        self.matriculas = _load_json(MATRICULAS_FILE)
        self.notas = _load_json(NOTAS_FILE)

        self.usuario_logado = None


    # ======================================================
    # AUTENTICAÇÃO
    # ======================================================
    def autenticar(self, email_or_enc, senha):
        """Autentica usuário verificando identificador (email ou cpf) + senha.
        email_or_enc: pode ser email (texto) ou CPF (texto) ou CPF/encrypted stored form.
        """
        for user in self.usuarios:
            # check identifier match: accept email or cpf (plain or encrypted)
            ident = email_or_enc
            try:
                user_email = user.get('email')
                user_cpf = user.get('cpf')
                email_match = False
                cpf_match = False
                try:
                    if user_email:
                        if user_email == ident or decrypt_text(user_email) == ident:
                            email_match = True
                except:
                    pass
                try:
                    if user_cpf:
                        if user_cpf == ident or decrypt_text(user_cpf) == ident:
                            cpf_match = True
                except:
                    pass
                if not (email_match or cpf_match):
                    # identifier doesn't match this user
                    continue
            except:
                continue

            # login moderno (senha armazenada com salt/hash)
            salt = user.get("senha_salt")
            hsh = user.get("senha_hash")
            if salt and hsh:
                try:
                    if verify_password(senha, salt, hsh):
                        self.usuario_logado = user
                        return user
                except:
                    pass

            # senha antiga (plain)
            if user.get("senha") == senha:
                try:
                    new_salt, new_hash = hash_password(senha)
                    user["senha_salt"] = new_salt
                    user["senha_hash"] = new_hash
                    del user["senha"]
                    _save_json(USERS_FILE, self.usuarios)
                except:
                    pass
                self.usuario_logado = user
                return user

        return None

    def verify_credentials_email(self, email, senha):
        return self.autenticar(email, senha)

    def verify_credentials_cpf(self, cpf, senha):
        cpf_enc = encrypt_text(cpf)
        return self.autenticar(cpf_enc, senha)


    # ======================================================
    # CRUD Usuários / Alunos
    # ======================================================
    def cadastrar_usuario(self, user):
        if "id" not in user:
            user["id"] = self._next_id(self.usuarios)
        self.usuarios.append(user)
        _save_json(USERS_FILE, self.usuarios)

    def atualizar_usuario(self, user_id, novo):
        for i, u in enumerate(self.usuarios):
            if u.get("id") == user_id:
                self.usuarios[i] = {**u, **novo, "id": user_id}
                _save_json(USERS_FILE, self.usuarios)
                return self.usuarios[i]
        return None

    def cadastrar_aluno(self, aluno):
        if "id" not in aluno:
            aluno["id"] = self._next_id(self.alunos)
        self.alunos.append(aluno)
        _save_json(ALUNOS_FILE, self.alunos)


    # ======================================================
    # CRUD CURSOS
    # ======================================================
    def criar_curso(self, curso):
        if "id" not in curso:
            curso["id"] = self._next_id(self.cursos)
        self.cursos.append(curso)
        _save_json(CURSOS_FILE, self.cursos)
        return curso

    def atualizar_curso(self, curso_id, novo):
        for i, c in enumerate(self.cursos):
            if c.get("id") == curso_id:
                self.cursos[i] = {**c, **novo, "id": curso_id}
                _save_json(CURSOS_FILE, self.cursos)
                return self.cursos[i]
        return None

    def deletar_curso(self, curso_id):
        before = len(self.cursos)
        self.cursos = [c for c in self.cursos if c.get("id") != curso_id]
        if len(self.cursos) < before:
            _save_json(CURSOS_FILE, self.cursos)
            return True
        return False


    # ======================================================
    # CRUD AULAS
    # ======================================================
    def criar_aula(self, aula):
        if "id" not in aula:
            aula["id"] = self._next_id(self.aulas)
        self.aulas.append(aula)
        _save_json(AULAS_FILE, self.aulas)
        return aula

    def atualizar_aula(self, aula_id, novo):
        for i, a in enumerate(self.aulas):
            if a.get("id") == aula_id:
                self.aulas[i] = {**a, **novo, "id": aula_id}
                _save_json(AULAS_FILE, self.aulas)
                return self.aulas[i]
        return None

    def deletar_aula(self, aula_id):
        before = len(self.aulas)
        self.aulas = [a for a in self.aulas if a.get("id") != aula_id]
        if len(self.aulas) < before:
            _save_json(AULAS_FILE, self.aulas)
            return True
        return False


    # ======================================================
    # UTIL
    # ======================================================

    def find_usuario_por_cpf(self, cpf):
        for u in getattr(self, 'usuarios', []):
            try:
                if decrypt_text(u.get('cpf', '')) == cpf:
                    return u
            except Exception:
                if u.get('cpf') == cpf:
                    return u
        return None

    def _next_id(self, lista):
        if not lista:
            return 1
        return max(item.get("id", 0) for item in lista) + 1


    def login(self, user):
        """Marca o usuário como logado."""
        self.usuario_logado = user
        return True

    def logout(self):
        """Desloga o usuário atual."""
        self.usuario_logado = None
        return True

# ======================================================
# Funções de módulo (compatibilidade total)
# ======================================================

def load_usuarios():
    return DataStore.get_instance().usuarios

def load_alunos():
    return DataStore.get_instance().alunos

def load_cursos():
    return DataStore.get_instance().cursos

def load_aulas():
    return DataStore.get_instance().aulas

def load_avaliacoes():
    return DataStore.get_instance().avaliacoes

def save_usuarios():
    _save_json(USERS_FILE, DataStore.get_instance().usuarios)

def save_alunos():
    _save_json(ALUNOS_FILE, DataStore.get_instance().alunos)

def save_cursos():
    _save_json(CURSOS_FILE, DataStore.get_instance().cursos)


# CRUD wrappers
def criar_curso(curso):
    return DataStore.get_instance().criar_curso(curso)

def atualizar_curso(curso_id, novo):
    return DataStore.get_instance().atualizar_curso(curso_id, novo)

def deletar_curso(curso_id):
    return DataStore.get_instance().deletar_curso(curso_id)

def criar_aula(aula):
    return DataStore.get_instance().criar_aula(aula)

def atualizar_aula(aula_id, novo):
    return DataStore.get_instance().atualizar_aula(aula_id, novo)

def deletar_aula(aula_id):
    return DataStore.get_instance().deletar_aula(aula_id)

def atualizar_usuario(user_id, novo):
    return DataStore.get_instance().atualizar_usuario(user_id, novo)

def cadastrar_usuario(user):
    return DataStore.get_instance().cadastrar_usuario(user)


# Aliases em inglês
def atualizar_curso(curso_id, novo):
    return DataStore.get_instance().atualizar_curso(curso_id, novo)

def deletar_curso(curso_id):
    return DataStore.get_instance().deletar_curso(curso_id)

def atualizar_aula(aula_id, novo):
    return DataStore.get_instance().atualizar_aula(aula_id, novo)

def deletar_aula(aula_id):
    return DataStore.get_instance().deletar_aula(aula_id)

def cadastrar_usuario(user):
    return DataStore.get_instance().cadastrar_usuario(user)

def atualizar_usuario(user_id, novo):
    return DataStore.get_instance().atualizar_usuario(user_id, novo)


# ADDED: module-level compatibility wrappers for the verify functions
def verify_credentials_email(email, senha):
    return DataStore.get_instance().verify_credentials_email(email, senha)

def verify_credentials_cpf(cpf, senha):
    return DataStore.get_instance().verify_credentials_cpf(cpf, senha)


# Migração de senhas antigas
def migrate_passwords():
    ds = DataStore.get_instance()
    changed = False
    for user in ds.usuarios:
        if "senha" in user:
            plain = user["senha"]
            try:
                salt, hsh = hash_password(plain)
                user["senha_salt"] = salt
                user["senha_hash"] = hsh
                del user["senha"]
                changed = True
            except:
                pass
    if changed:
        _save_json(USERS_FILE, ds.usuarios)
    return changed


# Lookups
def get_curso_by_id(cid):
    for c in load_cursos():
        if c.get("id") == cid:
            return c
    return None


def find_usuario_por_cpf(cpf):
    return DataStore.get_instance().find_usuario_por_cpf(cpf)

def get_aluno_by_id(aid):
    for a in load_alunos():
        if a.get("id") == aid:
            return a
    return None



def adicionar_nota(aluno_id, professor_id, valor, descricao=""):
    """
    Adiciona uma nota ao arquivo de notas (dicionário com id, aluno_id, professor_id, valor, descricao, timestamp)
    """
    import datetime as _dt
    ds = DataStore.get_instance()
    nota = {
        "id": ds._next_id(ds.notas),
        "aluno_id": aluno_id,
        "professor_id": professor_id,
        "valor": valor,
        "descricao": descricao,
        "data": _dt.datetime.now().isoformat()
    }
    ds.notas.append(nota)
    _save_json(NOTAS_FILE, ds.notas)
    return nota

def load_notas():
    return DataStore.get_instance().notas

def save_notas():
    _save_json(NOTAS_FILE, DataStore.get_instance().notas)
__all__ = [
    "adicionar_nota",
    "load_notas",
    "save_notas",

    "DataStore",
    "backup_data",
    "migrate_passwords",

    "load_usuarios",
    "load_alunos",
    "load_cursos",
    "load_aulas",
    "load_avaliacoes",

    "save_usuarios",
    "save_alunos",
    "save_cursos",

    "criar_curso",
    "atualizar_curso",
    "deletar_curso",
    "criar_aula",
    "atualizar_aula",
    "deletar_aula",

    "cadastrar_usuario",
    "atualizar_usuario",

    "atualizar_curso",
    "deletar_curso",
    "atualizar_aula",
    "deletar_aula",
    "cadastrar_usuario",
    "atualizar_usuario",

    # exporta os wrappers de compatibilidade de login
    "verify_credentials_email",
    "verify_credentials_cpf",

    "get_curso_by_id",
    "get_aluno_by_id",

    "encrypt_text",
    "decrypt_text",
    "hash_password",
    "verify_password",
]
