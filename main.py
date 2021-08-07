import os
from typing import Sequence

from market_data_loader import MarketData, MarketDataLoader
from portfolio.csv_portfolio import CsvPortfolio
from provider.finnhub import Finnhub, FinnhubHttpRequest
from provider.kraken import Kraken
from provider.marketstack import Marketstack, MarketstackHttpRequest

PTF = "ptf.csv"


class NoTokenError(Exception):
    pass


def get_token(token_env: str):
    token = os.environ.get(token_env)
    if token is None:
        raise NoTokenError
    return token


def format_market_data(md: MarketData) -> str:
    res = "{}:{}:{}:{}:{}:{}".format(
        md.symbol, md.date, md.open, md.high, md.low, md.close
    )
    return res


def print_quotes(quotes: Sequence[MarketData]):
    for q in quotes:
        print(format_market_data(q))


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

    print_quotes(quotes)


if __name__ == "__main__":
    main(PTF)
