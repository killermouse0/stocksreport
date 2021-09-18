import logging
from datetime import timedelta

from helpers.datetime import DateTime
from provider import ProviderParameters

logger = logging.getLogger("finnhub")


class FinnhubParameters(ProviderParameters):
    """Provides settings for Kraken provider"""

    def __init__(self, today: DateTime) -> None:
        self._today = today
        self._to = self._today.get_midnight_ts()

    def get_resolution(self):
        pass

    def get_from(self):
        pass

    def get_to(self):
        pass

    def get_interval(self):
        pass


class FinnhubParametersDayCandle(FinnhubParameters):
    def __init__(self, today: DateTime) -> None:
        super().__init__(today=today)
        self._from = self._today.get_days_ago_ts(10)
        logger.debug(f"Creating finnhub week candle from {self._from} to {self._to}")

    def get_resolution(self):
        return "D"

    def get_from(self):
        return self._from

    def get_to(self):
        return self._to

    def get_interval(self):
        return timedelta(days=0)


class FinnhubParametersWeekCandle(FinnhubParameters):
    def __init__(self, today: DateTime) -> None:
        super().__init__(today=today)
        self._from = self._today.get_days_ago_ts(10)

    def get_resolution(self):
        return "W"

    def get_from(self):
        return self._from

    def get_to(self):
        return self._to

    def get_interval(self):
        return timedelta(days=5)
