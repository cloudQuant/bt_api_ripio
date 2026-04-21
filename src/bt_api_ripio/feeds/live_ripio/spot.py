from __future__ import annotations

from typing import Any

from bt_api_base.feeds.capability import Capability
from bt_api_base.functions.utils import update_extra_data
from bt_api_ripio.exchange_data import RipioExchangeDataSpot
from bt_api_ripio.feeds.live_ripio.request_base import RipioRequestData


class RipioRequestDataSpot(RipioRequestData):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "RIPIO___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = RipioExchangeDataSpot()

    def _get_tick(self, symbol, extra_data=None, **kwargs):
        request_type = "get_tick"
        path = self._params.get_rest_path(request_type)
        ripio_symbol = self._params.get_symbol(symbol)
        path = path.replace(":symbol", ripio_symbol)
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_tick_normalize_function,
            },
        )
        return path, {}, extra_data

    @staticmethod
    def _get_tick_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        if not input_data.get("success", False):
            return [], False
        ticker = input_data.get("data", {})
        return [ticker], ticker is not None

    def get_tick(self, symbol, extra_data=None, **kwargs):
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_tick(self, symbol, extra_data=None, **kwargs):
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    get_ticker = get_tick
    async_get_ticker = async_get_tick

    def _get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        request_type = "get_depth"
        path = self._params.get_rest_path(request_type)
        ripio_symbol = self._params.get_symbol(symbol)
        path = path.replace(":symbol", ripio_symbol)
        params = {"limit": min(count, 100)}
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_depth_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_depth_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        if not input_data.get("success", False):
            return [], False
        depth = input_data.get("data", {})
        return [depth], depth is not None

    def get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_depth(self, symbol, count=20, extra_data=None, **kwargs):
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_kline(
        self, symbol, period, count=100, from_time=None, to_time=None, extra_data=None, **kwargs
    ):
        request_type = "get_kline"
        path = self._params.get_rest_path(request_type)
        ripio_symbol = self._params.get_symbol(symbol)
        ripio_period = self._params.get_period(period)
        params = {"limit": min(count, 1000), "period": ripio_period}
        if from_time:
            params["from"] = from_time
        if to_time:
            params["to"] = to_time
        path = path.replace(":symbol", ripio_symbol)
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "period": period,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_kline_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_kline_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        if not input_data.get("success", False):
            return [], False
        klines = input_data.get("data", [])
        return klines or [], klines is not None

    def get_kline(
        self, symbol, period, count=100, extra_data=None, from_time=None, to_time=None, **kwargs
    ):
        path, params, extra_data = self._get_kline(
            symbol, period, count, from_time, to_time, extra_data, **kwargs
        )
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_kline(
        self, symbol, period, count=100, extra_data=None, from_time=None, to_time=None, **kwargs
    ):
        path, params, extra_data = self._get_kline(
            symbol, period, count, from_time, to_time, extra_data, **kwargs
        )
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_exchange_info(self, extra_data=None, **kwargs):
        request_type = "get_exchange_info"
        path = self._params.get_rest_path(request_type)
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": "ALL",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_exchange_info_normalize_function,
            },
        )
        return path, {}, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        if not input_data.get("success", False):
            return [], False
        products = input_data.get("data", [])
        return products or [], products is not None

    def get_exchange_info(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_trades(self, symbol, limit=100, extra_data=None, **kwargs):
        request_type = "get_trades"
        path = self._params.get_rest_path(request_type)
        ripio_symbol = self._params.get_symbol(symbol)
        path = path.replace(":symbol", ripio_symbol)
        params = {"limit": min(limit, 500)}
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_trades_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_trades_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        if not input_data.get("success", False):
            return [], False
        trades = input_data.get("data", [])
        return trades or [], trades is not None

    def get_trades(self, symbol, limit=100, extra_data=None, **kwargs):
        path, params, extra_data = self._get_trades(symbol, limit, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_balance(self, symbol=None, extra_data=None, **kwargs):
        path = "/api/v1/balances"
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_balance",
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_balance_normalize_function,
            },
        )
        return path, {}, extra_data

    @staticmethod
    def _get_balance_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        if isinstance(input_data, dict) and not input_data.get("success", True):
            return [], False
        data = input_data.get("data", input_data) if isinstance(input_data, dict) else input_data
        return [data], True

    def get_balance(self, symbol=None, extra_data=None, **kwargs):
        path, params, extra_data = self._get_balance(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def _get_account(self, extra_data=None, **kwargs):
        path = "/api/v1/balances"
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "get_account",
                "symbol_name": "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_account_normalize_function,
            },
        )
        return path, {}, extra_data

    @staticmethod
    def _get_account_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        data = input_data.get("data", input_data) if isinstance(input_data, dict) else input_data
        return [data], True

    def get_account(self, symbol="ALL", extra_data=None, **kwargs):
        path, params, extra_data = self._get_account(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)

    def _make_order(
        self, symbol, volume, price, order_type, offset="open", extra_data=None, **kwargs
    ):
        ripio_symbol = self._params.get_symbol(symbol)
        path = "/api/v1/order"
        params = {
            "pair": ripio_symbol,
            "amount": str(volume),
            "price": str(price),
            "side": "buy" if "buy" in order_type.lower() else "sell",
            "type": "limit",
        }
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "make_order",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._make_order_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _make_order_normalize_function(input_data, extra_data):
        if not input_data:
            return [], False
        return [input_data], True

    def make_order(
        self,
        symbol,
        volume,
        price=None,
        order_type="buy-limit",
        offset="open",
        post_only=False,
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        path, params, extra_data = self._make_order(
            symbol, volume, price, order_type, offset, extra_data, **kwargs
        )
        return self.request(path, body=params, extra_data=extra_data, is_sign=True)

    def _cancel_order(self, symbol, order_id, extra_data=None, **kwargs):
        path = f"/api/v1/order/{order_id}"
        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": "cancel_order",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "order_id": order_id,
            },
        )
        return path, {}, extra_data

    def cancel_order(self, symbol, order_id, extra_data=None, **kwargs):
        path, params, extra_data = self._cancel_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data, is_sign=True)
