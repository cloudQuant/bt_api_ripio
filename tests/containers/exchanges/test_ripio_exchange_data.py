"""Tests for RipioExchangeData container."""

from __future__ import annotations

from bt_api_ripio.exchange_data import RipioExchangeData


class TestRipioExchangeData:
    """Tests for RipioExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = RipioExchangeData()

        assert exchange.exchange_name == "RIPIO___SPOT"
