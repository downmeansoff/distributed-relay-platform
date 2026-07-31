from __future__ import annotations

import time

from backend.app import HealthStatus, ProbeSpec, aggregate_health, run_probe


def test_all_probes_healthy() -> None:
    code, payload = aggregate_health(
        [
            ProbeSpec("database", lambda: True, critical=True),
            ProbeSpec("relay", lambda: True),
        ]
    )

    assert code == 200
    assert payload["status"] == "healthy"
    assert [item["status"] for item in payload["checks"]] == ["healthy", "healthy"]


def test_optional_probe_failure_degrades_service() -> None:
    code, payload = aggregate_health(
        [
            ProbeSpec("database", lambda: True, critical=True),
            ProbeSpec("relay", lambda: False),
        ]
    )

    assert code == 200
    assert payload["status"] == "degraded"


def test_critical_probe_failure_makes_service_unhealthy() -> None:
    code, payload = aggregate_health(
        [
            ProbeSpec("database", lambda: False, critical=True),
            ProbeSpec("relay", lambda: True),
        ]
    )

    assert code == 503
    assert payload["status"] == "unhealthy"


def test_probe_exception_is_sanitized() -> None:
    def explode() -> bool:
        raise RuntimeError("secret internal address")

    result = run_probe(ProbeSpec("database", explode, critical=True))

    assert result.status is HealthStatus.UNHEALTHY
    assert "secret internal address" not in result.detail
    assert result.detail == "RuntimeError: probe failed"


def test_slow_optional_probe_times_out_and_degrades() -> None:
    def slow_probe() -> bool:
        time.sleep(0.03)
        return True

    started = time.perf_counter()
    code, payload = aggregate_health(
        [
            ProbeSpec("database", lambda: True, critical=True),
            ProbeSpec("relay", slow_probe, timeout_seconds=0.005),
        ]
    )
    elapsed = time.perf_counter() - started

    assert code == 200
    assert payload["status"] == "degraded"
    assert payload["checks"][1]["detail"].startswith("timeout after")
    assert elapsed < 0.025
