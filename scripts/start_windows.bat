@echo off
setlocal

cd /d "%~dp0\.."

if "%PAINT_HUB_HOST%"=="" set PAINT_HUB_HOST=0.0.0.0
if "%PAINT_HUB_PORT%"=="" set PAINT_HUB_PORT=8010

if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente virtual...
    py -3 -m venv .venv
)

echo Instalando dependencias...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo Aplicando migrations no SQLite...
".venv\Scripts\python.exe" manage.py migrate

echo.
echo Ferramentas digitais Paint Shop iniciado.
echo Nesta maquina: http://127.0.0.1:%PAINT_HUB_PORT%/
echo Na rede local, acesse pelo IP desta maquina na porta %PAINT_HUB_PORT%.
echo Para descobrir o IP, veja o endereco IPv4 abaixo:
ipconfig | findstr /i "IPv4"
echo.

".venv\Scripts\python.exe" manage.py runserver %PAINT_HUB_HOST%:%PAINT_HUB_PORT%

endlocal
