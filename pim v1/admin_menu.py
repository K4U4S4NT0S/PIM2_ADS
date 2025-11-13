import os
import json
from users import load_users, save_users, delete_user_by_index
from log_utils import log_action
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
BACKUP_COURSES_DIR = os.path.join(BACKUP_DIR, "courses")
BACKUP_AULAS_DIR = os.path.join(BACKUP_DIR, "aulas")
os.makedirs(BACKUP_COURSES_DIR, exist_ok=True)
os.makedirs(BACKUP_AULAS_DIR, exist_ok=True)

def ensure_courses_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(COURSES_FILE):
        with open(COURSES_FILE, "w", encoding="utf-8") as f:
            json.dump({"courses": []}, f, indent=2, ensure_ascii=False)

def load_courses():
    ensure_courses_file()
    with open(COURSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_courses(data):
    ensure_courses_file()
    with open(COURSES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def backup_course(course_obj):
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"course_backup_{course_obj.get('id','unknown')}_{ts}.json"
    path = os.path.join(BACKUP_COURSES_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(course_obj, f, indent=2, ensure_ascii=False)
    return path

def backup_aula(aula_obj):
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"aula_backup_{aula_obj.get('id','unknown')}_{ts}.json"
    path = os.path.join(BACKUP_AULAS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(aula_obj, f, indent=2, ensure_ascii=False)
    return path

def admin_menu(user):
    print("Entrou no menu admin.")
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Editar usuarios")
        print("2. Criar/editar/excluir curso")
        print("3. Criar/editar/excluir aulas")
        print("4. Gerar diagramas")
        print("5. Gerar graficos")
        print("6. Ver registros de aulas dos professores")
        print("7. Logout")
        opc = input("Escolha: ").strip()
        if opc == "1":
            d = load_users()
            users = d['users']
            for i,u in enumerate(users):
                ident = u.get("email") or u.get("cpf") or u.get("username") or ""
                print(f"{i+1}. {u.get('nome')} | role: {u.get('role')} | id: {u.get('id')} | ident: {ident}")
            sel = input("Escolha usuario (numero) ou 'q': ")
            if sel.lower() == 'q':
                continue
            try:
                idx = int(sel)-1
                u = users[idx]
                print("1. Editar nome\n2. Editar genero\n3. Editar email/cpf\n4. Excluir usuario")
                a = input("Escolha: ")
                if a == "1":
                    old = u.get('nome')
                    u['nome'] = input("Novo nome: ")
                    save_users(d)
                    log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="edit", target_type="user", target_id=u.get("id"), details={"field":"nome","old":old,"new":u['nome']})
                elif a == "2":
                    old = u.get('genero')
                    u['genero'] = input("Novo genero: ")
                    save_users(d)
                    log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="edit", target_type="user", target_id=u.get("id"), details={"field":"genero","old":old,"new":u['genero']})
elif a == "3":
            if u.get('role') == 'aluno':
                old = u.get('email')
                u['email'] = input("Novo email: ")
                save_users(d)
                log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="edit", target_type="user", target_id=u.get("id"), details={"field":"email","old":old,"new":u['email']})
            else:
                old = u.get('cpf')
                u['cpf'] = input("Novo CPF: ")
                save_users(d)
                log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="edit", target_type="user", target_id=u.get("id"), details={"field":"cpf","old":old,"new":u['cpf']})
        elif a == "4":
            confirm = input("Confirmar exclusao? (s/n) ")
            if confirm.lower() == 's':
                if delete_user_by_index(idx):
                    print("Usuario excluido (backup criado).")
                else:
                    print("Erro ao excluir.")
        else:
            print("Opcao invalida.")
    except Exception as e:
        print("Entrada invalida:", e)
elif opc == "2":
    data = load_courses()
    courses = data['courses']
    print("Cursos existentes:")
    for i,c in enumerate(courses):
        print(f"{i+1}. {c.get('nome')} (id:{c.get('id')})")
    sub = input("1=Criar 2=Editar 3=Excluir 4=Voltar: ")
    if sub == "1":
        nome = input("Nome do curso: ")
        cid = f"course_{int(datetime.utcnow().timestamp())}"
        course = {"id": cid, "nome": nome, "aulas": [], "created_at": datetime.utcnow().isoformat()}
        courses.append(course)
        save_courses(data)
        log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="create", target_type="course", target_id=cid, details={"nome": nome})
        print("Curso criado.")
    elif sub == "2":
        sel = int(input("Curso numero: "))-1
        if 0 <= sel < len(courses):
            old = courses[sel].get('nome')
            courses[sel]['nome'] = input("Novo nome: ")
            save_courses(data)
            log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="edit", target_type="course", target_id=courses[sel].get('id'), details={"field":"nome","old":old,"new":courses[sel]['nome']})
            print("Curso editado.")
        else:
            print("Selecao invalida.")
    elif sub == "3":
        sel = int(input("Curso numero: "))-1
        if 0 <= sel < len(courses):
            course = courses[sel]
            backup_path = backup_course(course)
            courses.pop(sel)
            save_courses(data)
            log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="delete", target_type="course", target_id=course.get("id"), details={"backup": backup_path})
            print(f"Curso excluido. Backup em: {backup_path}")
        else:
            print("Selecao invalida.")
    elif sub == "4":
        continue
    else:
        print("Opcao invalida.")
elif opc == "3":
    data = load_courses()
    courses = data['courses']
    for i,c in enumerate(courses):
        print(f"{i+1}. {c.get('nome')} (id:{c.get('id')}) - {len(c.get('aulas',[]))} aulas")
    cid_idx = int(input("Escolha o curso numero (ou 0 para voltar): ")) - 1
    if cid_idx == -1:
        continue
    if cid_idx < 0 or cid_idx >= len(courses):
        print("Curso invalido.")
        continue
    course = courses[cid_idx]
    print(f"Aulas do curso {course.get('nome')}:")
    aulas = course.get('aulas', [])
    for i,a in enumerate(aulas):
        print(f"{i+1}. {a.get('titulo')} (id:{a.get('id')})")
    sub = input("1=Criar 2=Editar 3=Excluir 4=Voltar: ")
    if sub == "1":
        titulo = input("Titulo da aula: ")
        aid = f"aula_{int(datetime.utcnow().timestamp())}"
        aula = {"id": aid, "titulo": titulo, "conteudo": "", "data": "", "created_at": datetime.utcnow().isoformat()}
        aulas.append(aula)
        save_courses(data)
        log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="create", target_type="aula", target_id=aid, details={"course_id": course.get("id"), "titulo": titulo})
        print("Aula criada.")
    elif sub == "2":
        sidx = int(input("Aula numero: "))-1
        if 0 <= sidx < len(aulas):
            old = aulas[sidx].get('titulo')
            aulas[sidx]['titulo'] = input("Novo titulo: ")
            save_courses(data)
            log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="edit", target_type="aula", target_id=aulas[sidx].get('id'), details={"field":"titulo","old":old,"new":aulas[sidx]['titulo'], "course_id": course.get("id")})
            print("Aula editada.")
        else:
            print("Selecao invalida.")
    elif sub == "3":
        sidx = int(input("Aula numero: "))-1
        if 0 <= sidx < len(aulas):
            aula = aulas[sidx]
            backup_path = backup_aula(aula)
            aulas.pop(sidx)
            save_courses(data)
            log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="delete", target_type="aula", target_id=aula.get("id"), details={"course_id": course.get("id"), "backup": backup_path})
            print(f"Aula excluida. Backup em: {backup_path}")
        else:
            print("Selecao invalida.")
    elif sub == "4":
        continue
    else:
        print("Opcao invalida.")
elif opc == "4":
    try:
        from uml_and_graphs import generate_uml_diagram
        puml = generate_uml_diagram()
        log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="export", target_type="uml", target_id=puml)
    except Exception as e:
        print("Erro ao gerar diagramas:", e)
elif opc == "5":
    try:
        from uml_and_graphs import generate_course_graphs
        files = generate_course_graphs()
        for f in files:
            log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="export", target_type="graphic", target_id=f)
    except Exception as e:
        print("Erro ao gerar graficos:", e)
elif opc == "6":
    print("[REGISTROS] - verificar logs em logs/ (admin/professor/aluno).")
    path = os.path.join(BASE_DIR, "logs", "actions.log")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-30:]
            print("---- ultimas 30 acoes ----")
            for l in lines:
                print(l.strip())
    else:
        print("Nenhum registro encontrado.")
elif opc == "7":
    confirm = input("Confirmar logout? (s/n) ")
    if confirm.lower() == "s":
        log_action(actor_id=user.get("id"), actor_name=user.get("nome"), role="admin", action="logout", target_type="self", target_id=user.get("id"))
        break
else:
    print("Opcao invalida.")
