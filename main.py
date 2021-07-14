import os
import json
from provider.finnhub import Finnhub
from provider.marketstack import Marketstack
from portfolio.csv_portfolio import CsvPortfolio
from market_data_loader import MarketDataLoader

PTF = "ptf.csv"

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
    print(json.dumps(quotes))
