# integrated_data_store.py - dados (XOR+base64 para campos sensiveis; pbkdf2 para senha)
import os, json, base64, secrets, hashlib
BASE = os.path.dirname(__file__)
USERS_FILE = os.path.join(BASE, "data", "usuarios.json")
CURSOS_FILE = os.path.join(BASE, "data", "cursos.json")
AULAS_FILE = os.path.join(BASE, "data", "aulas.json")
AVAL_FILE = os.path.join(BASE, "data", "avaliacoes.json")
SECRET_FILE = os.path.join(BASE, "secret.key")

def _ensure_secret():
    if not os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "wb") as f:
            f.write(secrets.token_bytes(32))
    return open(SECRET_FILE, "rb").read()

_SECRET = _ensure_secret()

def _xor_bytes(b: bytes) -> bytes:
    key = _SECRET
    return bytes([b[i] ^ key[i % len(key)] for i in range(len(b))])

def encrypt_text(s: str) -> str:
    if not s: return ""
    return base64.b64encode(_xor_bytes(s.encode("utf-8"))).decode("utf-8")

def decrypt_text(s: str) -> str:
    if not s: return ""
    try:
        return _xor_bytes(base64.b64decode(s.encode("utf-8"))).decode("utf-8")
    except:
        return ""

def _load(path):
    if not os.path.exists(path): return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def hash_password(pw: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, 100000)
    return base64.b64encode(salt+dk).decode("utf-8")

def verify_password(pw: str, hashed: str) -> bool:
    try:
        raw = base64.b64decode(hashed.encode("utf-8"))
        salt = raw[:16]; dk = raw[16:]
        check = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, 100000)
        return check == dk
    except:
        return False

def next_usuario_id() -> int:
    us = _load(USERS_FILE)
    return (max([u.get("id",0) for u in us]) + 1) if us else 1

def add_usuario(user: dict) -> dict:
    us = _load(USERS_FILE)
    role = user.get("role","aluno")
    if role == "aluno" and user.get("email"):
        for u in us:
            if decrypt_text(u.get("email","")) == user.get("email"):
                raise ValueError("email_exists")
    if role == "professor" and user.get("cpf"):
        for u in us:
            if decrypt_text(u.get("cpf","")) == user.get("cpf"):
                raise ValueError("cpf_exists")
    uid = next_usuario_id()
    pwd = user.get("password","")
    pwd_h = hash_password(pwd)
    stored = {
        "id": uid,
        "role": role,
        "name": user.get("name",""),
        "email": encrypt_text(user.get("email","")),
        "cpf": encrypt_text(user.get("cpf","")),
        "dob": user.get("dob",""),
        "genero": user.get("genero",""),
        "password_hash": pwd_h
    }
    us.append(stored)
    _save(USERS_FILE, us)
    return stored

def find_usuario_por_email(email: str):
    if not email: return None
    for u in _load(USERS_FILE):
        if decrypt_text(u.get("email","")) == email:
            return u
    return None

def find_usuario_por_cpf(cpf: str):
    if not cpf: return None
    for u in _load(USERS_FILE):
        if decrypt_text(u.get("cpf","")) == cpf:
            return u
    return None

def verify_credentials_email(email: str, password: str):
    u = find_usuario_por_email(email)
    if not u: return None
    if verify_password(password, u.get("password_hash","")):
        return u
    return None

def verify_credentials_cpf(cpf: str, password: str):
    u = find_usuario_por_cpf(cpf)
    if not u: return None
    if verify_password(password, u.get("password_hash","")):
        return u
    return None

def update_usuario(u_id:int, updates:dict):
    us = _load(USERS_FILE)
    changed = False
    for i,u in enumerate(us):
        if u.get("id") == u_id:
            if "email" in updates: u["email"] = encrypt_text(updates["email"])
            if "cpf" in updates: u["cpf"] = encrypt_text(updates["cpf"])
            if "name" in updates: u["name"] = updates["name"]
            if "dob" in updates: u["dob"] = updates["dob"]
            if "genero" in updates: u["genero"] = updates["genero"]
            if "password" in updates:
                u["password_hash"] = hash_password(updates["password"])
            us[i] = u
            changed = True
            break
    if changed:
        _save(USERS_FILE, us)
        return u
    raise ValueError("user_not_found")

def load_cursos(): return _load(CURSOS_FILE)
def save_cursos(data): _save(CURSOS_FILE, data)
def load_aulas(): return _load(AULAS_FILE)
def save_aulas(data): _save(AULAS_FILE, data)
def load_avaliacoes(): return _load(AVAL_FILE)
def save_avaliacoes(data): _save(AVAL_FILE, data)

def aulas_por_curso(curso_id):
    return [a for a in load_aulas() if a.get("curso_id")==curso_id]

def adicionar_avaliacao(aula_id, usuario_id, nota, comentario=""):
    avals = load_avaliacoes()
    try:
        nota = int(nota)
    except:
        nota = 1
    nota = max(1, min(5, nota))
    for i,a in enumerate(avals):
        if a.get("aula_id")==aula_id and a.get("usuario_id")==usuario_id:
            avals[i]["nota"]=nota; avals[i]["comentario"]=comentario; save_avaliacoes(avals); return avals[i]
    nova = {"aula_id":aula_id,"usuario_id":usuario_id,"nota":nota,"comentario":comentario}
    avals.append(nova); save_avaliacoes(avals); return nova

def calcular_media_aula(aula_id):
    try:
        avaliacoes = load_avaliacoes()
        avaliacoes_aula = [a for a in avaliacoes if a.get("aula_id") == aula_id]
        if not avaliacoes_aula:
            return 0.0
        soma = sum(a.get("nota", 0) for a in avaliacoes_aula)
        media = soma / len(avaliacoes_aula)
        return round(media, 2)
    except Exception as e:
        print(f"[ERRO] {e}")
        return 0.0

def criar_aula(curso_id, titulo, descricao, professor_id):
    aulas = load_aulas()
    nova_id = (max([a.get("id",0) for a in aulas]) + 1) if aulas else 1
    nova = {"id": nova_id, "curso_id": curso_id, "titulo": titulo, "descricao": descricao, "professor_id": professor_id}
    aulas.append(nova); save_aulas(aulas); return nova

def update_aula(aula_id, updates):
    aulas = load_aulas()
    for i,a in enumerate(aulas):
        if a.get("id")==aula_id:
            aulas[i].update(updates); save_aulas(aulas); return aulas[i]
    raise ValueError("aula_not_found")

def delete_aula(aula_id):
    aulas = load_aulas()
    novas = [a for a in aulas if a.get("id")!=aula_id]
    save_aulas(novas)
    return True

def get_avaliacoes_por_aula(aula_id):
    return [a for a in load_avaliacoes() if a.get("aula_id")==aula_id]

def criar_curso(titulo, descricao):
    cursos = load_cursos()
    novo_id = (max([c.get("id",0) for c in cursos]) + 1) if cursos else 1
    novo = {"id": novo_id, "nome": titulo, "descricao": descricao}
    cursos.append(novo); save_cursos(cursos); return novo

def update_curso(curso_id, updates):
    cursos = load_cursos()
    for i,c in enumerate(cursos):
        if c.get("id")==curso_id:
            cursos[i].update(updates); save_cursos(cursos); return cursos[i]
    raise ValueError("curso_not_found")

def delete_curso(curso_id):
    cursos = load_cursos()
    novas = [c for c in cursos if c.get("id")!=curso_id]
    save_cursos(novas)
    aulas = load_aulas()
    aulas = [a for a in aulas if a.get("curso_id")!=curso_id]
    save_aulas(aulas)
    return True

def _ensure_admin():
    us = _load(USERS_FILE)
    for u in us:
        if decrypt_text(u.get("email","")) == "admin" and u.get("role") == "admin":
            return
    add_usuario({"role":"admin","name":"Administrator","email":"admin","cpf":"","dob":"","genero":"","password":"admin"})
_ensure_admin()