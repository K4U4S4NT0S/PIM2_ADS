import socket, threading, json, base64, os
from app.auth import authenticate_aluno, authenticate_professor, register_aluno, register_professor
from app.report import gender_dist, age_hist, avg_by_turma, attendance_trend, box_notas
HOST='0.0.0.0'; PORT=9001
def handle(conn,addr):
    print('Conn from',addr)
    with conn:
        data = conn.recv(65536)
        if not data: return
        try:
            msg = json.loads(data.decode('utf-8'))
        except:
            conn.send(b'INVALID')
            return
        cmd = msg.get('cmd')
        if cmd == 'report':
            kind = msg.get('kind')
            if kind == 'gender': path = gender_dist()
            elif kind == 'age': path = age_hist()
            elif kind == 'avg': path = avg_by_turma(msg.get('turma'))
            elif kind == 'trend': path = attendance_trend(msg.get('turma'))
            elif kind == 'box': path = box_notas(msg.get('turma'))
            else:
                conn.send(json.dumps({'status':'error','msg':'unknown kind'}).encode('utf-8')); return
            # send back metadata + file contents base64
            with open(path,'rb') as f:
                b = base64.b64encode(f.read()).decode('utf-8')
            conn.send(json.dumps({'status':'ok','path':os.path.basename(path),'file':b}).encode('utf-8'))
        else:
            conn.send(json.dumps({'status':'error','msg':'unknown command'}).encode('utf-8'))
def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST,PORT)); s.listen(5); print('Server on',HOST,PORT)
    try:
        while True:
            conn,addr = s.accept(); threading.Thread(target=handle,args=(conn,addr),daemon=True).start()
    finally:
        s.close()
if __name__=='__main__': main()
