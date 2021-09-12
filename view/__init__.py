from abc import ABC, abstractmethod
from typing import Dict, Sequence

from market_data_loader import MarketData


class Render(ABC):
    @abstractmethod
    def render(self, quotes_by_id: Dict[str, Sequence[MarketData]]):
        """Method to render a Sequence[MarketData] into an appropriate output format

        Args:
            quotes (Sequence[MarketData]): The data to render
        """
