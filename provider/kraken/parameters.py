import datetime
import time

from provider import ProviderParameters


class KrakenParameters(ProviderParameters):
    """Provides settings for Kraken provider"""

    def get_interval():
        """Provides the interval parameter"""

    def get_since():
        """Provides the since parameter"""


class KrakenParametersDayCandle(KrakenParameters):
    """Provides parameters for Kraken Provider to fetch a day candle"""

    def get_interval(self):
        return 1440

    @staticmethod
    def ten_days_ago() -> int:
        now_ts = int(time.time())
        today_ts = now_ts - now_ts % (24 * 60 * 60)
        ten_days_ago_ts = today_ts - 10 * 24 * 60 * 60
        return ten_days_ago_ts

    def get_since(self, d: datetime.date = None) -> int:
        return self.ten_days_ago()


# class KrakenParametersWeekCandle(KrakenParameters):
#    """Provides parameters for Kraken Provider to fetch a week week candle"""
