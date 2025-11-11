import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "exports")
DIAGRAMS_DIR = os.path.join(EXPORTS_DIR, "diagramas")
GRAFS_DIR = os.path.join(EXPORTS_DIR, "graficos")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)
os.makedirs(GRAFS_DIR, exist_ok=True)

def generate_uml_diagram():
    """
    Gera um arquivo .puml com uma versão simples do diagrama UML (classes).
    Para converter .puml em imagem instale PlantUML e Graphviz, ou use plantuml.jar.
    """
    puml = """@startuml
class Usuario {
  - id
  - nome
  - data_nasc
  - genero
  - password_hash
}
class Aluno {
  - email
  - notas
}
class Professor {
  - cpf
  - turmas
}
class Admin {
  - username
}
Usuario <|-- Aluno
Usuario <|-- Professor
Usuario <|-- Admin
class Curso {
  - id
  - nome
  - avaliacoes
}
class Aula {
  - id
  - titulo
  - data
}
Curso "1" *-- "*" Aula
Professor "1" o-- "*" Aula
Aluno "0..*" o-- "*" Curso
@enduml
"""
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    puml_path = os.path.join(DIAGRAMS_DIR, f"diagram_{ts}.puml")
    with open(puml_path, "w", encoding="utf-8") as f:
        f.write(puml)
    print(f"Arquivo PUML gerado em: {puml_path}")
    print("Para gerar PNG: instale PlantUML e rode: plantuml -tpng {puml_path}")
    return puml_path

def generate_course_graphs():
    """
    Simula dados e gera graficos de avaliacoes/generos/idades.
    Salva PNGs em exports/graficos/ e retorna caminhos para download.
    """
    # dados simulados (ou carregue de data/courses.json)
    df = pd.DataFrame({
        'curso': ['Matematica','Programacao','Redes','Matematica','Programacao','Redes'],
        'nota': [4,5,3,5,4,4],
        'genero': ['M','F','M','F','M','F'],
        'idade': [20,22,23,19,30,25]
    })

    # Grafico: avaliacoes por curso (media)
    g1 = df.groupby('curso')['nota'].mean().reset_index()
    plt.figure()
    plt.bar(g1['curso'], g1['nota'])
    plt.title("Media de avaliacoes por curso")
    g1_path = os.path.join(GRAFS_DIR, "avaliacoes_por_curso.png")
    plt.savefig(g1_path)
    plt.close()

    # Grafico: distribuicao por genero
    g2 = df['genero'].value_counts()
    plt.figure()
    g2.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Distribuicao por genero")
    g2_path = os.path.join(GRAFS_DIR, "genero.png")
    plt.savefig(g2_path)
    plt.close()

    # Grafico: idade (histograma)
    plt.figure()
    df['idade'].plot(kind='hist', bins=5)
    plt.title("Distribuicao de idades")
    g3_path = os.path.join(GRAFS_DIR, "idades.png")
    plt.savefig(g3_path)
    plt.close()

    print("Graficos gerados em:", GRAFS_DIR)
    return [g1_path, g2_path, g3_path]
