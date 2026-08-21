#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

HOST="${PAINT_HUB_HOST:-0.0.0.0}"
PORT="${PAINT_HUB_PORT:-8010}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    "$PYTHON_BIN" -m venv .venv
fi

echo "Instalando dependencias..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

echo "Aplicando migrations no SQLite..."
.venv/bin/python manage.py migrate

echo ""
echo "Paint Hub iniciado."
echo "Nesta maquina: http://127.0.0.1:${PORT}/"
echo "Na rede local, acesse pelo IP desta maquina na porta ${PORT}."
echo "IPs encontrados:"
hostname -I 2>/dev/null || true
echo ""

.venv/bin/python manage.py runserver "${HOST}:${PORT}"
