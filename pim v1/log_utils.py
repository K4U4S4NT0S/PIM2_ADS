import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import json

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Configuração básica de logger combinado
combined_logger = logging.getLogger("actions_combined")
combined_logger.setLevel(logging.INFO)
combined_handler = RotatingFileHandler(os.path.join(LOG_DIR, "actions.log"), maxBytes=5_000_000, backupCount=5, encoding="utf-8")
combined_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
if not combined_logger.handlers:
    combined_logger.addHandler(combined_handler)

# Criador de log por role
def _get_role_logger(role: str):
    name = f"actions_{role}"
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    path = os.path.join(LOG_DIR, f"{role}.log")
    handler = RotatingFileHandler(path, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    # evitar multi-handlers se já configurado
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def log_action(actor_id: str, actor_name: str, role: str, action: str, target_type: str, target_id: str, details: dict = None):
    """
    Registra uma ação. role deve ser 'admin', 'professor' ou 'aluno'.
    action exemplo: 'create','edit','delete','login','logout'
    target_type: 'user','course','aula', etc.
    details: dicionário com informações adicionais.
    """
    ts = datetime.utcnow().isoformat()
    entry = {
        "timestamp": ts,
        "actor_id": actor_id,
        "actor_name": actor_name,
        "role": role,
        "action": action,
        "target_type": target_type,
        "target_id": target_id,
        "details": details or {}
    }
    line = json.dumps(entry, ensure_ascii=False)
    # log combinado
    combined_logger.info(line)
    # log por role
    role_logger = _get_role_logger(role)
    role_logger.info(line)
