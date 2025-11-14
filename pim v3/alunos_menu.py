import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from integrated_data_store import (
    DataStore,
    decrypt_text
)

data = DataStore()


# ================================================================
# CADASTRO DE ALUNO
# ================================================================
def cadastrar_aluno_flow():
    print("\n=== Cadastro de Aluno ===")

    nome = input("Nome completo: ").strip()
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()

    # proteção para lista vazia
    novo_id = len(data.alunos) + 1 if data.alunos else 1

    cursos = data.cursos

    print("\nCursos disponíveis:")
    for c in cursos:
        print(f"{c['id']} - {c['nome']}")

    # proteção contra erro ao digitar curso inválido
    while True:
        try:
            curso_id = int(input("ID do curso: ").strip())
            break
        except ValueError:
            print("Digite um número válido.")

    aluno = {
        "id": novo_id,
        "name": nome,
        "email": email,
        "senha": senha,
        "curso_id": curso_id
    }

    data.cadastrar_aluno(aluno)

    data.adicionar_usuario({
        "id": novo_id,
        "name": nome,
        "email": email,
        "senha": senha,
        "role": "aluno"
    })

    print("\nAluno cadastrado com sucesso!")
    return aluno


# ================================================================
# MENU DO ALUNO
# ================================================================
def aluno_menu(user):
    while True:
        print("\n===== MENU DO ALUNO =====")
        print("1 - Ver meus dados")
        print("2 - Ver minhas notas")
        print("3 - Gerar boleto PDF")
        print("0 - Sair\n")

        op = input("> ").strip()

        if op == "1":
            mostrar_dados_aluno(user)

        elif op == "2":
            mostrar_notas_aluno(user)

        elif op == "3":
            gerar_boleto_pdf(user)

        elif op == "0":
            break
        else:
            print("Opcao inválida!")


# ================================================================
# MOSTRAR DADOS DO ALUNO
# ================================================================
def mostrar_dados_aluno(user):
    print("\n===== MEUS DADOS =====")
    print(f"ID: {user['id']}")
    print(f"Nome: {user['name']}")

    # email pode estar criptografado ou não
    email_raw = user.get("email", "")
    try:
        email_dec = decrypt_text(email_raw)
    except Exception:
        email_dec = email_raw

    print(f"Email: {email_dec}")
    print(f"Genero: {user.get('genero', 'Indefinido')}")
    print(f"Data nascimento: {user.get('dob', '---')}")


# ================================================================
# NOTAS DO ALUNO
# ================================================================
def mostrar_notas_aluno(user):

    avaliacoes = data.avaliacoes
    aulas = data.aulas

    print("\n===== MINHAS NOTAS =====")

    notas = []
    for aula in aulas:
        avs = [
            x for x in avaliacoes
            if x["aula_id"] == aula["id"] and x["usuario_id"] == user["id"]
        ]

        if not avs:
            continue

        nota = avs[-1].get("nota", 0)
        notas.append(nota)

        print(f"Aula: {aula['titulo']}  | Nota: {nota}")

    if not notas:
        print("\nNenhuma nota encontrada.")
        return

    media = sum(notas) / len(notas)
    situacao = "Aprovado" if media >= 6 else "Reprovado"

    print(f"\nMédia final: {media:.2f}")
    print(f"Situação: {situacao}")


# ================================================================
# GERAR BOLETO PDF
# ================================================================
def gerar_boleto_pdf(user):

    avaliacoes = data.avaliacoes
    aulas = data.aulas

    pasta = "boletos"
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    caminho = os.path.join(pasta, f"boleto_aluno_{user['id']}.pdf")

    c = canvas.Canvas(caminho, pagesize=A4)
    largura, altura = A4

    y = altura - 50

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, y, "Boleto / Relatório do Aluno")
    y -= 40

    # email seguro
    email_raw = user.get("email", "")
    try:
        email_dec = decrypt_text(email_raw)
    except Exception:
        email_dec = email_raw

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Nome: {user['name']}")
    y -= 20
    c.drawString(50, y, f"Email: {email_dec}")
    y -= 20

    # Notas
    y -= 25
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Notas por Aula:")
    y -= 25

    notas = []
    for aula in aulas:
        avs = [
            a for a in avaliacoes
            if a["aula_id"] == aula["id"] and a["usuario_id"] == user["id"]
        ]

        if avs:
            nota = avs[-1].get("nota", 0)
            notas.append(nota)

            c.setFont("Helvetica", 12)
            c.drawString(60, y, f"{aula['titulo']}: {nota}")
            y -= 20

    if notas:
        media = sum(notas) / len(notas)
        situacao = "Aprovado" if media >= 6 else "Reprovado"

        y -= 10
        c.drawString(50, y, f"Média Final: {media:.2f}")
        y -= 20
        c.drawString(50, y, f"Situação: {situacao}")
    else:
        c.drawString(60, y, "Nenhuma nota encontrada.")

    c.showPage()
    c.save()

    print(f"\n📄 Boleto gerado com sucesso em: {caminho}")
