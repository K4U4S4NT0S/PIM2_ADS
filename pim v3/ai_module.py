# ai_module.py - simple rule-based assistant (FAQ + recommender)
from integrated_data_store import load_cursos, load_aulas, decrypt_text
import logger_utils

FAQ = {
    "como me cadastrar": "Para se cadastrar, escolha Cadastro no menu inicial e preencha os dados solicitados.",
    "esqueci a senha": "Para redefinir a senha, faco login e use a opcao de alterar senha no perfil. Se perdeu acesso, contate o admin.",
    "como criar curso": "Apenas o admin pode criar cursos no menu Gerenciar Cursos.",
    "avaliacao": "Alunos podem avaliar aulas acessando o curso, selecionando a aula e usando a funcao de avaliar."
}

def answer_faq(question: str) -> str:
    q = question.lower().strip()
    for k,v in FAQ.items():
        if k in q:
            return v
    return "Desculpe, nao entendi. Tente palavras-chave como: 'como me cadastrar', 'esqueci a senha', 'avaliacao'."

def recommend_courses_for_user(user):
    cursos = load_cursos()
    aulas = load_aulas()
    if not cursos:
        return []
    counts = {c['id']: 0 for c in cursos}
    for a in aulas:
        cid = a.get('curso_id')
        if cid in counts:
            counts[cid] += 1
    sorted_ids = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    recommended = []
    for cid, cnt in sorted_ids[:5]:
        for c in cursos:
            if c.get('id') == cid:
                recommended.append(c)
    return recommended

def log_query(user, query):
    try:
        logger_utils.registrar_evento("INFO", f"IA query: {query}", usuario=(decrypt_text(user.get('email')) if user.get('email') else decrypt_text(user.get('cpf'))))
    except Exception:
        logger_utils.registrar_evento("INFO", f"IA query: {query}", usuario=None)