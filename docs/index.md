# RIPIO Documentation

## English

### Overview

[Ripio](https://www.ripio.com/) is an Argentine cryptocurrency exchange. This plugin integrates Ripio SPOT markets into the bt_api framework.

### Exchange Code

| Code | Description | Asset Type |
|------|-------------|------------|
| `RIPIO___SPOT` | Ripio spot markets | SPOT |

### Quick Start

```bash
pip install bt_api_ripio
```

```python
from bt_api import BtApi

api = BtApi(
    exchange_kwargs={
        "RIPIO___SPOT": {
            "api_key": "your_api_key",
            "secret": "your_secret",
        }
    }
)

# Market data
ticker = api.get_tick("RIPIO___SPOT", "BTCUSDT")
depth = api.get_depth("RIPIO___SPOT", "BTCUSDT")
bars = api.get_kline("RIPIO___SPOT", "BTCUSDT", "1h")

# WebSocket subscription
api.subscribe(
    "RIPIO___SPOT___BTCUSDT",
    [
        {"topic": "ticker", "symbol": "BTCUSDT"},
        {"topic": "depth", "symbol": "BTCUSDT"},
    ],
)
```

### API Reference

#### Feed Classes

| Class | Description |
|-------|-------------|
| `RipioRequestDataSpot` | REST feed for SPOT markets |

#### Container Classes

| Class | Description |
|-------|-------------|
| `RipioTickerData` | Ticker / price data |
| `RipioOrderBookData` | Order book / depth data |
| `RipioBarData` | K-line / OHLCV data |
| `RipioOrderData` | Order data |
| `RipioBalanceData` | Balance data |

#### Exchange Data Classes

| Class | Description |
|-------|-------------|
| `RipioExchangeData` | Base exchange metadata |
| `RipioExchangeDataSpot` | SPOT metadata |

#### Key Methods

| Method | Description |
|--------|-------------|
| `get_tick(symbol)` | Get ticker data |
| `get_depth(symbol, count=20)` | Get order book depth |
| `get_kline(symbol, period, count=20)` | Get K-line / OHLCV data |
| `get_recent_trades(symbol, limit=100)` | Get recent trades |
| `get_balance()` | Get account balance |
| `get_exchange_info()` | Get exchange / symbol info |
| `make_order(symbol, side, price, volume, order_type)` | Place order |
| `cancel_order(symbol, order_id)` | Cancel order |

---

## 中文

### 概述

[Ripio](https://www.ripio.com/) 是阿根廷加密货币交易所。本插件将 Ripio 现货市场接入 bt_api 框架。

### 交易所代码

| 代码 | 描述 | 资产类型 |
|------|------|----------|
| `RIPIO___SPOT` | Ripio 现货市场 | SPOT |

### 快速开始

```bash
pip install bt_api_ripio
```

```python
from bt_api import BtApi

api = BtApi(
    exchange_kwargs={
        "RIPIO___SPOT": {
            "api_key": "您的api_key",
            "secret": "您的secret",
        }
    }
)

# 行情数据
ticker = api.get_tick("RIPIO___SPOT", "BTCUSDT")
depth = api.get_depth("RIPIO___SPOT", "BTCUSDT")
bars = api.get_kline("RIPIO___SPOT", "BTCUSDT", "1h")

# WebSocket 订阅
api.subscribe(
    "RIPIO___SPOT___BTCUSDT",
    [
        {"topic": "ticker", "symbol": "BTCUSDT"},
        {"topic": "depth", "symbol": "BTCUSDT"},
    ],
)
```

### API 参考

#### Feed 类

| 类 | 描述 |
|----|------|
| `RipioRequestDataSpot` | SPOT 市场 REST feed |

#### 容器类

| 类 | 描述 |
|----|------|
| `RipioTickerData` | 行情 / 价格数据 |
| `RipioOrderBookData` | 订单簿 / 深度数据 |
| `RipioBarData` | K 线 / OHLCV 数据 |
| `RipioOrderData` | 订单数据 |
| `RipioBalanceData` | 余额数据 |

#### 交易所数据类

| 类 | 描述 |
|----|------|
| `RipioExchangeData` | 基础交易所元数据 |
| `RipioExchangeDataSpot` | SPOT 专用元数据 |

#### 核心方法

| 方法 | 描述 |
|------|------|
| `get_tick(symbol)` | 获取行情数据 |
| `get_depth(symbol, count=20)` | 获取订单簿深度 |
| `get_kline(symbol, period, count=20)` | 获取 K 线 / OHLCV 数据 |
| `get_recent_trades(symbol, limit=100)` | 获取最新成交 |
| `get_balance()` | 获取账户余额 |
| `get_exchange_info()` | 获取交易所 / 交易对信息 |
| `make_order(symbol, side, price, volume, order_type)` | 下单 |
| `cancel_order(symbol, order_id)` | 撤单 |
