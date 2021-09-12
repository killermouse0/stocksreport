import logging
import logging.config
import os

from helpers.datetime import DateTime
from market_data_loader import MarketDataLoader
from portfolio.csv_portfolio import CsvPortfolio
from provider.finnhub import Finnhub, FinnhubHttpRequest, FinnhubParametersDayCandle
from provider.finnhub.parameters import FinnhubParametersWeekCandle
from provider.kraken import Kraken, KrakenHttpRequest, KrakenParametersDayCandle
from provider.kraken.parameters import KrakenParametersWeekCandle
from provider.marketstack import (
    Marketstack,
    MarketstackHttpRequest,
    MarketstackParametersLatestDayCandle,
)
from provider.marketstack.parameters import MarketstackParametersWeekCandle
from view.renderer.webfront_render import WebfrontRender
from view.transformer.json_transformer import JsonTransformer

# from view.writer.console_writer import ConsoleWriter
from view.writer.s3_writer import S3Writer

PTF = "data/ptf.csv"
BUCKET = "sakana-stockpick-www"
S3_PREFIX = "data"


class NoTokenError(Exception):
    pass


def get_token(token_env: str):
    token = os.environ.get(token_env)
    if token is None:
        raise NoTokenError
    return token


def main(ptf_filename: str) -> None:

    # Which day are we interested in
    today = DateTime.today()

    # Loading the portfolio
    ptf = CsvPortfolio(ptf_filename)

    # Initializing the providers
    fh_request = FinnhubHttpRequest(token=get_token("FINNHUB_TOKEN"))
    fh_daily = Finnhub(
        id="fh_daily",
        requester=fh_request,
        parameters=FinnhubParametersDayCandle(today=today),
    )
    fh_weekly = Finnhub(
        id="fh_weekly",
        requester=fh_request,
        parameters=FinnhubParametersWeekCandle(today=today),
    )

    ms_request = MarketstackHttpRequest(token=get_token("MARKETSTACK_TOKEN"))
    ms_daily = Marketstack(
        id="ms_daily",
        requester=ms_request,
        parameters=MarketstackParametersLatestDayCandle(today=today),
    )
    ms_weekly = Marketstack(
        id="ms_weekly",
        requester=ms_request,
        parameters=MarketstackParametersWeekCandle(today=today),
    )

    kr_request = KrakenHttpRequest()
    kr_daily = Kraken(
        id="kr_daily",
        parameters=KrakenParametersDayCandle(today=today),
        requester=kr_request,
    )
    kr_weekly = Kraken(
        id="kr_weekly",
        parameters=KrakenParametersWeekCandle(today=today),
        requester=kr_request,
    )

    # Initializing the Market Data Loader and getting the data
    mdl = MarketDataLoader()
    mdl.register_providers(
        [ms_daily, ms_weekly, fh_daily, fh_weekly, kr_daily, kr_weekly]
    )
    quotes = mdl.get_quotes(ptf)

    # Writing the data
    transformer = JsonTransformer()
    writer = S3Writer(BUCKET, S3_PREFIX)
    # writer = ConsoleWriter()
    renderer = WebfrontRender(transformer=transformer, writer=writer)
    renderer.render(quotes_by_id=quotes)


if __name__ == "__main__":
    logging.config.fileConfig("logging.conf")
    main(PTF)
