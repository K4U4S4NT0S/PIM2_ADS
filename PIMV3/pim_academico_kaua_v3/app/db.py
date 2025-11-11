import sqlite3, os, threading
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'pim.db'))
_lock = threading.Lock()
def get_conn():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError('Banco nao encontrado. Rode setup_db.py')
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
def query(sql, params=(), fetch=False):
    with _lock:
        conn = get_conn(); cur = conn.cursor()
        cur.execute(sql, params)
        if fetch:
            rows = cur.fetchall(); conn.commit(); conn.close(); return [dict(r) for r in rows]
        conn.commit(); conn.close(); return None
