from provider import Provider
from portfolio import Portfolio


class MarketDataLoader:
    def __init__(self, portfolio: Portfolio) -> None:
        self._providers = {}
        self._portfolio = portfolio

    def register_provider(self, provider: Provider):
        provider_name = provider.provider_name
        self._providers[provider_name] = provider

    def get_quotes(self):
        res = {}
        for k, provider in self._providers.items():
            res[k] = provider.get_quotes(self._portfolio)
        return res
