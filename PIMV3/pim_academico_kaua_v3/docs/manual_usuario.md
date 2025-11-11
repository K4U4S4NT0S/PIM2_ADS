# Manual - PIM Acadêmico v3 (Demo)
1. Rode `python setup_db.py` para criar o banco com usuários demo (admin,prof,aluno).
2. Abra um terminal e rode `python run_server.py` (servidor de relatórios na porta 9001).
3. Em outro terminal rode `python run_client.py` e use as opções para gerar gráficos.
4. Os gráficos gerados ficam no servidor em `data/graphs/` e são enviados ao cliente quando solicitados.
5. Para testes, use os usuários criados por `setup_db.py`:
   - admin@demo.local / admin123
   - Prof Demo (CPF 12345678901) / prof123
   - aluno@demo.local / aluno123
