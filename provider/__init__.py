from __future__ import annotations

import abc
from typing import Dict, Sequence

import market_data_loader
import portfolio


class Provider(abc.ABC):
    @abc.abstractmethod
    def get_quote(self, symbol: str) -> Dict[str, market_data_loader.MarketData]:
        pass

    @abc.abstractmethod
    def get_quotes(
        self, portfolio: portfolio.Portfolio
    ) -> Sequence[Dict[str, market_data_loader.MarketData]]:
        pass

    @abc.abstractproperty
    def provider_name(self) -> str:
        pass
