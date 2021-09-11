from __future__ import annotations

import abc
import datetime
import logging
from dataclasses import dataclass
from typing import Dict, List, Sequence

import provider
from portfolio import Portfolio


@dataclass
class MarketData(abc.ABC):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    date: datetime.date
    provider: str


class MarketDataLoader:
    def __init__(self) -> None:
        self._providers: Dict[str, provider.Provider] = {}

    def register_providers(self, providers: List[provider.Provider]):
        for p in providers:
            provider_name = p.provider_name
            self._providers[provider_name] = p

    def get_quotes(self, portfolio: Portfolio) -> Dict[str, Sequence[MarketData]]:
        res: Dict[str, Sequence[MarketData]] = {}
        logging.debug("get_quotes")
        for p_name, p_provider in self._providers.items():
            logging.debug(f"get_quotes for {p_name}")
            res[p_provider.get_id()] = p_provider.get_quotes(
                portfolio.filter_provider(p_name)
            )
        return res
