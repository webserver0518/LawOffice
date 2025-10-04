##!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

git pull

# Build and start your service
docker-compose up -d --build

# Show logs (optional)
docker-compose logs -f law-office




