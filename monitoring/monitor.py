"""Лёгкий агент мониторинга relay-узлов.

Опрашивает список узлов, измеряет доступность и время отклика, считает аптайм
и печатает сводку. В проде метрики уходят в бэкенд/хранилище; здесь — stdout,
чтобы было видно принцип без тяжёлого стека.
"""
import os
import socket
import time
from dataclasses import dataclass, field


@dataclass
class NodeState:
    host: str
    port: int
    checks: int = 0
    up: int = 0
    last_rtt_ms: float | None = None
    history: list[bool] = field(default_factory=list)

    @property
    def uptime_pct(self) -> float:
        return 100.0 * self.up / self.checks if self.checks else 0.0


def probe(host: str, port: int, timeout: float = 2.0) -> float | None:
    """TCP-проба. Возвращает RTT в мс или None, если узел недоступен."""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return (time.perf_counter() - start) * 1000
    except OSError:
        return None


def parse_targets(raw: str) -> list[tuple[str, int]]:
    targets = []
    for item in filter(None, (x.strip() for x in raw.split(","))):
        host, _, port = item.partition(":")
        targets.append((host, int(port or 0)))
    return targets


def main() -> None:
    targets = parse_targets(os.getenv("MONITOR_TARGETS", "relay-1:10000,relay-2:10000"))
    interval = int(os.getenv("MONITOR_INTERVAL_SEC", "15"))
    states = {t: NodeState(*t) for t in targets}

    print(f"[monitor] targets={targets} interval={interval}s")
    while True:
        for t, st in states.items():
            rtt = probe(*t)
            st.checks += 1
            healthy = rtt is not None
            st.up += int(healthy)
            st.last_rtt_ms = rtt
            st.history = (st.history + [healthy])[-20:]
            flag = "UP  " if healthy else "DOWN"
            rtt_s = f"{rtt:6.1f}ms" if rtt is not None else "   —   "
            print(f"[{flag}] {st.host}:{st.port}  rtt={rtt_s}  uptime={st.uptime_pct:5.1f}%")
        time.sleep(interval)


if __name__ == "__main__":
    main()
