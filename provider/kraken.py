import abc
import datetime
import time
from typing import Any, Dict, Optional, Sequence

import requests

import market_data_loader
import portfolio
import provider


class KrakenData(market_data_loader.MarketData):
    def __init__(
        self,
        symbol: str,
        time: int,
        open: float,
        high: float,
        low: float,
        close: float,
        vwap: float,
        volume: float,
        num_trades: int,
    ) -> None:
        self._symbol = symbol
        self._date = datetime.datetime.fromtimestamp(time).date()
        self._open = open
        self._high = high
        self._low = low
        self._close = close
        self._vwap = vwap
        self._volume = volume
        self._num_trades = num_trades

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def open(self) -> float:
        return self._open

    @property
    def high(self) -> float:
        return self._high

    @property
    def low(self) -> float:
        return self._low

    @property
    def close(self) -> float:
        return self._close

    @property
    def date(self) -> datetime.date:
        return self._date

    @property
    def provider(self) -> str:
        return Kraken.PROVIDER_NAME


class KrakenRequest(abc.ABC):
    @abc.abstractmethod
    def query(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        pass


class KrakenHttpRequest(KrakenRequest):
    def query(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        res = requests.get(url, params=params)
        return res.json()


class Kraken(provider.Provider):
    BASE_URI = "https://api.kraken.com/0/public/"
    PROVIDER_NAME = "kraken"

    def __init__(self, requester: KrakenRequest = None) -> None:
        self._requester = requester or KrakenHttpRequest()

    @staticmethod
    def ten_days_ago() -> int:
        now_ts = int(time.time())
        today_ts = now_ts - now_ts % (24 * 60 * 60)
        ten_days_ago_ts = today_ts - 10 * 24 * 60 * 60
        return ten_days_ago_ts

    def get_quote(self, symbol: str) -> Optional[market_data_loader.MarketData]:
        url = Kraken.BASE_URI + "OHLC"
        ts = Kraken.ten_days_ago()
        params = {"pair": symbol, "interval": 1440, "since": ts}
        res = self._requester.query(url, params=params)
        res = res["result"]
        last_ts = res["last"]
        for values in res[symbol]:
            if values[0] == last_ts:
                return KrakenData(symbol, *values)
        return None

    def get_quotes(
        self, ptf: portfolio.Portfolio
    ) -> Sequence[Dict[str, market_data_loader.MarketData]]:
        kr_items = ptf.get_symbols_for_provider(self.provider_name)
        symbols = [x["symbol"] for x in kr_items]
        res = [{"symbol": s, "data": self.get_quote(s)} for s in symbols]
        return res

    @property
    def provider_name(self):
        return Kraken.PROVIDER_NAME
