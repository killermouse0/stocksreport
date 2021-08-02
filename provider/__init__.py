from __future__ import annotations

from typing import Dict, Sequence

import portfolio
from market_data_loader import MarketData


class Provider:
    def get_quote(self, symbol: str) -> Dict[str, MarketData]:
        pass

    def get_quotes(
        self, portfolio: portfolio.Portfolio
    ) -> Sequence[Dict[str, MarketData]]:
        pass

    @property
    def provider_name(self) -> str:
        pass
