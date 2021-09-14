import logging
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

logger = logging.getLogger("marketstack")


class Marketstack(provider.Provider):
    BASE_URI = "http://api.marketstack.com/v1"
    PROVIDER_NAME = "marketstack"

    def __init__(
        self,
        id: str,
        parameters: MarketstackParameters,
        requester: MarketstackRequest,
    ):
        self._id = id
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
        res["open_date"] = parser.parse(d["date"]).date()
        res["close_date"] = res["open_date"]
        res["provider"] = Marketstack.provider_name
        res.pop("date")
        return res

    @staticmethod
    def update_candles(
        candles: Dict[str, MarketstackData], quote: MarketstackData
    ) -> Dict[str, MarketstackData]:

        if quote.symbol in candles:
            v_open = candles[quote.symbol].open
            v_low = candles[quote.symbol].low
            v_high = candles[quote.symbol].high
            v_close = candles[quote.symbol].close
            v_volume = candles[quote.symbol].volume

            v_adj_open = candles[quote.symbol].adj_open
            v_adj_low = candles[quote.symbol].adj_low
            v_adj_high = candles[quote.symbol].adj_high
            v_adj_close = candles[quote.symbol].adj_close
            v_open_date = candles[quote.symbol].open_date
            v_close_date = candles[quote.symbol].close_date
            v_adj_volume = candles[quote.symbol].adj_volume

            v_symbol = candles[quote.symbol].symbol
            v_provider = candles[quote.symbol].provider
            v_exchange = candles[quote.symbol].exchange
            v_split_factor = candles[quote.symbol].split_factor
            if quote.low < v_low:
                v_low = quote.low
            if quote.adj_low and v_adj_low is not None and quote.adj_low < v_adj_low:
                v_adj_low = quote.adj_low
            if quote.high > v_high:
                v_high = quote.high
            if (
                quote.adj_high is not None
                and v_adj_high is not None
                and quote.adj_high > v_adj_high
            ):
                v_adj_high = quote.adj_high
            if quote.open_date < v_open_date:
                v_open_date = quote.open_date
                v_open = quote.open
                v_adj_open = quote.adj_open
            if quote.close_date > v_close_date:
                v_close_date = quote.close_date
                v_close = quote.close
                v_adj_close = quote.adj_close
            v_volume += quote.volume
            if quote.adj_volume is not None and v_adj_volume is not None:
                v_adj_volume += quote.adj_volume
            candles[quote.symbol] = MarketstackData(
                v_symbol,
                v_open,
                v_high,
                v_low,
                v_close,
                v_open_date,
                v_close_date,
                v_provider,
                v_volume,
                v_split_factor,
                v_exchange,
                v_adj_open,
                v_adj_high,
                v_adj_low,
                v_adj_close,
                v_adj_volume,
            )
        else:
            candles[quote.symbol] = quote
        return candles

    def summerize_data(self, quotes: Sequence[MarketstackData]):
        candles: Dict[str, MarketstackData] = reduce(self.update_candles, quotes, {})
        res = [data for (symbol, data) in candles.items()]
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
