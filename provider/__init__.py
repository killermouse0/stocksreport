from __future__ import annotations

from typing import Dict, Sequence

import market_data_loader
import portfolio


class Provider:
    def get_quote(self, symbol: str) -> Dict[str, market_data_loader.MarketData]:
        pass

    def get_quotes(
        self, portfolio: portfolio.Portfolio
    ) -> Sequence[Dict[str, market_data_loader.MarketData]]:
        pass

    @property
    def provider_name(self) -> str:
        pass
