from dataclasses import dataclass

from market_data_loader import MarketData


@dataclass
class FinnhubData(MarketData):
    """Dataclass holding a quote from Finnhub"""
