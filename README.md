# RIPIO

Exchange plugin for bt_api framework — Argentine cryptocurrency exchange.

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_ripio.svg)](https://pypi.org/project/bt_api_ripio/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_ripio.svg)](https://pypi.org/project/bt_api_ripio/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_ripio/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_ripio/actions)
[![Docs](https://readthedocs.org/projects/bt-api-ripio/badge/?version=latest)](https://bt-api-ripio.readthedocs.io/)

---

## English | [中文](#中文)

### Overview

[Ripio](https://www.ripio.com/) is an **Argentine cryptocurrency exchange** offering crypto trading services in Latin America. This plugin integrates Ripio into the [bt_api](https://github.com/cloudQuant/bt_api_py) unified trading framework, supporting **SPOT** markets.

### Features

- **REST API** — market data queries, order management, account queries
- **WebSocket feeds** — real-time ticker and trade streams
- **Latin America focus** — supports ARS (Argentine Peso) trading pairs
- **Simple API key auth** — standard API key + secret authentication

### Exchange Code

| Code | Description | Asset Type |
|------|-------------|------------|
| `RIPIO___SPOT` | Ripio spot markets | SPOT |

### Installation

```bash
pip install bt_api_ripio
```

Or install from source:

```bash
git clone https://github.com/cloudQuant/bt_api_ripio
cd bt_api_ripio
pip install -e .
```

### Quick Start

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

# Get ticker data
ticker = api.get_tick("RIPIO___SPOT", "BTCUSDT")
print(ticker)

# Get order book depth
depth = api.get_depth("RIPIO___SPOT", "BTCUSDT")
print(depth)

# Get K-line / bars
bars = api.get_kline("RIPIO___SPOT", "BTCUSDT", "1h")
print(bars)
```

### Supported Operations

| Operation | SPOT | Notes |
|-----------|:----:|-------|
| Ticker | ✅ | `get_tick()` |
| OrderBook (Depth) | ✅ | `get_depth()` |
| K-Line (Bars) | ✅ | `get_kline()` |
| Recent Trades | ✅ | `get_recent_trades()` |
| Exchange Info | ✅ | `get_exchange_info()` |
| Account Balance | ✅ | `get_balance()` |
| Order Management | ✅ | `make_order`, `cancel_order` |
| WebSocket Stream | ✅ | `subscribe()` |

### Architecture

```
bt_api_ripio/
├── src/bt_api_ripio/
│   ├── containers/              # Data containers
│   │   ├── accounts/           # Account data
│   │   ├── balances/          # Balance data
│   │   ├── bars/             # Bar/K-line data
│   │   ├── orderbooks/       # Order book data
│   │   ├── orders/           # Order data
│   │   └── tickers/          # Ticker data
│   ├── exchange_data/          # Exchange metadata & symbol routing
│   ├── feeds/live_ripio/      # REST feed implementations
│   │   ├── request_base.py   # RipioRequestData (REST feed base)
│   │   └── spot.py           # RipioRequestDataSpot (SPOT feed)
│   ├── errors/                 # Error translator
│   ├── registry_registration.py # Exchange registry wiring
│   └── plugin.py            # Plugin entry point
├── tests/                      # Unit tests
└── docs/                     # Documentation
```

### API Reference

#### Feed Classes

- **`RipioRequestDataSpot`** — REST feed for SPOT markets; supports ticker, depth, kline, order management, account queries

#### Container Classes

- **`RipioTickerData`** — Ticker / price data
- **`RipioOrderBookData`** — Order book / depth data
- **`RipioBarData`** — K-line / OHLCV data
- **`RipioOrderData`** — Order data
- **`RipioBalanceData`** — Balance data

#### Exchange Data Classes

- **`RipioExchangeData`** — Base exchange metadata
- **`RipioExchangeDataSpot`** — SPOT-specific metadata

### Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-ripio.readthedocs.io/ |
| Chinese Docs | https://bt-api-ripio.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_ripio |
| Issue Tracker | https://github.com/cloudQuant/bt_api_ripio/issues |

### Requirements

- Python 3.9+
- bt_api_base >= 0.15, < 1.0

### License

MIT License — see [LICENSE](LICENSE) for details.

### Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_ripio/issues)
- Email: yunjinqi@gmail.com

---

## 中文

### 概述

[Ripio](https://www.ripio.com/) 是**阿根廷加密货币交易所**，在拉丁美洲提供加密货币交易服务。本插件将 Ripio 接入 [bt_api](https://github.com/cloudQuant/bt_api_py) 统一交易框架，支持**现货（SPOT）**市场。

### 功能特点

- **REST API** — 行情查询、订单管理、账户查询
- **WebSocket 推送** — 实时行情和成交推送
- **拉丁美洲聚焦** — 支持 ARS（阿根廷比索）交易对
- **简单 API Key 认证** — 标准 API Key + Secret 认证

### 交易所代码

| 代码 | 描述 | 资产类型 |
|------|------|----------|
| `RIPIO___SPOT` | Ripio 现货市场 | SPOT |

### 安装

```bash
pip install bt_api_ripio
```

或从源码安装：

```bash
git clone https://github.com/cloudQuant/bt_api_ripio
cd bt_api_ripio
pip install -e .
```

### 快速开始

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

# 获取行情
ticker = api.get_tick("RIPIO___SPOT", "BTCUSDT")
print(ticker)

# 获取订单簿深度
depth = api.get_depth("RIPIO___SPOT", "BTCUSDT")
print(depth)

# 获取 K 线数据
bars = api.get_kline("RIPIO___SPOT", "BTCUSDT", "1h")
print(bars)
```

### 支持的操作

| 操作 | SPOT | 说明 |
|------|:----:|------|
| 行情 | ✅ | `get_tick()` |
| 订单簿 | ✅ | `get_depth()` |
| K 线 | ✅ | `get_kline()` |
| 最新成交 | ✅ | `get_recent_trades()` |
| 交易所信息 | ✅ | `get_exchange_info()` |
| 账户余额 | ✅ | `get_balance()` |
| 订单管理 | ✅ | `make_order`, `cancel_order` |
| WebSocket 推送 | ✅ | `subscribe()` |

### 架构

```
bt_api_ripio/
├── src/bt_api_ripio/
│   ├── containers/              # 数据容器
│   │   ├── accounts/           # 账户数据
│   │   ├── balances/           # 余额数据
│   │   ├── bars/                # K 线数据
│   │   ├── orderbooks/          # 订单簿数据
│   │   ├── orders/              # 订单数据
│   │   └── tickers/             # 行情数据
│   ├── exchange_data/           # 交易所元数据 & 交易对路由
│   ├── feeds/live_ripio/        # REST feed 实现
│   │   ├── request_base.py      # RipioRequestData (REST base)
│   │   └── spot.py              # RipioRequestDataSpot (SPOT feed)
│   ├── errors/                  # 错误翻译器
│   ├── registry_registration.py   # 交易所注册 wiring
│   └── plugin.py                # 插件入口
├── tests/                       # 单元测试
└── docs/                        # 文档
```

### API 参考

#### Feed 类

- **`RipioRequestDataSpot`** — SPOT 市场 REST feed；支持行情、深度、K 线、订单管理、账户查询

#### 容器类

- **`RipioTickerData`** — 行情 / 价格数据
- **`RipioOrderBookData`** — 订单簿 / 深度数据
- **`RipioBarData`** — K 线 / OHLCV 数据
- **`RipioOrderData`** — 订单数据
- **`RipioBalanceData`** — 余额数据

#### 交易所数据类

- **`RipioExchangeData`** — 基础交易所元数据
- **`RipioExchangeDataSpot`** — SPOT 专用元数据

### 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-ripio.readthedocs.io/ |
| 中文文档 | https://bt-api-ripio.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_ripio |
| 问题反馈 | https://github.com/cloudQuant/bt_api_ripio/issues |

### 系统要求

- Python 3.9+
- bt_api_base >= 0.15, < 1.0

### 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。

### 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_ripio/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com
