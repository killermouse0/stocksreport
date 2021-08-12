from dataclasses import dataclass

import market_data_loader


@dataclass
class MarketstackData(market_data_loader.MarketData):
    adj_open: float
    adj_high: float
    adj_low: float
    adj_close: float
    adj_volume: float
    volume: float
    split_factor: float
    exchange: str

    def __post_init__(self):
        self.open = self.adj_open if self.adj_open else self.open
        self.high = self.adj_high if self.adj_high else self.high
        self.low = self.adj_low if self.adj_low else self.low
        self.close = self.adj_close if self.adj_close else self.close
        self.volume = self.adj_volume if self.adj_volume else self.volume
