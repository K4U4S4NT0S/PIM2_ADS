# servidor.py - exibe logs do dia no console do servidor
import time
from logger_utils import ler_eventos


def _normalize_events(raw):
    """
    Normaliza a saída de logger_utils._normalize_events(ler_eventos()) para uma lista de dicionários.
    Aceita:
     - lista já pronta (list of dict)
     - string com JSON (um objeto ou uma lista)
     - string com JSONL (uma linha por evento)
     - string simples (retorna um evento único com key 'message')
    """
    import json
    if raw is None:
        return []
    # já é lista
    if isinstance(raw, list):
        return raw
    # se for bytes -> decode
    if isinstance(raw, bytes):
        try:
            raw = raw.decode("utf-8")
        except:
            raw = str(raw)
    # se for dict -> transformar em lista
    if isinstance(raw, dict):
        return [raw]
    # se for string -> tentar parse
    if isinstance(raw, str):
        s = raw.strip()
        if not s:
            return []
        # tentativa 1: parse como lista JSON
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                return parsed
            if isinstance(parsed, dict):
                return [parsed]
        except Exception:
            pass
        # tentativa 2: interpretar como JSONL (linha por linha)
        lines = s.splitlines()
        out = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                out.append(obj)
                continue
            except Exception:
                # não é JSON -> salvar como mensagem bruta
                out.append({"message": line, "type": "INFO"})
        return out
    # fallback
    return [{"message": str(raw), "type": "INFO"}]

CSI = "\033["
def color_code(tipo):
    t = tipo.upper()
    if t == "ERROR": return CSI + "91m"
    if t == "WARNING": return CSI + "93m"
    if t == "INFO": return CSI + "96m"
    return CSI + "0m"

def servidor_loop():
    print("Servidor Sys Academy - INICIADO")
    seen = 0
    try:
        while True:
            eventos = _normalize_events(ler_eventos())
            novos = eventos[seen:]
            for e in novos:
                c = color_code(e.get("type","INFO"))
                user = e.get("usuario") or "none"
                msg = e.get("mensagem") or e.get("message") or ""
                ts = e.get("timestamp","")
                print(f"{c}[{ts}] [{e.get('type')}] ({user}): {msg}{CSI}0m")
            seen = len(eventos)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Servidor finalizado.")

if __name__ == "__main__":
    servidor_loop()