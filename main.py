import json
import os
from typing import Sequence

import boto3

from market_data_loader import MarketData, MarketDataLoader
from portfolio.csv_portfolio import CsvPortfolio
from provider.finnhub import Finnhub, FinnhubHttpRequest
from provider.kraken import Kraken
from provider.marketstack import Marketstack, MarketstackHttpRequest

PTF = "ptf.csv"
BUCKET = "sakana-stockpick-www"
KEY = "data.js"


class NoTokenError(Exception):
    pass


def get_token(token_env: str):
    token = os.environ.get(token_env)
    if token is None:
        raise NoTokenError
    return token


def render_quotes(quotes: Sequence[MarketData]):
    res_quotes = []
    for q in quotes:
        keys = ["date", "symbol", "open", "close", "low", "high"]
        values = [q.date, q.symbol, q.open, q.close, q.low, q.high]
        res_q = dict(zip(keys, values))
        res_quotes.append(res_q)
    return "json_data = {}".format(json.dumps(res_quotes, default=str))


def upload_s3(bucket: str, key: str, data: str):
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=bytearray(data, "utf-8"))


def main(ptf_filename: str) -> None:
    # Loading the portfolio
    ptf = CsvPortfolio(ptf_filename)

    # Initializing the providers
    fh = Finnhub(requester=FinnhubHttpRequest(token=get_token("FINNHUB_TOKEN")))
    ms = Marketstack(
        requester=MarketstackHttpRequest(token=get_token("MARKETSTACK_TOKEN"))
    )
    kr = Kraken()

    # Initializing the Market Data Loader
    mdl = MarketDataLoader(ptf)
    mdl.register_providers([ms, fh, kr])

    quotes = mdl.get_quotes()

    data = render_quotes(quotes)
    upload_s3(BUCKET, KEY, data)


if __name__ == "__main__":
    main(PTF)
