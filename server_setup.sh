# server_setup.sh
##!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Build and start your service
docker-compose build
docker-compose up -d

# Show logs (optional)
docker-compose logs -f law-office


# old:
#set -euo pipefail
#cd "$(dirname "$0")"

#PY=python3
#if [ ! -d .venv ]; then
#  "$PY" -m venv .venv
#fi
#source .venv/bin/activate
#pip install --upgrade pip
#if [ -f constraints.txt ]; then
#  pip install -r requirements.txt -c constraints.txt
#else
#  pip install -r requirements.txt
#fi
#deactivate

#sudo systemctl daemon-reload
#sudo systemctl restart flask-lawofficesystem
#sudo systemctl --no-pager status flask-lawofficesystem