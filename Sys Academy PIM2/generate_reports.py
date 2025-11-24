
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, datetime

def gerar_relatorio_aluno(user, notas=None, out_dir=None):
    """
    Gera um PDF simples com informações do aluno e suas notas.
    user: dict com campos id, name, email, etc.
    notas: list of dicts [{'disciplina':..., 'nota':...}, ...]
    """
    if out_dir is None:
        base = os.path.dirname(__file__)
        out_dir = os.path.join(base, 'reports')
    os.makedirs(out_dir, exist_ok=True)
    fname = f"relatorio_aluno_{user.get('id')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(out_dir, fname)
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    x = 50
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, f"Relatório do Aluno: {user.get('name') or user.get('nome') or '' or user.get('nome') or ''}")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(x, y, f"ID: {user.get('id')}")
    y -= 20
    c.drawString(x, y, f"Email: {user.get('email','-')}")
    y -= 20
    c.drawString(x, y, f"CPF: {user.get('cpf','-')}")
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Notas:")
    y -= 20
    c.setFont("Helvetica", 12)
    if notas:
        for n in notas:
            c.drawString(x, y, f"- {n.get('disciplina','')} : {n.get('nota','-')}")
            y -= 18
            if y < 80:
                c.showPage()
                y = height - 50
    else:
        c.drawString(x, y, "Nenhuma nota registrada.")
    c.showPage()
    c.save()
    return path


def gerar_boletim_aluno(user, matriculas=None, notas=None, out_dir=None):
    """Gera um boletim escolar para o aluno com média por aula e situação (Aprovado/Reprovado)."""
    if out_dir is None:
        base = os.path.dirname(__file__)
        out_dir = os.path.join(base, 'reports')
    os.makedirs(out_dir, exist_ok=True)
    fname = f"boletim_{user.get('id')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(out_dir, fname)
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    x = 50
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, f"Boletim Escolar: {user.get('name') or user.get('nome') or ''}")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(x, y, f"Idade: {user.get('idade','-')}   Genero: {user.get('genero','-')}")
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Cursos & Aulas:")
    y -= 20
    # build mapping aula_id -> notas list
    notas_map = {}
    if notas:
        for n in notas:
            notas_map.setdefault(int(n.get('aula_id', -1)), []).append(float(n.get('nota', 0)))
    # list enrolled aulas
    if matriculas:
        for m in matriculas:
            aid = int(m.get('aula_id', -1))
            # find aula and curso
            aula = None
            # try to load from data files
            # we'll attempt to open data/aulas.json
            try:
                base = os.path.dirname(__file__)
                with open(os.path.join(base, 'data', 'aulas.json'), encoding='utf-8') as f:
                    aulas_all = json.load(f)
            except Exception:
                aulas_all = []
            aula = next((a for a in aulas_all if int(a.get('id', -1)) == aid), None)
            titulo = aula.get('titulo', aula.get('nome','-')) if aula else str(aid)
            notas_list = notas_map.get(aid, [])
            media = sum(notas_list)/len(notas_list) if notas_list else 0
            situ = 'Aprovado' if media >= 6 else 'Reprovado'
            c.setFont('Helvetica', 12)
            c.drawString(x, y, f"- Aula: {titulo} | Media: {media:.2f} | Situacao: {situ}")
            y -= 18
            if y < 80:
                c.showPage()
                y = height - 50
    else:
        c.drawString(x, y, 'Nenhuma matricula registrada.')

    # Notas do aluno (se houver)
    try:
        aluno_notas = [n for n in (notas or []) if int(n.get('aluno_id', -1)) == int(user.get('id', -1))]
    except Exception:
        aluno_notas = []
    if aluno_notas:
        y -= 10
        c.setFont('Helvetica-Bold', 14)
        c.drawString(x, y, 'Notas Registradas:')
        y -= 20
        soma = 0
        cont = 0
        for n in aluno_notas:
            val = n.get('valor') if n.get('valor') is not None else n.get('nota') if n.get('nota') is not None else None
            try:
                v = float(val)
            except:
                v = None
            desc = n.get('descricao') or n.get('desc') or ''
            if v is not None:
                soma += v
                cont += 1
            c.setFont('Helvetica', 12)
            c.drawString(x, y, f"- Nota: {v if v is not None else '-'} | {desc}")
            y -= 16
            if y < 80:
                c.showPage()
                y = height - 50
        media_geral = (soma/cont) if cont else 0
        y -= 8
        c.setFont('Helvetica-Bold', 12)
        c.drawString(x, y, f'Média geral: {media_geral:.2f}')
    
    c.showPage()
    c.save()
    return path
