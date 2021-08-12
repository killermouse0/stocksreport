from typing import Any, Dict, Sequence

from dateutil import parser

import portfolio
import provider
from provider.marketstack.data import MarketstackData
from provider.marketstack.parameters import MarketstackParameters
from provider.marketstack.request import MarketstackRequest


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

    def get_quotes(self, portfolio: portfolio.Portfolio) -> Sequence[MarketstackData]:
        url = f"{Marketstack.BASE_URI}/{self._parameters.endpoint()}"
        symbols = portfolio.get_symbols()
        params = {"symbols": ",".join(symbols)}
        res = self._requester.query(url, params)
        data = res["data"]
        l_res = [MarketstackData(**self.fix_data(q)) for q in data]
        return l_res

    @property
    def provider_name(self) -> str:
        return self.PROVIDER_NAME
