from provider import Provider
from portfolio import Portfolio
import requests


class Marketstack(Provider):
    BASE_URI = "http://api.marketstack.com/v1"

    def __init__(self, token: str):
        self._token = token
        pass

    def query(self, url, params):
        params["access_key"] = self._token
        res = requests.get(url, params=params)
        return res.json()

    def get_quote(self, symbol: str):
        url = f"{Marketstack.BASE_URI}/eod/latest"
        params = {"symbols": symbol}
        res = self.query(url, params)
        return {"symbol": symbol, "quote": res["data"][0]}

    def get_quotes(self, ptf: Portfolio):
        url = f"{Marketstack.BASE_URI}/eod/latest"
        ms_items = ptf.get_symbols_for_provider("marketstack")
        symbols = [x["symbol"] for x in ms_items]
        params = {"symbols": ",".join(symbols)}
        res = self.query(url, params)
        data = res["data"]
        l = [{"symbol": q["symbol"], "quote": q} for q in data]
        return l

    @property
    def provider_name(self):
        return "marketstack"
