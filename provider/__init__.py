from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, Sequence

import market_data_loader
import portfolio


class SymbolNotFoundError(Exception):
    """Exception we raise if the symbol lookup returns nothing or fails"""


class ProviderParameters(ABC):
    """Class to hold the parameters for a Provider"""


class Provider(ABC):
    @abstractmethod
    def get_quote(self, symbol: str) -> Optional[market_data_loader.MarketData]:
        pass

    @abstractmethod
    def get_quotes(
        self, portfolio: portfolio.Portfolio
    ) -> Sequence[market_data_loader.MarketData]:
        pass

    @abstractproperty
    def provider_name(self) -> str:
        pass

    @property
    def id(self):
        return self._id
