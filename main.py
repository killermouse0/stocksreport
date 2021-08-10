import os

from market_data_loader import MarketDataLoader
from portfolio.csv_portfolio import CsvPortfolio
from provider.finnhub import Finnhub, FinnhubHttpRequest
from provider.kraken import Kraken
from provider.marketstack import Marketstack, MarketstackHttpRequest
from view.renderer.webfront_render import WebfrontRender
from view.transformer.json_transformer import JsonTransformer
from view.writer.console_writer import ConsoleWriter

# from view.writer.s3_writer import S3Writer

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


def main(ptf_filename: str) -> None:
    # Loading the portfolio
    ptf = CsvPortfolio(ptf_filename)

    # Initializing the providers
    fh = Finnhub(requester=FinnhubHttpRequest(token=get_token("FINNHUB_TOKEN")))
    ms = Marketstack(
        requester=MarketstackHttpRequest(token=get_token("MARKETSTACK_TOKEN"))
    )
    kr = Kraken()

    # Initializing the Market Data Loader and getting the data
    mdl = MarketDataLoader(ptf)
    mdl.register_providers([ms, fh, kr])
    quotes = mdl.get_quotes()

    # Writing the data
    transformer = JsonTransformer()
    # writer = S3Writer(BUCKET, KEY)
    writer = ConsoleWriter()
    renderer = WebfrontRender(transformer=transformer, writer=writer)
    renderer.render(quotes=quotes)


if __name__ == "__main__":
    main(PTF)
