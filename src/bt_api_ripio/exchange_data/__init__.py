from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData

_FALLBACK_REST_PATHS = {
    'get_tick': 'GET /api/v1/ticker/{symbol}',
    'get_depth': 'GET /api/v1/depth/{symbol}',
    'get_kline': 'GET /api/v1/kline/{symbol}',
    'get_trades': 'GET /api/v1/trades/{symbol}',
    'get_exchange_info': 'GET /api/v1/products',
}


class RipioExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = 'RIPIO___SPOT'
        self.rest_url = 'https://api.exchange.ripio.com'
        self.wss_url = 'wss://api.exchange.ripio.com/ws'
        self.rest_paths = dict(_FALLBACK_REST_PATHS)
        self.wss_paths = {}
        self.kline_periods = {
            '1m': '1',
            '5m': '5',
            '15m': '15',
            '30m': '30',
            '1h': '60',
            '4h': '240',
            '1d': '1440',
            '1w': '10080',
        }
        self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}
        self.legal_currency = ['ARS', 'BRL', 'EUR', 'MXN', 'USD', 'USDT', 'BTC', 'ETH', 'UAH']

    def get_symbol(self, symbol: str) -> str:
        return symbol.replace('-', '_').replace('/', '_').upper()

    def get_period(self, period: str) -> str:
        return self.kline_periods.get(period, period)

    def get_rest_path(self, request_type: str, **kwargs) -> str:
        if request_type not in self.rest_paths or self.rest_paths[request_type] == '':
            raise ValueError('REST path not found')
        path = self.rest_paths[request_type]
        if kwargs:
            for k, v in kwargs.items():
                path = path.replace(f'{{{k}}}', str(v))
        return path


class RipioExchangeDataSpot(RipioExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = 'SPOT'

    def get_symbol(self, symbol: str) -> str:
        return symbol.replace('-', '_').replace('/', '_').upper()
