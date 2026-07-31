"""Sanitized API demo with structured health states.

The production system has richer probes and telemetry. This public implementation
keeps only deterministic, injectable health checks for the BOS.PRO harness demo.
"""

from __future__ import annotations

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import asdict, dataclass
from enum import Enum
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, Iterable

APP_ENV = os.getenv("APP_ENV", "local")


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass(frozen=True)
class ProbeSpec:
    name: str
    check: Callable[[], bool]
    critical: bool = False
    timeout_seconds: float = 0.25


@dataclass(frozen=True)
class ProbeResult:
    name: str
    status: HealthStatus
    critical: bool
    latency_ms: int
    detail: str


def run_probe(spec: ProbeSpec) -> ProbeResult:
    """Run one probe with a hard timeout and a sanitized error result."""

    started = time.perf_counter()
    executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix=f"probe-{spec.name}")
    future = executor.submit(spec.check)

    try:
        is_healthy = bool(future.result(timeout=spec.timeout_seconds))
        status = HealthStatus.HEALTHY if is_healthy else HealthStatus.UNHEALTHY
        detail = "ok" if is_healthy else "check returned false"
    except FutureTimeoutError:
        future.cancel()
        status = HealthStatus.UNHEALTHY
        detail = f"timeout after {spec.timeout_seconds:.3f}s"
    except Exception as exc:  # noqa: BLE001 - probe failures must be isolated
        status = HealthStatus.UNHEALTHY
        detail = f"{type(exc).__name__}: probe failed"
    finally:
        executor.shutdown(wait=False, cancel_futures=True)

    latency_ms = max(0, round((time.perf_counter() - started) * 1000))
    return ProbeResult(
        name=spec.name,
        status=status,
        critical=spec.critical,
        latency_ms=latency_ms,
        detail=detail,
    )


def aggregate_health(probes: Iterable[ProbeSpec]) -> tuple[int, dict[str, object]]:
    """Aggregate critical and optional probes into a stable API contract."""

    results = [run_probe(probe) for probe in probes]

    if any(result.critical and result.status is HealthStatus.UNHEALTHY for result in results):
        overall = HealthStatus.UNHEALTHY
        http_status = 503
    elif any(result.status is HealthStatus.UNHEALTHY for result in results):
        overall = HealthStatus.DEGRADED
        http_status = 200
    else:
        overall = HealthStatus.HEALTHY
        http_status = 200

    payload = {
        "status": overall.value,
        "env": APP_ENV,
        "checks": [
            {
                **asdict(result),
                "status": result.status.value,
            }
            for result in results
        ],
    }
    return http_status, payload


def _mode_probe(env_name: str) -> Callable[[], bool]:
    """Deterministic probe used only by the sanitized public demo."""

    def check() -> bool:
        mode = os.getenv(env_name, "healthy").strip().lower()
        if mode == "timeout":
            time.sleep(1.0)
        if mode == "error":
            raise RuntimeError("simulated probe failure")
        return mode == "healthy"

    return check


def default_probes() -> list[ProbeSpec]:
    return [
        ProbeSpec(
            name="database",
            check=_mode_probe("DEMO_DB_HEALTH"),
            critical=True,
            timeout_seconds=0.10,
        ),
        ProbeSpec(
            name="relay",
            check=_mode_probe("DEMO_RELAY_HEALTH"),
            critical=False,
            timeout_seconds=0.10,
        ),
    ]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - stdlib callback name
        if self.path == "/health":
            code, payload = aggregate_health(default_probes())
            self._json(code, payload)
        elif self.path == "/api/v1/nodes":
            self._json(200, {"nodes": [], "note": "sanitized demo"})
        else:
            self._json(404, {"error": "not found"})

    def _json(self, code: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: object) -> None:
        pass


def main(host: str = "0.0.0.0", port: int = 8000) -> None:
    HTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
