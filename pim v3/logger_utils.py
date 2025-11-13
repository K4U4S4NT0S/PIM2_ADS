# logger_utils.py - grava eventos em logs/ (jsonl minimal)
import os
import json
import datetime

BASE = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE, "logs")

# Garante que o diretório de logs exista
os.makedirs(LOG_DIR, exist_ok=True)

def _log_path():
    """Gera o caminho completo para o arquivo de log do dia atual."""
    return os.path.join(LOG_DIR, f"logs_{datetime.date.today().strftime('%Y-%m-%d')}.jsonl")

def registrar_evento(tipo, mensagem, usuario=None):
    """Registra um evento no log em formato JSONL."""
    evento = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": tipo.upper(),
        "usuario": usuario,
        "mensagem": mensagem
    }

    try:
        with open(_log_path(), "a", encoding="utf-8") as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"[ERRO AO GRAVAR LOG] {e}")

def ler_eventos_dia():
    """Lê todos os eventos registrados no log do dia."""
    path = _log_path()
    if not os.path.exists(path):
        return []

    eventos = []
    with open(path, "r", encoding="utf-8") as f:
        for linha in f:
            try:
                eventos.append(json.loads(linha.strip()))
            except json.JSONDecodeError:
                continue

    return eventos
