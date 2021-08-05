from __future__ import annotations

import abc
import os
from typing import Dict, Optional, Sequence

import market_data_loader
import portfolio


class NoTokenError(Exception):
    pass


class Provider(abc.ABC):
    def __init__(self, token: Optional[str] = None):
        env_token = f"{self.provider_name}_TOKEN".upper()
        self._token = token if token else os.environ.get(env_token)
        if self._token is None:
            raise NoTokenError
        pass

    @abc.abstractmethod
    def get_quote(self, symbol: str) -> Optional[market_data_loader.MarketData]:
        pass

    @abc.abstractmethod
    def get_quotes(
        self, portfolio: portfolio.Portfolio
    ) -> Sequence[Dict[str, market_data_loader.MarketData]]:
        pass

    @abc.abstractproperty
    def provider_name(self) -> str:
        pass
