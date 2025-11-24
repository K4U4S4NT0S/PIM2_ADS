
# logger_utils_fixed.py - logger simples que escreve em arquivo e colore saída por tipo
import logging
import os
from datetime import datetime

# Cores ANSI
COLORS = {
    "DEBUG": "\033[94m",   # azul claro
    "INFO": "\033[92m",    # verde
    "WARN": "\033[93m",    # amarelo
    "ERROR": "\033[91m",   # vermelho
    "RESET": "\033[0m"
}

LOG_FILE = os.path.join(os.path.dirname(__file__), "server.log")

# Configuração básica do logging para arquivo (sem cores)
logger = logging.getLogger("sys_academy_logger")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

def _write_file(level, message, usuario=None):
    user_info = f" user={usuario}" if usuario else ""
    logger.log(getattr(logging, level if level in ["DEBUG","INFO","WARN","ERROR"] else "INFO"), f"{message}{user_info}")

def log(level, message, usuario=None):
    """
    level: DEBUG, INFO, WARN, ERROR
    message: texto
    usuario: id ou email do usuário que gerou a ação (opcional)
    """
    try:
        # grava no arquivo
        _write_file(level, message, usuario)
        # imprime colorido no terminal
        color = COLORS.get(level, "")
        reset = COLORS["RESET"]
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_info = f" user={usuario}" if usuario else ""
        print(f"{color}{ts} [{level}] {message}{user_info}{reset}")
    except Exception as e:
        # fallback silencioso (não interrompe execução)
        try:
            logger.exception("Erro ao registrar log: %s", e)
        except:
            pass



# --- Compatibilidade: funções antigas usadas pelo projeto ---
def registrar_evento(level, message, usuario=None):
    """
    Compatibilidade com código antigo que chamava logger_utils.registrar_evento(...).
    Level: 'INFO', 'WARN', 'ERROR', 'DEBUG' (ou lower)
    """
    try:
        lvl = level.upper() if isinstance(level, str) else "INFO"
        # map 'WARN' to our 'WARN'
        if lvl == "WARNING":
            lvl = "WARN"
        log(lvl, message, usuario=usuario)
    except Exception as e:
        try:
            logger.exception("Erro em registrar_evento: %s", e)
        except:
            pass

def ler_eventos():
    """
    Lê o conteúdo do arquivo de log (server.log) e retorna como string.
    Compatível com chamadas antigas que esperavam essa função.
    """
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""
