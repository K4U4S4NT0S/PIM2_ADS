# integrated_data_store.py
# DataStore central para o PIM — persistência em JSON + funções de compatibilidade
import json
import os
import base64
from typing import Any, Dict, List, Optional

# ================================
# Arquivos e pastas
# ================================

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "usuarios.json")
ALUNOS_FILE = os.path.join(DATA_DIR, "alunos.json")
CURSOS_FILE = os.path.join(DATA_DIR, "cursos.json")
NOTAS_FILE = os.path.join(DATA_DIR, "notas.json")
AULAS_FILE = os.path.join(DATA_DIR, "aulas.json")
AVALIACOES_FILE = os.path.join(DATA_DIR, "avaliacoes.json")

# Garante diretório e arquivos existirem
def _ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    for f in [USERS_FILE, ALUNOS_FILE, CURSOS_FILE, NOTAS_FILE, AULAS_FILE, AVALIACOES_FILE]:
        if not os.path.exists(f):
            with open(f, "w", encoding="utf-8") as fh:
                fh.write("[]")

_ensure_data_files()

# ----------------
# Utilitários
# ----------------
def _load_json(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return []
            return json.loads(raw)
    except Exception:
        return []

def _save_json(path: str, data: List[Dict[str, Any]]):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    try:
        os.replace(tmp, path)
    except Exception:
        os.remove(tmp)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# Simulação simples de criptografia base64
def decrypt_text(texto: str) -> str:
    try:
        return base64.b64decode(texto.encode()).decode()
    except Exception:
        return texto

def encrypt_text(texto: str) -> str:
    try:
        return base64.b64encode(texto.encode()).decode()
    except Exception:
        return texto


# ================================
# Classe DataStore (Singleton)
# ================================
class DataStore:
    _instance = None  # Singleton

    @classmethod
    def get_instance(cls):
        """Retorna instância única do DataStore."""
        if cls._instance is None:
            cls._instance = DataStore()
        return cls._instance

    def __init__(self):
        # Evita recriação se já existe instância
        if DataStore._instance is not None:
            return

        self.usuarios = _load_json(USERS_FILE)
        self.alunos = _load_json(ALUNOS_FILE)
        self.cursos = _load_json(CURSOS_FILE)
        self.notas = _load_json(NOTAS_FILE)
        self.aulas = _load_json(AULAS_FILE)
        self.avaliacoes = _load_json(AVALIACOES_FILE)

        self.usuario_logado: Optional[Dict[str,Any]] = None

    def _next_id(self, collection, key="id"):
        try:
            vals = [int(item.get(key, 0)) for item in collection if str(item.get(key, 0)).isdigit()]
            return max(vals, default=0) + 1
        except:
            return len(collection) + 1


    # ==========================
    # Usuários
    # ==========================
    def add_usuario(self, usuario):
        if "id" not in usuario:
            usuario["id"] = self._next_id(self.usuarios)
        self.usuarios.append(usuario)
        _save_json(USERS_FILE, self.usuarios)
        return usuario

    def update_usuario(self, usuario_id, novos_dados):
        for u in self.usuarios:
            if u.get("id") == usuario_id:
                u.update(novos_dados)
                _save_json(USERS_FILE, self.usuarios)
                return True
        return False

    def find_usuario_por_cpf(self, cpf):
        for u in self.usuarios:
            if decrypt_text(u.get("cpf", "")) == cpf:
                return u
        return None

    def verify_credentials_cpf(self, cpf, senha):
        cpf_enc = encrypt_text(cpf)
        for user in self.usuarios:
            if user.get("cpf") == cpf_enc and user.get("senha") == senha:
                return user
        return None

    def autenticar(self, email_or_enc, senha):
        for user in self.usuarios:
            if user.get("email") == email_or_enc and user.get("senha") == senha:
                self.usuario_logado = user
                return user
        return None


    # ==========================
    # Alunos
    # ==========================
    def cadastrar_aluno(self, aluno):
        if "id" not in aluno:
            aluno["id"] = self._next_id(self.alunos)
        self.alunos.append(aluno)
        _save_json(ALUNOS_FILE, self.alunos)
        return aluno

    def buscar_aluno_por_id(self, aluno_id):
        for aluno in self.alunos:
            if aluno.get("id") == aluno_id:
                return aluno
        return None


    # ==========================
    # Cursos
    # ==========================
    def cadastrar_curso(self, curso):
        if "id" not in curso:
            curso["id"] = self._next_id(self.cursos)
        self.cursos.append(curso)
        _save_json(CURSOS_FILE, self.cursos)
        return curso

    def buscar_curso(self, curso_id):
        for curso in self.cursos:
            if curso.get("id") == curso_id:
                return curso
        return None

    def atualizar_curso(self, curso_id, novos):
        for c in self.cursos:
            if c.get("id") == curso_id:
                c.update(novos)
                _save_json(CURSOS_FILE, self.cursos)
                return True
        return False

    def remover_curso(self, curso_id):
        before = len(self.cursos)
        self.cursos = [c for c in self.cursos if c.get("id") != curso_id]
        if len(self.cursos) < before:
            _save_json(CURSOS_FILE, self.cursos)
            return True
        return False


    # ==========================
    # Aulas
    # ==========================
    def criar_aula(self, aula):
        if "id" not in aula:
            aula["id"] = self._next_id(self.aulas)
        self.aulas.append(aula)
        _save_json(AULAS_FILE, self.aulas)
        return aula

    def update_aula(self, aula_id, novos_dados):
        for a in self.aulas:
            if a.get("id") == aula_id:
                a.update(novos_dados)
                _save_json(AULAS_FILE, self.aulas)
                return True
        return False

    def delete_aula(self, aula_id):
        original = len(self.aulas)
        self.aulas = [a for a in self.aulas if a.get("id") != aula_id]
        if len(self.aulas) < original:
            _save_json(AULAS_FILE, self.aulas)
            return True
        return False


    # ==========================
    # Notas
    # ==========================
    def registrar_nota(self, aluno_id, disciplina, nota):
        for n in self.notas:
            if n.get("aluno_id") == aluno_id and n.get("disciplina") == disciplina:
                n["nota"] = nota
                _save_json(NOTAS_FILE, self.notas)
                return
        self.notas.append({"aluno_id": aluno_id, "disciplina": disciplina, "nota": nota})
        _save_json(NOTAS_FILE, self.notas)

    def buscar_notas_do_aluno(self, aluno_id):
        return [n for n in self.notas if n.get("aluno_id") == aluno_id]


    # ==========================
    # Login / Sessão
    # ==========================
    def get_usuario_logado(self):
        return self.usuario_logado

    def login(self, usuario):
        self.usuario_logado = usuario

    def logout(self):
        self.usuario_logado = None



# ================================
# Funções Wrapper — compatibilidade
# ================================
def _ds():
    return DataStore.get_instance()

def load_cursos():
    return _ds().cursos

def criar_curso(nome, descricao):
    ds = _ds()
    return ds.cadastrar_curso({"nome": nome, "descricao": descricao})

def update_curso(curso_id, novos: dict):
    ds = _ds()
    return ds.atualizar_curso(curso_id, novos)

def delete_curso(curso_id):
    return _ds().remover_curso(curso_id)

def load_aulas():
    return _ds().aulas

def criar_aula(curso_id: int, titulo: str, descricao: str, autor: str):
    ds = _ds()
    aula = {
        "curso_id": curso_id,
        "titulo": titulo,
        "descricao": descricao,
        "autor": autor
    }
    return ds.criar_aula(aula)

def update_aula(aula_id, novos):
    return _ds().update_aula(aula_id, novos)

def delete_aula(aula_id):
    return _ds().delete_aula(aula_id)

def add_usuario(usuario):
    return _ds().add_usuario(usuario)

def update_usuario(usuario_id, novos):
    return _ds().update_usuario(usuario_id, novos)
