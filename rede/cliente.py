
import socket
HOST = '127.0.0.1'
PORT = 5050

def solicitar_atividades(turma_codigo):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    msg = f"GET_ATIVIDADES|{turma_codigo}"
    s.sendall(msg.encode('utf-8'))
    resp = s.recv(4096).decode('utf-8')
    s.close()
    return resp

if __name__ == '__main__':
    print(solicitar_atividades('2ADS'))
