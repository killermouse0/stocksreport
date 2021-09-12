from __future__ import annotations

import abc
import datetime
import logging
from dataclasses import dataclass
from typing import Dict, List, Sequence

import provider
from portfolio import Portfolio

logger = logging.getLogger("market_data_loader")


@dataclass
class MarketData(abc.ABC):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    open_date: datetime.date
    close_date: datetime.date
    provider: str


class MarketDataLoader:
    def __init__(self) -> None:
        self._providers: Dict[str, provider.Provider] = {}

    def register_providers(self, providers: List[provider.Provider]):
        for p in providers:
            self._providers[p.id] = p

    def get_quotes(self, portfolio: Portfolio) -> Dict[str, Sequence[MarketData]]:
        res: Dict[str, Sequence[MarketData]] = {}
        logger.debug("get_quotes")
        logger.debug(f"Portfolio has {portfolio.num_rows} rows")
        for p_id, p_provider in self._providers.items():
            logger.debug(f"get_quotes for provider_id {p_id}")
            res[p_provider.id] = p_provider.get_quotes(
                portfolio.filter_provider(p_provider.provider_name)
            )
        return res
