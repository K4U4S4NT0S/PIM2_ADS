@echo off
REM instalador para Windows - verifica Python, instala requisitos e abre o sistema em outra janela

REM --- Verifica se python está disponível
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Python nao encontrado. Instalando Python embutido via winget (se disponivel)...
  winget install --id Python.Python.3 -e --silent
  if %ERRORLEVEL% neq 0 (
    echo Falha ao instalar Python automaticamente. Por favor instale o Python 3.10+ manualmente e rode este .bat novamente.
    pause
    exit /b 1
  )
)

REM --- Cria venv
python -m venv venv
call venv\Scripts\activate

REM --- Atualiza pip
python -m pip install --upgrade pip

REM --- Instala dependencias
pip install bcrypt matplotlib pandas plantuml python-dotenv

REM --- Abre o sistema numa nova janela do cmd
start cmd /k "call venv\Scripts\activate && python main.py"

exit /b 0
