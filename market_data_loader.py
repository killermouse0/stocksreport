from __future__ import annotations

import abc
import datetime
from typing import Dict, List, Sequence

import provider
from portfolio import Portfolio


class MarketData(abc.ABC):
    """
    symbol, open, high, low, close, date, provider
    """

    @abc.abstractproperty
    def symbol(self) -> str:
        pass

    @abc.abstractproperty
    def open(self) -> float:
        pass

    @abc.abstractproperty
    def high(self) -> float:
        pass

    @abc.abstractproperty
    def low(self) -> float:
        pass

    @abc.abstractproperty
    def close(self) -> float:
        pass

    @abc.abstractproperty
    def date(self) -> datetime.date:
        pass

    @abc.abstractproperty
    def provider(self) -> str:
        pass


class MarketDataLoader:
    def __init__(self, portfolio: Portfolio) -> None:
        self._providers: dict[str, provider.Provider] = {}
        self._portfolio = portfolio

    def register_providers(self, providers: List[provider.Provider]):
        for p in providers:
            provider_name = p.provider_name
            self._providers[provider_name] = p

    def get_quotes(self) -> Dict[str, Sequence[Dict[str, MarketData]]]:
        res = {}
        for p_name, p_provider in self._providers.items():
            res[p_name] = p_provider.get_quotes(self._portfolio)
        return res
