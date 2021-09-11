import json
import os
import sys
from datetime import date
from typing import Any, Dict

from dateutil import parser

from helpers.datetime import DateTime

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest

import portfolio
import provider.marketstack  # noqa: E402

today = DateTime(date(2021, 8, 12))
ptf = portfolio.Portfolio.from_rows([portfolio.PortfolioRow("BNP.XPAR", "marketstack")])


class MarketstackMockRequest(provider.marketstack.MarketstackRequest):
    def query(self, url: str, params: Dict[str, str]) -> Dict[str, Any]:
        res = {
            "pagination": {"limit": 100, "offset": 0, "count": 1, "total": 1},
            "data": [
                {
                    "open": 146.98,
                    "high": 147.84,
                    "low": 146.17,
                    "close": 147.06,
                    "volume": 46236448.0,
                    "adj_high": None,
                    "adj_low": None,
                    "adj_close": 147.06,
                    "adj_open": None,
                    "adj_volume": None,
                    "split_factor": 1.0,
                    "symbol": "AAPL",
                    "exchange": "XNAS",
                    "date": "2021-08-05T00:00:00+0000",
                }
            ],
        }
        return res


class MarketstackMockRequestWeek(provider.marketstack.MarketstackRequest):
    def __init__(self, filename: str) -> None:
        with open(filename) as file:
            self.json_data = json.load(file)

    def query(self, url: str, params: Dict[str, str]) -> Dict[str, Any]:
        return self.json_data


def test_get_quote():
    ms = provider.marketstack.Marketstack(
        id="test_quote",
        parameters=provider.marketstack.MarketstackParametersLatestDayCandle(
            today=today
        ),
        requester=MarketstackMockRequest(),
    )
    expected = provider.marketstack.MarketstackData(
        **{
            "open": 146.98,
            "high": 147.84,
            "low": 146.17,
            "close": 147.06,
            "volume": 46236448.0,
            "adj_high": None,
            "adj_low": None,
            "adj_close": 147.06,
            "adj_open": None,
            "adj_volume": None,
            "split_factor": 1.0,
            "symbol": "AAPL",
            "exchange": "XNAS",
            "date": parser.parse("2021-08-05T00:00:00+0000").date(),
            "provider": provider.marketstack.Marketstack.provider_name,
        }
    )
    res = ms.get_quote("AAPL")
    assert expected == res


def test_week_candle():
    ms = provider.marketstack.Marketstack(
        id="test_week_candle",
        parameters=provider.marketstack.MarketstackParametersWeekCandle(today=today),
        requester=MarketstackMockRequestWeek(
            filename="tests/data/marketstack_week.json"
        ),
    )
    quotes = ms.get_quotes(ptf)

    with pytest.raises(StopIteration) as exc_info:
        next((q for q in quotes if q.symbol == "TSLAX"))
    assert exc_info.errisinstance(StopIteration)

    tsla = next((q for q in quotes if q.symbol == "TSLA"))
    assert tsla.symbol == "TSLA"
    assert tsla.date == date(2021, 8, 12)
    assert tsla.low == 648.84
    assert tsla.high == 729.9
    assert tsla.open == 706.34
    assert tsla.close == 673.47


def test_get_id():
    ms = provider.marketstack.Marketstack(
        id="test_quote",
        parameters=provider.marketstack.MarketstackParametersLatestDayCandle(
            today=today
        ),
        requester=MarketstackMockRequest(),
    )
    assert ms.get_id() == "test_quote"
