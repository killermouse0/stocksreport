import requests
from provider import Provider
from portfolio import Portfolio


class Finnhub(Provider):
    BASE_URI = "https://finnhub.io/api/v1"

    def __init__(self, token: str = None):
        self._token = token

    def query(self, url, params):
        headers = {"X-Finnhub-Token": self._token}
        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def get_quote(self, symbol: str):
        url = f"{Finnhub.BASE_URI}/quote"
        params = {"symbol": symbol}
        res = self.query(url, params)
        return {"symbol": symbol, "quote": res}

    def get_quotes(self, ptf: Portfolio):
        fh_items = ptf.get_symbols_for_provider("finnhub")
        symbols = [x["symbol"] for x in fh_items]
        res = [{"symbol": s, "quote": self.get_quote(s)} for s in symbols]
        return res

    @property
    def provider_name(self):
        return "finnhub"
