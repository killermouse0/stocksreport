from dataclasses import dataclass

from market_data_loader import MarketData


@dataclass
class KrakenData(MarketData):
    vwap: float
    volume: float
    num_trades: int
