from __future__ import annotations

from typing import Any

from bt_api_ripio.feeds.live_ripio.request_base import RipioRequestData


def test_ripio_accepts_public_private_key_aliases(monkeypatch: Any) -> None:
    request_data = RipioRequestData(public_key="public-key", private_key="secret-key")

    timestamp = "1710000000000"
    monkeypatch.setattr("time.time", lambda: 1710000000.0)
    headers = request_data._build_headers("GET", "/api/v1/balances", is_sign=True)

    assert request_data.api_key == "public-key"
    assert request_data.api_secret == "secret-key"
    assert headers["X-API-KEY"] == "public-key"
    assert headers["X-API-TIMESTAMP"] == timestamp
    assert headers["X-API-SIGNATURE"]
