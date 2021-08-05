import os
import sys
from typing import Dict, Sequence

from market_data_loader import MarketData, MarketDataLoader
from portfolio.csv_portfolio import CsvPortfolio
from provider.finnhub import Finnhub
from provider.kraken import Kraken
from provider.marketstack import Marketstack

PTF = "ptf.csv"

sys.path.append(os.path.join(os.path.dirname(__file__)))


def format_market_data(md: MarketData) -> str:
    res = "{}:{}:{}:{}:{}:{}".format(
        md.symbol, md.date, md.open, md.high, md.low, md.close
    )
    return res


def print_quotes(quotes: Dict[str, Sequence[Dict[str, MarketData]]]):
    for provider_name, provider_quotes in quotes.items():
        print(provider_name.upper(), "\n", "=" * len(provider_name), sep="")
        for q in provider_quotes:
            print(format_market_data(q["data"]))
        print()


if __name__ == "__main__":

    # Loading the portfolio
    ptf = CsvPortfolio(PTF)

    # Initializing the providers
    fh = Finnhub()
    ms = Marketstack()
    kr = Kraken()

    # Initializing the Market Data Loader
    mdl = MarketDataLoader(ptf)
    mdl.register_providers([ms, fh, kr])

    quotes = mdl.get_quotes()

    print_quotes(quotes)
