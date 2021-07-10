from provider import Provider
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

    def get_quotes(self, symbols: list):
        url = f"{Marketstack.BASE_URI}/eod/latest"
        params = {"symbols": ",".join(symbols)}
        res = self.query(url, params)
        data = res["data"]
        l = [{"symbol": q["symbol"], "quote": q} for q in data]
        return l
