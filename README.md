=========================================================================== 

🎓 PIM V3 — Sistema Acadêmico em Python (Terminal)

Um sistema acadêmico completo desenvolvido em Python para execução via terminal.
O projeto implementa autenticação por papéis (Admin, Professor e Aluno), CRUDs, gerenciamento de aulas, atividades, notas, logs e um chat IA simulado.

===========================================================================

📌 Sumário

Visão Geral

- Funcionalidades
- Estrutura do Projeto
- Instalação
- Como Executar
- Tecnologias Utilizadas
- Melhorias Futuras
- Autores

===========================================================================

📘 Visão Geral

Este projeto foi desenvolvido para o PIM (Projeto Integrado Multidisciplinar).
O sistema simula um ambiente acadêmico interno, permitindo o gerenciamento de alunos, professores, turmas, aulas e atividades usando arquivos JSON como base de dados.

Ele foi projetado para ser modular, simples de utilizar e fácil de expandir.

===========================================================================

🚀 Funcionalidades
🔐 Autenticação

- Login com usuário e senha
- Papéis disponíveis:
- Administrador
- Professor
- Aluno

===========================================================================

🛠️ Administrador (Admin)

Permite:

- Gerenciar alunos
- Gerenciar professores
- Gerenciar turmas
- Gerenciar atividades
- Gerenciar aulas
- Visualizar e gerar logs
- Criar backups dos dados

===========================================================================

👨‍🏫 Professor

O professor pode:

- Ver suas turmas
- Listar alunos da turma
- Criar atividades
- Registrar e editar notas
- Ver agenda de aulas
- Visualizar relatórios

===========================================================================

👨‍🎓 Aluno

O aluno tem acesso a:

- Agenda de aulas
- Notas e atividades
- Perfil
- Consulta a cursos
- Chat IA simulado

🤖 IA Simulada
- O projeto inclui um módulo de IA mockado que responde perguntas básicas, simulando um assistente interno.

===========================================================================

📝 Logs e Auditoria

- Armazenados em JSONL
- Registram ações, erros e operações CRUD
- Trazem maior rastreabilidade ao sistema

===========================================================================

📂 Estrutura do Projeto

pim_v3/

├── admin_menu.py

├── aluno_menu.py

├── professores_menu.py

├── ai_module.py

├── app/

│   ├── auth.py

│   ├── db.py

│   ├── logs.py

│   ├── main.py

│   ├── main_menu.py

│   ├── database/

│   │   ├── aluno_manager.py

│   │   ├── professor_manager.py

│   │   ├── turma_manager.py

│   │   ├── aulas_manager.py

│   │   ├── atividades_manager.py

│   │   ├── database_manager.py

│   │   ├── file_manager.py

│   │   └── json/

│   │       ├── alunos.json

│   │       ├── professores.json

│   │       ├── turmas.json

│   │       ├── aulas.json

│   │       ├── atividades.json

│   │       ├── cursos.json

│   │       └── usuarios.json

├── logs/

│   └── logs_YYYY-MM-DD.jsonl

└── requirements.txt

===========================================================================

🛠️ Instalação

1️⃣ Clone o repositório
git clone https://github.com/K4U4S4NT0S/PIM2_ADS.git
cd SEU-REPO

2️⃣ Instale as dependências
pip install -r requirements.txt

▶️ Como Executar

Execute o sistema com:
python app/main.py

===========================================================================

🧰 Tecnologias Utilizadas

- Python 3.10+
- JSON como banco de dados
- Estrutura modular
- Logs em JSONL
- Menus interativos via terminal
- Dashboards com gráficos de desempenho
- Autenticação JWT
- Exportação de relatórios em PDF
