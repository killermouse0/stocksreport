from abc import abstractmethod

from provider import ProviderParameters


class MarketstackParameters(ProviderParameters):
    @abstractmethod
    def endpoint(self) -> str:
        pass


class MarketstackParametersLatestDayCandle(MarketstackParameters):
    def endpoint(self) -> str:
        return "eod/latest"
