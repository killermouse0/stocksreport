import datetime
from typing import Any, Dict, Sequence

import portfolio
import provider
from provider.kraken.data import KrakenData
from provider.kraken.parameters import (
    KrakenParameters,
    KrakenParametersDayCandle,
    KrakenParametersWeekCandle,
)
from provider.kraken.request import KrakenHttpRequest, KrakenRequest


class Kraken(provider.Provider):
    BASE_URI = "https://api.kraken.com/0/public/"
    PROVIDER_NAME = "kraken"

    def __init__(
        self, id: str, parameters: KrakenParameters, requester: KrakenRequest
    ) -> None:
        self._id = id
        self._parameters = parameters
        self._requester = requester

    @staticmethod
    def fix_data(d: Dict[str, Any], add_to_start: int) -> Dict[str, Any]:
        res = d.copy()
        res["open_date"] = datetime.datetime.fromtimestamp(d["time"]).date()
        res["close_date"] = datetime.datetime.fromtimestamp(
            d["time"] + add_to_start
        ).date()
        res["provider"] = Kraken.provider_name
        res["open"] = float(res["open"])
        res["close"] = float(res["close"])
        res["high"] = float(res["high"])
        res["low"] = float(res["low"])
        res["vwap"] = float(res["vwap"])
        res["volume"] = float(res["volume"])
        res.pop("time")
        return res

    def get_quote(self, symbol: str) -> KrakenData:
        url = Kraken.BASE_URI + "OHLC"
        params = {
            "pair": symbol,
            "interval": self._parameters.get_interval(),
            "since": self._parameters.get_since(),
        }
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
                return KrakenData(
                    **self.fix_data(d, self._parameters.get_add_to_start())
                )
        raise provider.SymbolNotFoundError

    def get_quotes(self, ptf: portfolio.Portfolio) -> Sequence[KrakenData]:
        symbols = ptf.get_symbols()
        res = [self.get_quote(s) for s in symbols]
        return res

    @property
    def provider_name(self):
        return Kraken.PROVIDER_NAME
