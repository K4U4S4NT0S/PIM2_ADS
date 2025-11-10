
from utils.filedb import load_json, save_json
from utils.logs import info, error
import uuid, os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ALUNOS_F = os.path.join('/mnt/data/pim2_code', 'data', 'alunos.json')

def listar_alunos():
    return load_json(ALUNOS_F, [])

def cadastrar_aluno(nome, ra, email):
    alunos = listar_alunos()
    novo = {'id': str(uuid.uuid4())[:8], 'nome': nome, 'ra': ra, 'email': email, 'turmas': [], 'historico_notas': []}
    alunos.append(novo)
    save_json(ALUNOS_F, alunos)
    info(f"Aluno cadastrado: {nome}")
    return novo

def buscar_por_ra(ra):
    alunos = listar_alunos()
    for a in alunos:
        if a.get('ra') == ra:
            return a
    return None
