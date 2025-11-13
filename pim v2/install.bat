@echo off
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
start cmd /k "python setup_db.py & echo DB criado & pause"
timeout /t 2 >nul
start cmd /k "python run_server.py"
timeout /t 1 >nul
start cmd /k "python run_client.py"
