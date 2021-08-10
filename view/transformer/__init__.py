from abc import ABC, abstractmethod
from typing import Sequence

from market_data_loader import MarketData


class Transformer(ABC):
    """Class is responsible for the transformation of a Sequence[MarketData]
    into a string that can be written out / stored"""

    @abstractmethod
    def transform(self, quotes: Sequence[MarketData]) -> str:
        """Method doing the actual transformation"""
