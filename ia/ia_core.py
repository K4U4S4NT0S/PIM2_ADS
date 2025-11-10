
def resposta_simples(pergunta, contexto=None):
    p = pergunta.lower().strip()
    if 'nota' in p or 'melhorar' in p:
        return "Revise exercícios, pratique resolução de problemas e revise listas de estruturas de dados (listas e dicionários)."
    if 'como usar sistema' in p or 'ajuda' in p:
        return "Use os comandos do menu. Para dúvidas específicas digite 'ajuda' seguido do tema."
    return "Desculpe, não entendi totalmente. Reformule a pergunta com mais detalhes."
