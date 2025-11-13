# analytics.py - gera CSV simples de logins por dia
import os, json
def generate_logins_csv():
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    files = [f for f in os.listdir(logs_dir) if f.startswith("logs_") and f.endswith(".jsonl")]
    counts = {}
    for fn in files:
        p = os.path.join(logs_dir, fn)
        for l in open(p, "r", encoding="utf-8"):
            try:
                j = json.loads(l)
                msg = j.get("mensagem","")
                if "login" in msg.lower():
                    day = fn.replace("logs_","").replace(".jsonl","")
                    counts[day] = counts.get(day,0) + 1
            except:
                pass
    out = os.path.join(os.path.dirname(__file__), "exports", "logins_by_day.csv")
    with open(out, "w", encoding="utf-8") as f:
        f.write("day,count\n")
        for k in sorted(counts.keys()):
            f.write(f"{k},{counts[k]}\n")
    return out