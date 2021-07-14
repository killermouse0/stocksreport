from portfolio import Portfolio
from typing import overload


class Provider:
    @overload
    def get_quote(self, symbol: str):
        pass

    @overload
    def get_quotes(self, portfolio: Portfolio):
        pass

    @property
    @overload
    def provider_name(self):
        pass
