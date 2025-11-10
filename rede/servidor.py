
import socket, threading
from utils.filedb import load_json
HOST = '127.0.0.1'
PORT = 5050

def handle(conn, addr):
    with conn:
        data = conn.recv(4096).decode('utf-8').strip()
        if not data:
            return
        parts = data.split('|')
        cmd = parts[0].upper()
        if cmd == 'GET_ATIVIDADES':
            turma = parts[1] if len(parts)>1 else ''
            ativ = load_json('/mnt/data/pim2_code/data/atividades.json', [])
            out = [a for a in ativ if a.get('turma_codigo')==turma]
            conn.sendall(('OK|' + str(len(out)) + '|' + ';'.join([a.get('titulo') for a in out])).encode('utf-8'))
        else:
            conn.sendall(('ERR|UNKNOWN_CMD|Comando desconhecido').encode('utf-8'))

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Servidor rodando em {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print('Servidor finalizado')
    finally:
        s.close()

if __name__ == '__main__':
    start_server()
