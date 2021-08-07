import abc
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Sequence, Union

import requests

import market_data_loader
import portfolio
import provider


@dataclass
class FinnhubData(market_data_loader.MarketData):
    """Dataclass holding a quote from Finnhub"""


class FinnhubRequest(abc.ABC):
    @abc.abstractmethod
    def query(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        pass


class FinnhubHttpRequest(FinnhubRequest):
    def __init__(self, token: str) -> None:
        self._token = token

    def query(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        headers = {"X-Finnhub-Token": self._token}
        res = requests.get(url, params=params, headers=headers)
        return res.json()


class Finnhub(provider.Provider):
    BASE_URI = "https://finnhub.io/api/v1"
    PROVIDER_NAME = "finnhub"

    def __init__(self, requester: FinnhubRequest):
        self._requester = requester

    @staticmethod
    def midnight(ts: Union[int, None] = None) -> datetime:
        if ts is None:
            ts = int(time.time())
        ts_midnight = ts - ts % (24 * 60 * 60)
        dt_midnight = datetime.fromtimestamp(ts_midnight)
        return dt_midnight

    @staticmethod
    def get_latest_quote(quotes: dict):
        keys = ["symbol", "t", "open", "high", "low", "close", "provider"]
        syms = [quotes["symbol"]] * len(quotes["t"])
        provs = [Finnhub.provider_name] * len(quotes["t"])
        values = zip(
            syms,
            quotes["t"],
            quotes["o"],
            quotes["h"],
            quotes["l"],
            quotes["c"],
            provs,
        )
        last_value = list(values)[-1]
        res = dict(zip(keys, last_value))
        return res

    def fix_data(self, d: Dict[str, Any]) -> Dict[str, Any]:
        res = d.copy()
        res["date"] = datetime.fromtimestamp(d["t"]).date()
        res.pop("t")
        return res

    def get_quote(self, symbol: str) -> FinnhubData:
        to_date = Finnhub.midnight()
        from_date = to_date - timedelta(days=10)
        url = f"{Finnhub.BASE_URI}/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": "D",
            "from": int(from_date.timestamp()),
            "to": int(to_date.timestamp()),
        }
        res = self._requester.query(url, params)
        res["symbol"] = symbol
        latest_quote = Finnhub.get_latest_quote(res)
        fh_res = FinnhubData(**self.fix_data(latest_quote))
        return fh_res

    def get_quotes(self, ptf: portfolio.Portfolio) -> Sequence[FinnhubData]:
        symbols = ptf.get_symbols()
        res = [self.get_quote(s) for s in symbols]
        return res

    @property
    def provider_name(self):
        return self.PROVIDER_NAME
