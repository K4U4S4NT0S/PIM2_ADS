# servidor.py - exibe logs do dia no console do servidor
import time
from logger_utils import ler_eventos

CSI = "\033["
def color_code(tipo):
    t = tipo.upper()
    if t == "ERROR": return CSI + "91m"
    if t == "WARNING": return CSI + "93m"
    if t == "INFO": return CSI + "96m"
    return CSI + "0m"

def servidor_loop():
    print("=== Servidor PIM2 ADS Iniciado ===")
    seen = 0
    try:
        while True:
            eventos = ler_eventos()
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