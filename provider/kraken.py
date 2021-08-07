import abc
import datetime
import time
from dataclasses import dataclass
from typing import Any, Dict, Sequence

import requests

import market_data_loader
import portfolio
import provider


@dataclass
class KrakenData(market_data_loader.MarketData):
    vwap: float
    volume: float
    num_trades: int
    date: datetime.date


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

    def fix_data(self, d: Dict[str, Any]) -> Dict[str, Any]:
        res = d.copy()
        res["date"] = datetime.datetime.fromtimestamp(d["time"]).date()
        res["provider"] = Kraken.provider_name
        res.pop("time")
        return res

    def get_quote(self, symbol: str) -> KrakenData:
        url = Kraken.BASE_URI + "OHLC"
        ts = Kraken.ten_days_ago()
        params = {"pair": symbol, "interval": 1440, "since": ts}
        res = self._requester.query(url, params=params)
        res = res["result"]
        last_ts = res["last"]
        for values in res[symbol]:
            if values[0] == last_ts:
                keys = [
                    "symbol",
                    "time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "vwap",
                    "volume",
                    "num_trades",
                    "provider",
                ]
                values = [symbol, *values, self.provider_name]
                d = dict(zip(keys, values))
                return KrakenData(**self.fix_data(d))
        raise provider.SymbolNotFoundError

    def get_quotes(self, ptf: portfolio.Portfolio) -> Sequence[KrakenData]:
        symbols = ptf.get_symbols()
        res = [self.get_quote(s) for s in symbols]
        return res

    @property
    def provider_name(self):
        return Kraken.PROVIDER_NAME
