# distributed-relay-platform

Обезличенный референс инфраструктуры распределённой сетевой платформы, которую я
спроектировал и держу в проде: балансировка нагрузки на сеть relay-узлов, единый
бэкенд с общим API, CI/CD со staging-окружением и собственная система мониторинга.

> **Про этот репозиторий.** Это *санитизированная портфолио-версия* реального
> продакшн-сервиса. Секреты, ключи, домены и код бизнес-логики сюда не входят — их
> заменяют примеры (`*.example`) и заглушки. Задача репозитория — показать
> архитектуру и DevOps-практики, а не поднять сервис «из коробки».

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?logo=gnubash&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-1F3864)

## Архитектура

```mermaid
flowchart TD
    subgraph Clients["Клиенты"]
        WEB[Веб-интерфейс]
        MOB[Мобильные приложения<br/>Android / iOS]
        TG[Telegram-бот]
    end

    LB[["Балансировщик нагрузки<br/>(edge / health-aware)"]]

    subgraph Relays["Сеть relay-узлов (Docker)"]
        R1[relay-1]
        R2[relay-2]
        R3[relay-3]
        RN[... relay-N]
    end

    API[["Единый бэкенд / API"]]
    DB[(PostgreSQL)]
    MON[["Собственный мониторинг<br/>нагрузка · аптайм · воркеры"]]

    WEB --> API
    MOB --> API
    TG  --> API
    API --> LB
    LB --> R1 & R2 & R3 & RN
    API --> DB
    MON -. опрашивает .-> R1 & R2 & R3 & RN
    MON -. метрики .-> API
```

**Ключевые решения**

- **Один API на все клиенты.** Веб, мобильные приложения и Telegram-бот ходят в
  единый бэкенд через общий контракт — меньше дублирования логики, проще выкатки.
- **Балансировка с учётом здоровья узлов.** Трафик не льётся на relay, который не
  прошёл health-check; узел выводится из ротации до восстановления.
- **Собственный мониторинг вместо готового.** Лёгкий агент собирает нагрузку,
  аптайм и состояние воркеров с каждого узла — полный контроль над тем, что и как
  измеряется, без тяжёлого стека.
- **CI/CD со staging.** Изменения сначала едут на stage-узлы, прогоняются проверки,
  и только потом — в прод. Деплой без даунтайма (rolling).

## Стек

| Слой            | Технологии                                          |
|-----------------|-----------------------------------------------------|
| Оркестрация     | Docker, Docker Compose                              |
| Edge / relay    | Xray (VLESS), health-aware балансировка             |
| Бэкенд / API    | Python                                              |
| Хранилище       | PostgreSQL                                          |
| CI/CD           | GitHub Actions (lint → test → staging → prod)       |
| Наблюдаемость   | Собственный агент мониторинга (Python)              |
| Скрипты / ops   | Bash                                                |

## Структура репозитория

```
distributed-relay-platform/
├── docker-compose.yml         # локальная сборка: LB + relay-узлы + backend + monitoring
├── .env.example               # переменные окружения (без реальных значений)
├── Makefile                   # частые команды: up / down / logs / lint / deploy
├── .github/workflows/ci.yml   # пайплайн: lint → test → deploy staging → deploy prod
├── backend/                   # заглушка единого API
│   ├── app.py
│   └── requirements.txt
├── config/xray/
│   └── relay.example.json     # пример конфигурации relay-узла (санитизировано)
├── monitoring/
│   ├── monitor.py             # агент: аптайм, нагрузка, состояние воркеров
│   └── README.md
└── scripts/
    ├── deploy.sh              # rolling-деплой на узлы по SSH
    └── healthcheck.sh         # проверка здоровья узла для балансировщика
```

## Как запустить локально

```bash
cp .env.example .env      # заполнить примерными значениями
make up                   # поднять стенд в Docker
make logs                 # смотреть логи
make down                 # остановить
```

> Для локального стенда relay-узлы работают в демо-режиме (без реального проксирования).

## CI/CD

Пайплайн в `.github/workflows/ci.yml`:

1. **lint** — проверка Python (`ruff`) и Bash (`shellcheck`);
2. **test** — юнит-тесты бэкенда и агента мониторинга;
3. **deploy-staging** — выкатка на stage-узлы, smoke-проверки;
4. **deploy-prod** — ручное подтверждение (environment protection) → rolling-деплой.

## Лицензия

[MIT](LICENSE) © 2026 Глеб Лутфуллин
