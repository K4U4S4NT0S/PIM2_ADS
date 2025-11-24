@echo off
title Inicializador PIM2_ADS_FINAL_v10
color 0A
echo =============================================
echo   SISTEMA PIM2_ADS FINAL FULL v10 - INICIALIZADOR
echo =============================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python nao encontrado. Baixando e instalando...
    curl -L -o python_installer.exe https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe
    echo Instalando Python, aguarde...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python_installer.exe
) else (
    echo Python encontrado.
)
echo.

echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install colorama matplotlib flask requests >nul

echo Iniciando servidor e cliente...
start "Servidor PIM2" cmd /k "title Servidor PIM2 && python servidor.py"
start "Cliente PIM2" cmd /k "title Cliente PIM2 && python client.py"

echo Sistema iniciado.
pause