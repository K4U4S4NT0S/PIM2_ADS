# logger_utils.py - grava eventos em logs/ (jsonl minimal)
import os
import json
import datetime
import traceback

BASE = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE, "logs")

# Garante que o diretório de logs exista
os.makedirs(LOG_DIR, exist_ok=True)

def _log_path():
    """Gera o caminho completo para o arquivo de log do dia atual."""
    return os.path.join(LOG_DIR, f"logs_{datetime.date.today().strftime('%Y-%m-%d')}.jsonl")

def registrar_evento(tipo, mensagem, usuario=None):
    """
    Registra um evento no log do dia em formato JSONL:
    {"timestamp": "YYYY-MM-DD HH:MM:SS", "type": "INFO"/"ERROR"/..., "usuario": "<valor ou null>", "mensagem": "..."}
    Retorna True se gravou com sucesso, False caso contrário.
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "type": tipo,
            "usuario": usuario,
            "mensagem": mensagem
        }
        path = _log_path()
        # Abre em modo append e escreve uma linha JSON por evento
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return True
    except Exception as e:
        # Se houver falha na escrita do log, escrevemos em stderr (não quebrar aplicação)
        try:
            err_path = os.path.join(LOG_DIR, "logger_errors.txt")
            with open(err_path, "a", encoding="utf-8") as ef:
                ef.write(f"{datetime.datetime.now().isoformat()} - ERRO ao registrar evento: {e}\n")
                ef.write(traceback.format_exc() + "\n")
        except Exception:
            # último recurso: print
            print("Erro ao gravar log e erro ao gravar logger_errors.txt:", e)
        return False

def ler_eventos():
    """
    Lê todos os eventos registrados no log do dia atual e retorna
    uma lista de dicionários. Se não houver arquivo, retorna lista vazia.
    """
    path = _log_path()
    if not os.path.exists(path):
        return []

    eventos = []
    with open(path, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            try:
                eventos.append(json.loads(linha))
            except json.JSONDecodeError:
                # Ignora linhas inválidas
                continue

    return eventos

def ler_eventos_dia():
    return ler_eventos()