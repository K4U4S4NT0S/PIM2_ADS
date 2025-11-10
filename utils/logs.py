
from datetime import datetime
def info(msg):
    print(f"[{datetime.now().isoformat()}] INFO: {msg}")
def error(msg):
    print(f"[{datetime.now().isoformat()}] ERROR: {msg}")
