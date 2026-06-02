@echo off
REM ============================================================
REM  Arranca la aplicacion de canciones.
REM  La primera vez crea un entorno virtual e instala Flask.
REM ============================================================

cd /d "%~dp0"

if not exist ".venv\" (
    echo Primera vez: creando entorno virtual e instalando Flask...
    py -m venv .venv
    call .venv\Scripts\activate.bat
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo ============================================================
echo  Abri el navegador en:  http://127.0.0.1:5000
echo  Para detener: cerra esta ventana o presiona Ctrl + C
echo ============================================================
echo.

py app.py
pause
