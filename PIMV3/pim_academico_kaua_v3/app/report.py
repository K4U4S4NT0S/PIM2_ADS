import os, matplotlib.pyplot as plt
from .db import query
from datetime import datetime, date
GRAPHS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'graphs'))
os.makedirs(GRAPHS_DIR, exist_ok=True)
def _save_fig(fig, name):
    path = os.path.join(GRAPHS_DIR, f"{name}_{int(datetime.now().timestamp())}.png")
    fig.savefig(path); plt.close(fig); return path
def gender_dist():
    users = query('SELECT genero FROM usuarios', fetch=True)
    counts = {}
    for u in users:
        g = u.get('genero') or 'Outro'; counts[g] = counts.get(g,0)+1
    fig = plt.figure(); plt.bar(list(counts.keys()), list(counts.values())); plt.title('Distribuição de gêneros'); plt.tight_layout()
    return _save_fig(fig,'gender_dist')
def age_hist():
    users = query('SELECT nascimento FROM usuarios', fetch=True)
    ages = []
    for u in users:
        n = u.get('nascimento')
        if not n: continue
        try:
            dt = datetime.fromisoformat(n).date()
            today = date.today(); age = today.year - dt.year - ((today.month,today.day) < (dt.month,dt.day))
            ages.append(age)
        except:
            continue
    if not ages: ages=[18,20,22]
    fig = plt.figure(); plt.hist(ages, bins=range(10,70,5)); plt.title('Histograma de idades'); plt.tight_layout()
    return _save_fig(fig,'age_hist')
def avg_by_turma(turma_id=None):
    # turma_id optional: averages by turma (all) or single turma
    if turma_id:
        rows = query('SELECT d.nota FROM diario d JOIN aulas a ON d.aula_id=a.id WHERE a.turma_id=?',(turma_id,),fetch=True)
        notas = [r['nota'] for r in rows if r.get('nota') is not None]
        labels = [f'Turma {turma_id}']; values = [sum(notas)/len(notas) if notas else 0]
    else:
        rows = query('SELECT t.id, t.nome, d.nota FROM turmas t LEFT JOIN aulas a ON a.turma_id=t.id LEFT JOIN diario d ON d.aula_id=a.id', fetch=True)
        agg = {}
        for r in rows:
            tid = r['id']; agg.setdefault(tid,[])
            if r.get('nota') is not None: agg[tid].append(r['nota'])
        labels = [f"{k}" for k in agg.keys()]; values = [ (sum(v)/len(v)) if v else 0 for v in agg.values() ]
    fig = plt.figure(); plt.bar(labels, values); plt.title('Média de notas por turma'); plt.ylim(0,10); plt.tight_layout()
    return _save_fig(fig,'avg_by_turma')
def attendance_trend(turma_id):
    # compute % presence by aula date for given turma
    rows = query('SELECT a.id, a.data FROM aulas a WHERE a.turma_id=?',(turma_id,),fetch=True)
    dates = []
    rates = []
    for r in rows:
        aid = r['id']; d = r.get('data') or 'unknown'; pres = query('SELECT COUNT(*) as total, SUM(presenca) as pres FROM diario WHERE aula_id=?',(aid,),fetch=True)
        if pres:
            total = pres[0].get('total') or 0; presc = pres[0].get('pres') or 0
            pct = (presc/total*100) if total>0 else 0
            dates.append(d); rates.append(pct)
    fig = plt.figure(); plt.plot(dates or [0], rates or [0]); plt.title('Tendência de Presença'); plt.tight_layout()
    return _save_fig(fig,'attendance_trend')
def box_notas(turma_id=None):
    # boxplot of notas
    if turma_id:
        rows = query('SELECT d.nota FROM diario d JOIN aulas a ON d.aula_id=a.id WHERE a.turma_id=?',(turma_id,),fetch=True)
        notas = [r['nota'] for r in rows if r.get('nota') is not None]
    else:
        rows = query('SELECT nota FROM diario WHERE nota IS NOT NULL', fetch=True)
        notas = [r['nota'] for r in rows]
    if not notas: notas=[5,6,7,8,9]
    fig = plt.figure(); plt.boxplot(notas); plt.title('Boxplot de Notas'); plt.tight_layout()
    return _save_fig(fig,'box_notas')
