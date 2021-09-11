import abc
import logging
from dataclasses import dataclass
from typing import List, Sequence


@dataclass
class PortfolioRow(abc.ABC):
    """This class represents a portfolio row"""

    symbol: str
    provider: str


class Portfolio:
    def __init__(self) -> None:
        self._portfolio: List[PortfolioRow] = []

    def add_row(self, row: PortfolioRow) -> None:
        self._portfolio.append(row)

    @classmethod
    def from_rows(cls, rows: Sequence[PortfolioRow]) -> "Portfolio":
        p = cls()
        for r in rows:
            p.add_row(r)
        return p

    def get_symbols(self):
        syms = [r.symbol for r in self._portfolio]
        return syms

    def filter_provider(self, provider: str) -> "Portfolio":
        logging.debug(f"Filtering portfolio for provider {repr(provider)}")
        return Portfolio.from_rows(
            [r for r in self._portfolio if r.provider == provider]
        )
