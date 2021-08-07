from __future__ import annotations

import abc
from typing import Optional, Sequence

import market_data_loader
import portfolio


class SymbolNotFoundError(Exception):
    """Exception we raise if the symbol lookup returns nothing or fails"""


class Provider(abc.ABC):
    @abc.abstractmethod
    def get_quote(self, symbol: str) -> Optional[market_data_loader.MarketData]:
        pass

    @abc.abstractmethod
    def get_quotes(
        self, portfolio: portfolio.Portfolio
    ) -> Sequence[market_data_loader.MarketData]:
        pass

    @abc.abstractproperty
    def provider_name(self) -> str:
        pass
