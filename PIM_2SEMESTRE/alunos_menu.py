def _input_nonempty(prompt):
    val = input(prompt).strip()
    if not val:
        print("Entrada vazia — operação cancelada.")
        return None
    return val

def _clear():
    import os
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

import os
import getpass
from generate_reports import gerar_relatorio_aluno, gerar_boletim_aluno

from integrated_data_store import (
    DataStore,
    decrypt_text
)

from generate_reports import gerar_relatorio_aluno

data = DataStore.get_instance()


from generate_reports import gerar_relatorio_aluno

data = DataStore.get_instance()


# ================================================================
# CADASTRO DE ALUNO
# ================================================================


def cadastrar_aluno_flow():
    """
    Fluxo de cadastro de aluno:
    - nome
    - email
    - genero
    - idade
    - senha (para permitir login)
    Validações amigáveis e persistência em alunos.json e usuarios.json (role=aluno).
    """
    from integrated_data_store import DataStore, encrypt_text

    data = DataStore.get_instance()

    _clear()
    print("\n" + "="*40)
    print("CADASTRO DE ALUNO")
    print("="*40)

    try:
        # Nome
        nome = input("Nome completo: ").strip()
        if not nome:
            print("Nome inválido. O cadastro foi cancelado.")
            return None

        # Email simple validation
        email = input("Email: ").strip()
        if "@" not in email or "." not in email:
            print("Email inválido. Insira um email no formato exemplo@dominio.com")
            return None

        # Genero (male/female/other or text)
        genero = input("Gênero (M/F/Outro) — deixe em branco se preferir não informar: ").strip()
        if not genero:
            genero = "Não informado"

        # Idade must be integer >= 0
        idade_raw = input("Idade (apenas números): ").strip()
        try:
            idade = int(idade_raw)
            if idade < 0 or idade > 120:
                print("Idade inválida. Deve ser um número entre 0 e 120.")
                return None
        except:
            print("Idade inválida. Use apenas números.")
            return None

        # Senha para login (oculta) com confirmação
        senha = getpass.getpass("Senha (mínimo 4 caracteres) — será usada para login: ").strip()
        if len(senha) < 4:
            print("Senha muito curta. Cadastro cancelado.")
            return None
        senha_conf = getpass.getpass("Confirme a senha: ").strip()
        if senha != senha_conf:
            print("Senhas diferentes. Cadastro cancelado.")
            return None

        # preparar dados do aluno
        aluno = {
            "nome": nome,
            "email": email,
            "genero": genero,
            "idade": idade
        }

        # persistir aluno (cadastrar_aluno gera id automaticamente)
        data.cadastrar_aluno(aluno)

        # criar usuário correspondente para login (na lista usuarios)
        try:
            cpf_placeholder = ""  # não temos CPF aqui
            cpf_guardado = encrypt_text(cpf_placeholder)
        except Exception:
            cpf_guardado = ""

        usuario = {
            "nome": nome,
            "email": email,
            "cpf": cpf_guardado,
            "role": "aluno",
            "senha": senha
        }

        # vincula usuário ao aluno recém-criado
        try:
            usuario["aluno_id"] = aluno.get("id")
        except Exception:
            pass

        data.cadastrar_usuario(usuario)

        # mostrar confirmação com id do aluno e do usuário
        criado_aluno = None
        for a in data.alunos:
            if a.get("email") == email:
                criado_aluno = a
                break

        criado_user = None
        for u in data.usuarios:
            if u.get("email") == email:
                criado_user = u
                break

        if criado_aluno:
            print(f"Aluno cadastrado com sucesso! ID aluno = {criado_aluno.get('id')}")
        else:
            print("Aluno cadastrado, mas não foi possível recuperar o ID do aluno.")

        if criado_user:
            print(f"Conta de acesso criada! ID usuário = {criado_user.get('id')}")
        else:
            print("Conta de acesso não foi criada corretamente.")

        input("ENTER para voltar")
        return criado_aluno

    except Exception as e:
        print("Erro durante o cadastro de aluno:", str(e))
        return None


def aluno_menu(user):
    _clear()
    while True:
        print("\n===== MENU DO ALUNO =====")
        print("1 - Ver meus dados")
        print("2 - Ver minhas notas")
        print("3 - Gerar relatorio em PDF")
        print("4 - Cursos")
        print("5 - Boletim")
        print("0 - Sair\n")

        op = input("> ").strip()

        if op == "1":
            # Mostrar dados basicos do usuario
            _clear()
            print("\n===== MEUS DADOS =====")
            try:
                from integrated_data_store import DataStore
                data = DataStore.get_instance()
                aluno_rec = None
                # procurar por aluno vinculado via aluno_id no usuario
                if user.get('aluno_id'):
                    aluno_rec = next((a for a in data.alunos if a.get('id') == int(user.get('aluno_id'))), None)
                if aluno_rec is None:
                    aluno_rec = next((a for a in data.alunos if a.get('email') == user.get('email')), None)
                merged = dict(user)
                if aluno_rec:
                    for k,v in aluno_rec.items():
                        if v is not None:
                            merged[k]=v
                # campos a mostrar
                for k in ['id', 'nome', 'email', 'genero', 'idade', 'curso_id']:
                    print(f"{k}: {merged.get(k, '-')}")
            except Exception:
                for k in ['id','nome','email']:
                    print(f"{k}: {user.get(k)}")
            input("ENTER para voltar")
            _clear()
        elif op == "2":
            _clear()
            print("\n===== MINHAS NOTAS =====")
            # tenta recuperar notas se existir estrutura
            try:
                notas = getattr(data, 'notas', [])
                aluno_id = user.get('aluno_id') or user.get('id')
                notas_aluno = [n for n in notas if int(n.get('aluno_id', -1)) == int(aluno_id or -1)]
                if notas_aluno:
                    for n in notas_aluno:
                        print(n)
                else:
                    print("Nenhuma nota encontrada para este aluno.")
            except Exception:
                print("Sem dados de notas.")
            input("ENTER para voltar")
            _clear()
        elif op == "3":
            _clear()
            try:
                notas = getattr(data, 'notas', [])
                aluno_id = user.get('aluno_id') or user.get('id')
                notas_aluno = [n for n in notas if int(n.get('aluno_id', -1)) == int(aluno_id or -1)]
            except Exception:
                notas_aluno = None
            path = gerar_relatorio_aluno(user, notas=notas_aluno)
            print('Relatorio gerado em', path)
            input("ENTER para voltar")
            _clear()

        elif op == "4":
            _clear()
            mostrar_cursos_aluno(user)
            _clear()

        elif op == "5":
            _clear()
            # gerar boletim
            try:
                matriculas = data.listar_matriculas_do_aluno(user.get('id')) if hasattr(data, 'listar_matriculas_do_aluno') else None
            except Exception:
                matriculas = None
            try:
                notas = getattr(data, 'notas', [])
            except Exception:
                notas = None
            path = gerar_boletim_aluno(user, matriculas=matriculas, notas=notas)
            print('Boletim gerado em', path)
            input('ENTER para voltar')
            _clear()
        elif op == "0":
            # confirma saída do menu do aluno
            conf = input("Deseja realmente sair do menu do aluno? (S/N): ").strip().lower()
            if conf in ("s", "sim"):
                _clear()
                break
            else:
                _clear()
                continue
        else:
            print("Opção inválida")
            input("ENTER para voltar")
            _clear()


def mostrar_cursos_aluno(user):
    """Mostra lista de cursos e permite ao aluno escolher um curso para ver as aulas deste curso."""
    base = os.path.dirname(__file__)
    cursos = getattr(data, 'cursos', [])
    if not cursos:
        print("Nenhum curso cadastrado no sistema.")
        input("ENTER para voltar")
        return
    while True:
        print("\n=== Cursos Disponíveis ===")
        for c in cursos:
            cid = c.get('id') or c.get('curso_id') or '(sem id)'
            titulo = c.get('nome') or c.get('titulo') or '(sem nome)'
            print(f"{cid} - {titulo}")
        print("0 - Voltar")
        escolha = input("ID do curso: ").strip()
        if escolha == "0" or escolha == "":
            break
        try:
            cid = int(escolha)
        except Exception:
            print("Digite um ID válido.")
            continue
        curso = next((c for c in cursos if int(c.get('id', -1)) == cid), None)
        if not curso:
            print("Curso não encontrado.")
            continue
        # mostrar submenu de aulas do curso
        aulas = getattr(data, 'aulas', [])
        aulas_do_curso = [a for a in aulas if int(a.get('curso_id', -1)) == int(curso.get('id', -1))]
        while True:
            print(f"\n== Aulas do curso: {curso.get('nome') } ==")
            if not aulas_do_curso:
                print("Nenhuma aula cadastrada para este curso.")
            else:
                for a in aulas_do_curso:
                    prof_name = data.get_user_name(a.get('professor_id')) if hasattr(data, 'get_user_name') else a.get('professor_id')
                    print(f"{a.get('id')} - {a.get('titulo', a.get('nome','(sem titulo)'))} (Prof: {prof_name})")
            print("0 - Voltar ao menu de cursos")
            sel = input("ID da aula para ver detalhes: ").strip()
            if sel == "0" or sel == "":
                break
            try:
                aid = int(sel)
            except Exception:
                print("Digite um ID válido.")
                continue
            aula = next((x for x in aulas_do_curso if int(x.get('id', -1)) == aid), None)
            if not aula:
                print("Aula não encontrada.")
                continue
            # mostrar detalhes da aula
            print("\n--- Detalhes da Aula ---")
            print(f"ID: {aula.get('id')}")
            print(f"Titulo: {aula.get('titulo', aula.get('nome','-'))}")
            print(f"Descricao: {aula.get('descricao','-')}")
            prof_name = data.get_user_name(aula.get('professor_id')) if hasattr(data, 'get_user_name') else aula.get('professor_id')
            print(f"Professor: {prof_name}")
            # matricular
            try:
                if hasattr(data, 'is_matriculado') and data.is_matriculado(user.get('id'), aula.get('id')):
                    print('Você já está matriculado nesta aula.')
                    input('ENTER para voltar às aulas')
                else:
                    resp = input('Deseja se matricular nesta aula? (s/n): ').strip().lower()
                    if resp == 's':
                        if hasattr(data, 'matricular_aluno'):
                            m = data.matricular_aluno(user.get('id'), aula.get('id'))
                        else:
                            m = True
                        if m:
                            print('Matriculado com sucesso!')
                        else:
                            print('Nao foi possivel matricular.')
                        input('ENTER para voltar às aulas')
                    else:
                        input('ENTER para voltar às aulas')
            except Exception:
                print("Erro ao verificar matrícula.")
                input('ENTER para voltar às aulas')
