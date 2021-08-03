from __future__ import annotations

import datetime
from typing import Dict, Sequence

import requests
from dateutil import parser

import market_data_loader
import portfolio
import provider


class MarketstackData(market_data_loader.MarketData):
    def __init__(
        self,
        date: str,
        symbol: str,
        adj_open: float,
        adj_high: float,
        adj_low: float,
        adj_close: float,
        adj_volume: float,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: float,
        **kwargs,
    ):
        self._symbol = symbol
        self._date = parser.parse(date).date()
        self._adj_open = adj_open
        self._adj_high = adj_high
        self._adj_low = adj_low
        self._adj_close = adj_close
        self._adj_volume = adj_volume
        self._open = open
        self._high = high
        self._low = low
        self._close = close
        self._volume = volume

    @property
    def date(self) -> datetime.date:
        return self._date

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def open(self) -> float:
        return self._adj_open if self._adj_open else self._open

    @property
    def high(self) -> float:
        return self._adj_high if self._adj_high else self._high

    @property
    def low(self) -> float:
        return self._adj_low if self._adj_low else self._low

    @property
    def close(self) -> float:
        return self._adj_close if self._adj_close else self._close

    @property
    def volume(self) -> float:
        return self._adj_volume if self._adj_volume else self._volume

    @property
    def provider(self) -> str:
        return Marketstack.PROVIDER_NAME


class Marketstack(provider.Provider):
    BASE_URI = "http://api.marketstack.com/v1"
    PROVIDER_NAME = "marketstack"

    def query(self, url, params):
        params["access_key"] = self._token
        res = requests.get(url, params=params)
        return res.json()

    def get_quote(self, symbol: str):
        url = f"{Marketstack.BASE_URI}/eod/latest"
        params = {"symbols": symbol}
        res = self.query(url, params)
        data = res["data"][0]
        return MarketstackData(**data)

    def get_quotes(
        self, portfolio: portfolio.Portfolio
    ) -> Sequence[Dict[str, market_data_loader.MarketData]]:
        url = f"{Marketstack.BASE_URI}/eod/latest"
        ms_items = portfolio.get_symbols_for_provider(self.provider_name)
        symbols = [x["symbol"] for x in ms_items]
        params = {"symbols": ",".join(symbols)}
        res = self.query(url, params)
        data = res["data"]
        l = [  # noqa: E741
            {"symbol": q["symbol"], "data": MarketstackData(**q)} for q in data
        ]
        return l

    @property
    def provider_name(self) -> str:
        return self.PROVIDER_NAME
