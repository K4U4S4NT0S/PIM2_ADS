# generate_diagrams.py - gera arquivos PlantUML em exports/diagrams/
import os, datetime
BASE = os.path.dirname(__file__)
OUT_DIR = os.path.join(BASE, "exports", "diagrams")
os.makedirs(OUT_DIR, exist_ok=True)

def write_file(name, content):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def generate_class_diagram():
    puml = """@startuml
class IntegratedDataStore {
  +add_usuario()
  +criar_curso()
  +criar_aula()
}
class AlunosMenu
class ProfessoresMenu
class AdminMenu
class LoggerUtils
class AiModule

IntegratedDataStore -- AlunosMenu
IntegratedDataStore -- ProfessoresMenu
IntegratedDataStore -- AdminMenu
LoggerUtils ..> IntegratedDataStore
AiModule ..> IntegratedDataStore
@enduml
"""
    return write_file("class_diagram.puml", puml)

def generate_usecase_diagram():
    puml = """@startuml
left to right direction
actor Aluno
actor Professor
actor Admin

rectangle "PIM2 ADS" {
  Aluno -- (Ver cursos)
  Aluno -- (Avaliar aula)
  Professor -- (Criar/Editar/Avaliar aulas)
  Admin -- (Gerenciar usuarios)
  Admin -- (Gerenciar cursos)
}
@enduml
"""
    return write_file("usecase_diagram.puml", puml)

def generate_sequence_diagram():
    puml = """@startuml
actor Aluno
participant Client
participant IntegratedDataStore
participant Server

Aluno -> Client: Login/Cadastro
Client -> IntegratedDataStore: read/write JSON
Client -> Server: registrar_evento (log)
Server -> Server: exibe logs
@enduml
"""
    return write_file("sequence_diagram.puml", puml)

def generate_all():
    files = []
    files.append(generate_class_diagram())
    files.append(generate_usecase_diagram())
    files.append(generate_sequence_diagram())
    idx = os.path.join(OUT_DIR, "index.txt")
    with open(idx, "w", encoding="utf-8") as f:
        f.write("Diagrams generated on " + datetime.datetime.now().isoformat() + "\n")
        for p in files:
            f.write(p + "\n")
    return files

if __name__ == "__main__":
    for p in generate_all():
        print("Wrote", p)