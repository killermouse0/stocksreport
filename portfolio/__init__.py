import abc


class Portfolio(abc.ABC):
    @abc.abstractmethod
    def get_symbols_for_provider(self, provider: str):
        pass
