from typing import overload


class Portfolio:
    @overload
    def load(self):
        pass

    @overload
    def get_symbols(self):
        pass

    @overload
    def get_symbols_for_provider(self, provider: str):
        pass
