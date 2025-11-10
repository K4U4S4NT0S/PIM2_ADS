
from utils.filedb import load_json, save_json
from utils.logs import info
import os, uuid, datetime

ATIV_F = os.path.join('/mnt/data/pim2_code', 'data', 'atividades.json')

def listar_atividades(turma_codigo):
    atividades = load_json(ATIV_F, [])
    return [a for a in atividades if a.get('turma_codigo') == turma_codigo]

def enviar_entrega(atividade_id, aluno_id, referencia):
    atividades = load_json(ATIV_F, [])
    for a in atividades:
        if a.get('id') == atividade_id:
            entrega = {'aluno_id': aluno_id, 'arquivo_referencia': referencia, 'nota': None, 'data_envio': datetime.date.today().isoformat()}
            a.setdefault('entregas', []).append(entrega)
            save_json(ATIV_F, atividades)
            info(f"Entrega registrada: atividade {atividade_id} por {aluno_id}")
            return entrega
    return None
