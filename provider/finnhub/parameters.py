import time
from datetime import datetime, timedelta
from typing import Union

from provider import ProviderParameters


class FinnhubParameters(ProviderParameters):
    """Provides settings for Kraken provider"""

    def get_resolution():
        pass

    def get_from():
        pass

    def get_to():
        pass


class FinnhubParametersDayCandle(FinnhubParameters):
    def __init__(self) -> None:
        self._to = self.midnight()
        self._from = self._to - timedelta(days=10)

    @staticmethod
    def midnight(ts: Union[int, None] = None) -> datetime:
        if ts is None:
            ts = int(time.time())
        ts_midnight = ts - ts % (24 * 60 * 60)
        dt_midnight = datetime.fromtimestamp(ts_midnight)
        return dt_midnight

    def get_resolution(self):
        return "D"

    def get_from(self):
        return int(self._from.timestamp())

    def get_to(self):
        return int(self._to.timestamp())
