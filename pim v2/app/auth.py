from .db import query
import bcrypt
def register_aluno(nome,email,nascimento,genero,senha):
    h = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    query('INSERT INTO usuarios (nome,email,senha_hash,role,nascimento,genero) VALUES (?,?,?,?,?,?)', (nome,email,h,'aluno',nascimento,genero))
    return query('SELECT * FROM usuarios WHERE email=?',(email,),fetch=True)[0]
def register_professor(nome,cpf,nascimento,genero,senha):
    h = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    query('INSERT INTO usuarios (nome,cpf,senha_hash,role,nascimento,genero) VALUES (?,?,?,?,?,?)', (nome,cpf,h,'professor',nascimento,genero))
    return query('SELECT * FROM usuarios WHERE cpf=?',(cpf,),fetch=True)[0]
def authenticate_aluno(email,senha):
    users = query('SELECT * FROM usuarios WHERE email=?',(email,),fetch=True)
    if not users: return None
    u = users[0]
    if bcrypt.checkpw(senha.encode('utf-8'), u['senha_hash'].encode('utf-8')): return u
    return None
def authenticate_professor(cpf,senha):
    users = query('SELECT * FROM usuarios WHERE cpf=?',(cpf,),fetch=True)
    if not users: return None
    u = users[0]
    if bcrypt.checkpw(senha.encode('utf-8'), u['senha_hash'].encode('utf-8')): return u
    return None
