import datetime
from dataclasses import dataclass
from typing import Optional

import market_data_loader


@dataclass
class MarketstackData(market_data_loader.MarketData):
    open: float
    high: float
    low: float
    close: float
    volume: float
    split_factor: float
    exchange: str
    provider: str
    date: datetime.date
    adj_open: Optional[float] = None
    adj_high: Optional[float] = None
    adj_low: Optional[float] = None
    adj_close: Optional[float] = None
    adj_volume: Optional[float] = None
