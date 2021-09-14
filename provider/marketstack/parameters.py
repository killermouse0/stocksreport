import logging
from abc import abstractmethod
from typing import Any, Dict

from helpers.datetime import DateTime
from provider import ProviderParameters

logger = logging.getLogger("marketstack")


class MarketstackParameters(ProviderParameters):
    def __init__(self, today: DateTime) -> None:
        super().__init__()
        self._today = today

    @abstractmethod
    def endpoint(self) -> str:
        pass

    @abstractmethod
    def params(self) -> Dict[str, Any]:
        pass


class MarketstackParametersLatestDayCandle(MarketstackParameters):
    def endpoint(self) -> str:
        return "eod/latest"

    def params(self) -> Dict[str, Any]:
        return {}


class MarketstackParametersWeekCandle(MarketstackParameters):
    def __init__(self, today: DateTime) -> None:
        super().__init__(today)
        self._date_from = today.get_days_ago(7)
        self._date_to = today.get_today()
        logger.debug(
            "Created MarketstackParameterWeekCandle"
            f" from {self._date_from} to {self._date_to}"
        )

    def endpoint(self) -> str:
        return "eod"

    def params(self) -> Dict[str, Any]:
        params = {}
        params["date_from"] = self._date_from
        params["date_to"] = self._date_to
        return params
