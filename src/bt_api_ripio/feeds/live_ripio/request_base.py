from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient
from bt_api_ripio.exchange_data import RipioExchangeDataSpot


class RipioRequestData(Feed):
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
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "RIPIO___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = RipioExchangeDataSpot()
        self._http_client = HttpClient(venue=self.exchange_name, timeout=30)
        self.api_key = kwargs.get("public_key") or kwargs.get("api_key", "")
        self.api_secret = (
            kwargs.get("private_key") or kwargs.get("api_secret") or kwargs.get("secret_key") or ""
        )

    def _generate_signature(self, method: str, path: str, timestamp: str, body: str = "") -> str:
        sign_str = timestamp + method + path + body
        signature = hmac.new(
            self.api_secret.encode("utf-8"), sign_str.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return signature

    def _build_headers(self, method: str, path: str, body: str = "", is_sign: bool = False) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if is_sign and self.api_key and self.api_secret:
            timestamp = str(int(time.time() * 1000))
            signature = self._generate_signature(method, path, timestamp, body)
            headers["X-API-KEY"] = self.api_key
            headers["X-API-SIGNATURE"] = signature
            headers["X-API-TIMESTAMP"] = timestamp

        return headers

    def _build_url(self, path: str, params: dict[str, Any] | None = None) -> str:
        if " " in path:
            path = path.split(" ", 1)[1]

        url = self._params.rest_url + path

        if params:
            from urllib.parse import urlencode

            url = f"{url}?{urlencode(params)}"

        return url

    def request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        extra_data: dict[str, Any] | None = None,
        timeout: int = 10,
        is_sign: bool = False,
    ) -> RequestData:
        method = "GET"
        body_str = ""

        if body:
            method = "POST"
            import json

            body_str = json.dumps(body)

        headers = self._build_headers(method, path, body_str, is_sign)
        url = self._build_url(path, params)

        try:
            response = self._http_client.request(
                method=method,
                url=url,
                headers=headers,
                json_data=body if method == "POST" else None,
            )
            self.logger.info(f"Request: {method} {url}")
            return RequestData(response, extra_data or {})

        except Exception as e:
            self.logger.error(f"Request failed: {e}")
            raise

    async def async_request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        extra_data: dict[str, Any] | None = None,
        timeout: int = 5,
        is_sign: bool = False,
    ) -> RequestData:
        method = "GET"
        body_str = ""

        if body:
            method = "POST"
            import json

            body_str = json.dumps(body)

        headers = self._build_headers(method, path, body_str, is_sign)
        url = self._build_url(path, params)

        try:
            response = await self._http_client.async_request(
                method=method,
                url=url,
                headers=headers,
                json_data=body if method == "POST" else None,
            )
            self.logger.info(f"Async Request: {method} {url}")
            return RequestData(response, extra_data or {})

        except Exception as e:
            self.logger.error(f"Async request failed: {e}")
            raise

    def async_callback(self, future):
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as e:
            self.logger.error(f"Async callback error: {e}")

    def _get_server_time(self, extra_data=None, **kwargs):
        path = self._params.get_rest_path("get_tick").replace(":symbol", "BTC_USDT")
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_server_time",
                "normalize_function": self._get_server_time_normalize_function,
            }
        )
        return path, {}, extra_data

    def get_server_time(self, extra_data=None, **kwargs):
        path, params, extra_data = self._get_server_time(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    @staticmethod
    def _get_server_time_normalize_function(input_data, extra_data):
        if not input_data:
            return None, False
        if isinstance(input_data, dict):
            data = input_data.get("data", input_data)
            if isinstance(data, dict):
                ts = data.get("timestamp") or data.get("time")
                return ts, True
        return input_data, True

    def push_data_to_queue(self, data):
        if self.data_queue is not None:
            self.data_queue.put(data)

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def is_connected(self) -> bool:
        return True
