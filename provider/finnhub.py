import time
from datetime import date, datetime, timedelta
from typing import Union

import requests

import market_data_loader
import portfolio
import provider


class FinnhubData(market_data_loader.MarketData):
    def __init__(
        # noqa: E741
        self,
        symbol: str,
        o: float,
        c: float,
        h: float,
        l: float,  # noqa: E741
        t: int,
    ) -> None:
        self._symbol = symbol
        self._open = o
        self._close = c
        self._high = h
        self._low = l
        self._date = datetime.fromtimestamp(t).date()

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
    def date(self) -> date:
        return self._date

    @property
    def provider(self) -> str:
        return Finnhub.PROVIDER_NAME


class Finnhub(provider.Provider):
    BASE_URI = "https://finnhub.io/api/v1"
    PROVIDER_NAME = "finnhub"

    def __init__(self, token: str = None):
        self._token = token

    def query(self, url, params):
        headers = {"X-Finnhub-Token": self._token}
        res = requests.get(url, headers=headers, params=params)
        return res.json()

    @staticmethod
    def midnight(ts: Union[int, None] = None) -> datetime:
        if ts is None:
            ts = int(time.time())
        ts_midnight = ts - ts % (24 * 60 * 60)
        dt_midnight = datetime.fromtimestamp(ts_midnight)
        return dt_midnight

    @staticmethod
    def get_latest_quote(quotes: dict):
        syms = (quotes["symbol"] for _ in quotes["t"])
        q = zip(
            syms,
            quotes["o"],
            quotes["c"],
            quotes["h"],
            quotes["l"],
            quotes["t"],
        )
        list_q = list(q)
        res = list(list_q[-1])
        return res

    def get_quote(self, symbol: str):
        to_date = Finnhub.midnight()
        from_date = to_date - timedelta(days=10)
        url = f"{Finnhub.BASE_URI}/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": "D",
            "from": int(from_date.timestamp()),
            "to": int(to_date.timestamp()),
        }
        res = self.query(url, params)
        res["symbol"] = symbol
        last_quote = Finnhub.get_latest_quote(res)
        fh_res = FinnhubData(*last_quote)
        return fh_res

    def get_quotes(self, ptf: portfolio.Portfolio):
        fh_items = ptf.get_symbols_for_provider(self.provider_name)
        symbols = [x["symbol"] for x in fh_items]
        res = [{"symbol": s, "data": self.get_quote(s)} for s in symbols]
        return res

    @property
    def provider_name(self):
        return self.PROVIDER_NAME
