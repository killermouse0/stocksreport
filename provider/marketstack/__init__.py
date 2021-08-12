import abc
from dataclasses import dataclass
from typing import Any, Dict, Sequence

import requests
from dateutil import parser

import market_data_loader
import portfolio
import provider


@dataclass
class MarketstackData(market_data_loader.MarketData):
    adj_open: float
    adj_high: float
    adj_low: float
    adj_close: float
    adj_volume: float
    volume: float
    split_factor: float
    exchange: str

    def __post_init__(self):
        self.open = self.adj_open if self.adj_open else self.open
        self.high = self.adj_high if self.adj_high else self.high
        self.low = self.adj_low if self.adj_low else self.low
        self.close = self.adj_close if self.adj_close else self.close
        self.volume = self.adj_volume if self.adj_volume else self.volume


class MarketstackParameters(provider.ProviderParameters):
    @abc.abstractmethod
    def endpoint(self) -> str:
        pass


class MarketstackParametersLatestDayCandle(MarketstackParameters):
    def endpoint(self) -> str:
        return "eod/latest"


class MarketstackRequest(abc.ABC):
    @abc.abstractmethod
    def query(self, url: str, params: Dict[str, str]) -> Dict[str, Any]:
        pass


class MarketstackHttpRequest(MarketstackRequest):
    def __init__(self, token: str) -> None:
        self._token = token

    def query(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params["access_key"] = self._token
        res = requests.get(url, params=params)
        return res.json()


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
