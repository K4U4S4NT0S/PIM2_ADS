=========================================================================== 

🎓 PIM2 - Sys Academy (Terminal)

Um sistema acadêmico completo desenvolvido em Python para execução via terminal.
O projeto implementa autenticação por papéis (Admin, Professor e Aluno), CRUDs, gerenciamento de aulas, atividades, notas e logs.

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
- Gerenciar aulas
- Visualizar e gerar logs
- Criar backups dos dados

===========================================================================

👨‍🏫 Professor

O professor pode:

- Ver seus dados
- Gerenciar Aulas
- Registrar e editar notas

===========================================================================

👨‍🎓 Aluno

O aluno tem acesso a:

- Ver seus dados
- Notas
- Cursos
- Boletim
- Relatorio

===========================================================================

📝 Logs e Auditoria

- Armazenados em JSONL
- Registram ações, erros e operações CRUD
- Trazem maior rastreabilidade ao sistema

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
