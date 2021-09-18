from helpers.datetime import DateTime
from provider import ProviderParameters


class KrakenParameters(ProviderParameters):
    """Provides settings for Kraken provider"""

    def __init__(self, today: DateTime):
        self._today = today

    def get_interval(self):
        """Provides the interval parameter"""

    def get_since(self):
        """Provides the since parameter"""

    def get_to(self):
        """Provides the end of the candle"""


class KrakenParametersDayCandle(KrakenParameters):
    """Provides parameters for Kraken Provider to fetch a day candle"""

    def __init__(self, today: DateTime):
        super().__init__(today)
        self._since = self._today.get_days_ago_ts(10)

    def get_interval(self):
        return 1440

    def get_since(self) -> int:
        return self._since

    def get_to(self):
        return self._since


class KrakenParametersWeekCandle(KrakenParameters):
    """Provides parameters for Kraken Provider to fetch a week week candle"""

    def __init__(self, today: DateTime):
        super().__init__(today)
        self._since = self._today.get_days_ago_ts(10)

    def get_interval(self):
        return 10080

    def get_since(self):
        return self._since

    def get_to(self):
        return self._since + 7 * 24 * 60 * 60
