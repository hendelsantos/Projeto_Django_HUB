@echo off
REM ============================================================
REM  Paint HUB - Script simples para iniciar o sistema
REM  Basta dar 2 cliques neste arquivo para rodar o projeto.
REM ============================================================

REM Entra na pasta do projeto (uma pasta acima de "scripts")
cd /d "%~dp0\.."

REM Se a pasta do ambiente virtual (.venv) ainda nao existe, cria agora.
REM Isso so acontece na primeira vez que o script roda.
if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente virtual do Python...
    py -3 -m venv .venv
)

REM Instala (ou atualiza) as bibliotecas que o projeto precisa,
REM usando o Python de dentro do ambiente virtual (.venv).
echo Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt

REM Atualiza o banco de dados (cria/ajusta as tabelas necessarias).
echo Preparando banco de dados...
".venv\Scripts\python.exe" manage.py migrate

REM Mostra o IP desta maquina na rede, para acessar de outro
REM computador ou celular conectado na mesma rede Wi-Fi/cabo.
echo.
echo ============================================================
echo  Sistema iniciando...
echo  Nesta maquina, acesse:      http://localhost:8010
echo  De outro aparelho na rede, use o IP abaixo na porta 8010:
ipconfig | findstr /i "IPv4"
echo ============================================================
echo.
echo Para PARAR o sistema, feche esta janela ou aperte Ctrl+C.
echo.

REM Inicia o servidor do Django.
REM "0.0.0.0" faz o sistema ficar visivel para outros aparelhos
REM da mesma rede, nao somente para esta maquina.
".venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8010

REM Mantem a janela aberta caso algum erro tenha acontecido acima.
pause
