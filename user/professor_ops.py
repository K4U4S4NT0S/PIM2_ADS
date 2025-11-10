
from utils.filedb import load_json, save_json
from utils.logs import info
import os, uuid

ATIV_F = os.path.join('/mnt/data/pim2_code', 'data', 'atividades.json')
AULAS_F = os.path.join('/mnt/data/pim2_code', 'data', 'aulas.json')

def lancar_atividade(turma_codigo, titulo, descricao, data_entrega):
    atividades = load_json(ATIV_F, [])
    novo = {'id': str(uuid.uuid4())[:8], 'turma_codigo': turma_codigo, 'titulo': titulo, 'descricao': descricao, 'data_entrega': data_entrega, 'entregas': []}
    atividades.append(novo)
    save_json(ATIV_F, atividades)
    info(f"Atividade lançada: {titulo} para {turma_codigo}")
    return novo

def registrar_aula(turma_codigo, data, conteudo):
    aulas = load_json(AULAS_F, [])
    novo = {'id': str(uuid.uuid4())[:8], 'turma_codigo':turma_codigo, 'data':data, 'conteudo':conteudo, 'presencas':[]}
    aulas.append(novo)
    save_json(AULAS_F, aulas)
    info(f"Aula registrada: {data} - {turma_codigo}")
    return novo
