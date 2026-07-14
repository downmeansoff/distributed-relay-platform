#!/usr/bin/env bash
# Проверка здоровья узла для балансировщика/деплоя.
# Возвращает 0, если узел отвечает на /health в течение N попыток.
set -euo pipefail

NODE="${1:?usage: healthcheck.sh <host>}"
PORT="${2:-8000}"
RETRIES="${RETRIES:-10}"
DELAY="${DELAY:-3}"

for i in $(seq 1 "$RETRIES"); do
    if curl -fsS "http://${NODE}:${PORT}/health" >/dev/null 2>&1; then
        echo "ok: ${NODE} healthy (attempt ${i})"
        exit 0
    fi
    sleep "$DELAY"
done

echo "fail: ${NODE} did not become healthy"
exit 1
