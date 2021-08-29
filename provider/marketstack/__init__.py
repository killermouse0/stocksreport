import dataclasses
from functools import reduce, update_wrapper
from typing import Any, Dict, Sequence

from dateutil import parser

import portfolio
import provider
from provider.marketstack.data import MarketstackData
from provider.marketstack.parameters import (
    MarketstackParameters,
    MarketstackParametersLatestDayCandle,
    MarketstackParametersWeekCandle,
)
from provider.marketstack.request import MarketstackHttpRequest, MarketstackRequest


class Marketstack(provider.Provider):
    BASE_URI = "http://api.marketstack.com/v1"
    PROVIDER_NAME = "marketstack"

    def __init__(
        self,
        parameters: MarketstackParameters,
        requester: MarketstackRequest,
    ):
        self._parameters = parameters
        self._requester = requester

    def get_quote(self, symbol: str):
        url = f"{Marketstack.BASE_URI}/{self._parameters.endpoint()}"
        params = {"symbols": symbol}
        res = self._requester.query(url, params)
        data = res["data"][0]
        return MarketstackData(**self.fix_data(data))

    @staticmethod
    def fix_data(d: Dict[str, Any]) -> Dict[str, Any]:
        res = d.copy()
        res["date"] = parser.parse(d["date"]).date()
        res["provider"] = Marketstack.provider_name
        return res

    @staticmethod
    def update_candles(
        candles: Dict[str, Dict[str, Any]], quote: MarketstackData
    ) -> Dict[str, Dict[str, Any]]:
        if quote.symbol in candles:
            if quote.low < candles[quote.symbol]["low"]:
                candles[quote.symbol]["low"] = quote.low
            if (
                quote.adj_low is not None
                and quote.adj_low < candles[quote.symbol]["adj_low"]
            ):
                candles[quote.symbol]["adj_low"] = quote.adj_low
            if quote.high > candles[quote.symbol]["high"]:
                candles[quote.symbol]["high"] = quote.high
            if (
                quote.adj_high is not None
                and quote.adj_high > candles[quote.symbol]["adj_high"]
            ):
                candles[quote.symbol]["adj_high"] = quote.adj_high
            if quote.date < candles[quote.symbol]["min_date"]:
                candles[quote.symbol]["min_date"] = quote.date
                candles[quote.symbol]["open"] = quote.open
                candles[quote.symbol]["adj_open"] = quote.adj_open
                candles[quote.symbol]["date"] = quote.date
            if quote.date > candles[quote.symbol]["max_date"]:
                candles[quote.symbol]["max_date"] = quote.date
                candles[quote.symbol]["close"] = quote.close
                candles[quote.symbol]["adj_close"] = quote.adj_close
            candles[quote.symbol]["volume"] += quote.volume
            if quote.adj_volume is not None:
                candles[quote.symbol]["adj_volume"] += quote.adj_volume
        else:
            candles[quote.symbol] = {
                "symbol": quote.symbol,
                "date": quote.date,
                "low": quote.low,
                "high": quote.high,
                "min_date": quote.date,
                "max_date": quote.date,
                "volume": quote.volume,
                "close": quote.close,
                "open": quote.open,
                "adj_low": quote.adj_low,
                "adj_high": quote.adj_high,
                "adj_volume": quote.adj_volume,
                "adj_close": quote.adj_close,
                "adj_open": quote.adj_open,
                "provider": quote.provider,
                "split_factor": quote.split_factor,
                "exchange": quote.exchange,
            }
        return candles

    def summerize_data(self, quotes: Sequence[MarketstackData]):
        candles = reduce(self.update_candles, quotes, {})
        res = []
        print("Number of candle items = ", len(candles.items()))
        for (symbol, data) in candles.items():
            d = data.copy()
            valid_cols = set([f.name for f in dataclasses.fields(MarketstackData)])
            for col in data.keys():
                if col not in valid_cols:
                    d.pop(col)
            print(d)
            ms_data = MarketstackData(**d)
            print(ms_data)
            res.append(ms_data)
        return res

    def get_quotes(self, portfolio: portfolio.Portfolio) -> Sequence[MarketstackData]:
        url = f"{Marketstack.BASE_URI}/{self._parameters.endpoint()}"
        symbols = portfolio.get_symbols()
        params = self._parameters.params()
        params["symbols"] = ",".join(symbols)
        res = self._requester.query(url, params)
        data = res["data"]
        l_res = [MarketstackData(**self.fix_data(q)) for q in data]
        summerized_data = self.summerize_data(l_res)
        return summerized_data

    @property
    def provider_name(self) -> str:
        return self.PROVIDER_NAME
