import os
import sys

from market_data_loader import MarketData, MarketDataLoader
from portfolio.csv_portfolio import CsvPortfolio
from provider.finnhub import Finnhub
from provider.marketstack import Marketstack

PTF = "ptf.csv"

sys.path.append(os.path.join(os.path.dirname(__file__)))


def format_market_data(md: MarketData) -> str:
    res = "{}:{}:{}:{}:{}:{}:{}".format(
        md.provider, md.symbol, md.date, md.open, md.high, md.low, md.close
    )
    return res


if __name__ == "__main__":

    ptf = CsvPortfolio(PTF)
    mdl = MarketDataLoader(ptf)

    fh_token = os.environ.get("FINNHUB_TOKEN")
    if fh_token:
        fh = Finnhub(token=fh_token)
        mdl.register_provider(fh)

    ms_token = os.environ.get("MARKETSTACK_TOKEN")
    if ms_token:
        ms = Marketstack(token=ms_token)
        mdl.register_provider(ms)

    quotes = mdl.get_quotes()
    for md in quotes["marketstack"]:
        print(format_market_data(md["data"]))
    for md in quotes["finnhub"]:
        print(format_market_data(md["data"]))

    print(format_market_data(ms.get_quote("TSLA")))
