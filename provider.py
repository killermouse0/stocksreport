from typing import overload


class Provider:
    @overload
    def get_quote(self, symbol: str):
        pass

    @overload
    def get_quotes(self, symbols: list):
        pass
