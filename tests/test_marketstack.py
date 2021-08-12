import os
import sys
from typing import Any, Dict

from dateutil import parser

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import provider.marketstack  # noqa: E402


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


def test_get_quote():
    ms = provider.marketstack.Marketstack(
        parameters=provider.marketstack.MarketstackParametersLatestDayCandle(),
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
