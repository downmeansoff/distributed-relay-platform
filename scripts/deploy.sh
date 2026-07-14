#!/usr/bin/env bash
# Rolling-деплой на узлы окружения. Узлы обновляются по одному: выводим из
# балансировки -> обновляем -> ждём health -> возвращаем. Секреты (SSH-ключ,
# список хостов) приходят из окружения/CI, в репозиторий не попадают.
set -euo pipefail

ENVIRONMENT="${1:?usage: deploy.sh <staging|prod>}"
HOSTS="${HOSTS:?HOSTS env is required (comma-separated)}"

echo ">> deploy to ${ENVIRONMENT}"
IFS=',' read -ra NODES <<< "$HOSTS"

for node in "${NODES[@]}"; do
    echo ">> [$node] drain from balancer"
    # ssh "$node" 'touch /etc/drp/drain'      # пример: пометить узел на вывод

    echo ">> [$node] pull & restart"
    # ssh "$node" 'cd /opt/drp && git pull --ff-only && docker compose up -d --build'

    echo ">> [$node] wait for health"
    ./scripts/healthcheck.sh "$node" || { echo "!! [$node] unhealthy, aborting"; exit 1; }

    echo ">> [$node] back to rotation"
    # ssh "$node" 'rm -f /etc/drp/drain'
done

echo ">> ${ENVIRONMENT} deploy done"
