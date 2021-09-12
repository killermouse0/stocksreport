import datetime
from dataclasses import dataclass
from typing import Optional

from market_data_loader import MarketData


@dataclass
class MarketstackData(MarketData):
    volume: float
    split_factor: float
    exchange: str
    open_date: datetime.date
    adj_open: Optional[float] = None
    adj_high: Optional[float] = None
    adj_low: Optional[float] = None
    adj_close: Optional[float] = None
    adj_volume: Optional[float] = None
