from __future__ import annotations

from bt_api_base.balance_utils import simple_balance_handler as _ripio_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_ripio.exchange_data import RipioExchangeDataSpot
from bt_api_ripio.feeds.live_ripio.spot import RipioRequestDataSpot


def register_ripio(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed('RIPIO___SPOT', RipioRequestDataSpot)
    registry.register_exchange_data('RIPIO___SPOT', RipioExchangeDataSpot)
    registry.register_balance_handler('RIPIO___SPOT', _ripio_balance_handler)
