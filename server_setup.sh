##!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

docker stop $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
docker network prune -f
docker volume prune -f

git pull

# Build and start your service
docker-compose up -d --build

# Show logs (optional)
#docker-compose logs -f law-office