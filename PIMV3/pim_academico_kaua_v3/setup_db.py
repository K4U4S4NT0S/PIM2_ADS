import sqlite3, os, bcrypt
DB = os.path.join(os.path.dirname(__file__), 'data', 'pim.db')
os.makedirs(os.path.dirname(DB), exist_ok=True)
conn = sqlite3.connect(DB)
c = conn.cursor()
# users
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT UNIQUE,
    cpf TEXT UNIQUE,
    username TEXT,
    senha_hash TEXT,
    role TEXT,
    nascimento TEXT,
    genero TEXT,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
)''')
# turmas, aulas, atividades, diario, auditoria, ia_logs
c.execute('''CREATE TABLE IF NOT EXISTS turmas (id INTEGER PRIMARY KEY AUTOINCREMENT,codigo TEXT UNIQUE,nome TEXT,periodo TEXT,criado_em TEXT DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS aulas (id INTEGER PRIMARY KEY AUTOINCREMENT,turma_id INTEGER,data TEXT,conteudo TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS atividades (id INTEGER PRIMARY KEY AUTOINCREMENT,turma_id INTEGER,titulo TEXT,descricao TEXT,arquivo_path TEXT,data_entrega TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS diario (id INTEGER PRIMARY KEY AUTOINCREMENT,aula_id INTEGER,aluno_id INTEGER,presenca INTEGER DEFAULT 0,nota REAL,observacao TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS auditoria (id INTEGER PRIMARY KEY AUTOINCREMENT,usuario_id INTEGER,acao TEXT,alvo TEXT,timestamp TEXT DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS ia_logs (id INTEGER PRIMARY KEY AUTOINCREMENT,usuario_id INTEGER,prompt TEXT,resposta TEXT,contexto TEXT,criado_em TEXT DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()
def add_user(nome,email,cpf,senha,role,nascimento,genero):
    try:
        h = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        c.execute('INSERT INTO usuarios (nome,email,cpf,senha_hash,role,nascimento,genero) VALUES (?,?,?,?,?,?,?)', (nome,email,cpf,h,role,nascimento,genero))
        conn.commit()
    except Exception as e:
        pass
add_user('Admin Demo','admin@demo.local',None,'admin123','admin','1990-01-01','Outro')
add_user('Prof Demo',None,'12345678901','prof123','professor','1980-05-05','Masculino')
add_user('Aluno Demo','aluno@demo.local',None,'aluno123','aluno','2003-07-07','Feminino')
print('DB criado em',DB)
conn.close()
