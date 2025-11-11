def ask_ai(prompt: str) -> str:
    """
    Simples engine de respostas baseada em palavras-chave para simular IA local.
    """
    p = prompt.lower()
    if "nota" in p or "notas" in p:
        return "Para ver suas notas, vá ao menu de aluno e escolha 'Notas'."
    if "perfil" in p:
        return "Você pode editar seu perfil no menu de aluno ou professor. Procure a opção 'Perfil'."
    if "avaliar" in p:
        return "Para avaliar um curso ou aula, entre em 'Cursos' e escolha 'avaliar'."
    if "ajuda" in p or "suporte" in p:
        return "Entre em contato com o administrador ou verifique a documentação."
    return "Desculpe, ainda estou aprendendo. Tente reformular sua pergunta."
