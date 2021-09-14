import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Sequence

import portfolio
import provider
from provider.finnhub.data import FinnhubData
from provider.finnhub.parameters import (
    FinnhubParameters,
    FinnhubParametersDayCandle,
    FinnhubParametersWeekCandle,
)
from provider.finnhub.request import FinnhubHttpRequest, FinnhubRequest

logger = logging.getLogger("finnhub")


class Finnhub(provider.Provider):
    BASE_URI = "https://finnhub.io/api/v1"
    PROVIDER_NAME = "finnhub"

    def __init__(
        self, id: str, parameters: FinnhubParameters, requester: FinnhubRequest
    ):
        self._id = id
        self._parameters = parameters
        self._requester = requester

    @staticmethod
    def get_latest_quote(quotes: dict):
        keys = ["symbol", "t", "open", "high", "low", "close", "provider"]
        syms = [quotes["symbol"]] * len(quotes["t"])
        provs = [Finnhub.provider_name] * len(quotes["t"])
        values = list(
            zip(
                syms,
                quotes["t"],
                quotes["o"],
                quotes["h"],
                quotes["l"],
                quotes["c"],
                provs,
            )
        )
        logger.debug(f"values = {repr(values)}")
        last_value = values[-1]
        res = dict(zip(keys, last_value))
        logger.debug(f"Last values = {repr(res)}")
        return res

    @staticmethod
    def fix_data(d: Dict[str, Any], interval: timedelta) -> Dict[str, Any]:
        res = d.copy()
        dt = datetime.fromtimestamp(d["t"])
        res["close_date"] = dt.date()
        res["open_date"] = (dt - interval).date()
        res.pop("t")
        return res

    def get_quote(self, symbol: str) -> FinnhubData:
        logger.debug("get_quote")
        url = f"{Finnhub.BASE_URI}/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": self._parameters.get_resolution(),
            "from": self._parameters.get_from(),
            "to": self._parameters.get_to(),
        }
        logger.debug(f"Params {params}")
        res = self._requester.query(url, params)
        logger.debug(f"Res = {repr(res)}")
        res["symbol"] = symbol
        latest_quote = Finnhub.get_latest_quote(res)
        fh_res = FinnhubData(
            **self.fix_data(latest_quote, self._parameters.get_interval())
        )
        return fh_res

    def get_quotes(self, ptf: portfolio.Portfolio) -> Sequence[FinnhubData]:
        symbols = ptf.get_symbols()
        res = [self.get_quote(s) for s in symbols]
        return res

    @property
    def provider_name(self):
        return self.PROVIDER_NAME
