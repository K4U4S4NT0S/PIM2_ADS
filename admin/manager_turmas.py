
from utils.filedb import load_json, save_json
from utils.logs import info
import uuid, os

TURMAS_F = os.path.join('/mnt/data/pim2_code', 'data', 'turmas.json')

def listar_turmas():
    return load_json(TURMAS_F, [])

def buscar_por_codigo(codigo):
    turmas = listar_turmas()
    for t in turmas:
        if t.get('codigo') == codigo:
            return t
    return None

def adicionar_aluno_turma(turma_codigo, aluno_id):
    turmas = listar_turmas()
    for t in turmas:
        if t.get('codigo') == turma_codigo:
            if aluno_id not in t.get('alunos', []):
                t.setdefault('alunos', []).append(aluno_id)
                save_json(TURMAS_F, turmas)
                info(f"Aluno {aluno_id} adicionado à turma {turma_codigo}")
                return True
    return False
