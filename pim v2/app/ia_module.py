import json, os
LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'ia_logs.json'))
def _log(prompt,resposta,usuario_id=None):
    try:
        data = json.load(open(LOG,'r',encoding='utf-8'))
    except:
        data = []
    data.append({'usuario_id':usuario_id,'prompt':prompt,'resposta':resposta})
    with open(LOG,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
def gerar_comentario(nota,contexto='',usuario_id=None):
    prompt = f'Gerar comentario para nota {nota} e contexto: {contexto}'
    resposta = f'Aluno obteve nota {nota}. Comentario automatizado: "Bom trabalho"' if nota>=7 else f'Aluno obteve nota {nota}. Sugere revisão e estudo focado.'
    _log(prompt,resposta,usuario_id)
    return resposta
def detectar_outliers(notas):
    if not notas: return []
    mean = sum(notas)/len(notas)
    stdev = (sum((x-mean)**2 for x in notas)/len(notas))**0.5
    out = [x for x in notas if abs(x-mean) > 2*stdev]
    return out
