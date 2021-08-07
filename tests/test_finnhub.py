import os
import sys
from datetime import datetime
from typing import Any, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import provider.finnhub  # noqa: E402


class FinnhubMockRequest(provider.finnhub.FinnhubRequest):
    def query(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        res = {
            "c": [
                122.8155,
                122.56986900000001,
                122.7902615316,
                122.87519054367901,
                122.62944016259165,
                122.84993980892907,
                123.40276453806923,
                123.95807697849054,
                124.04381372084846,
                123.79572609340676,
            ],
            "h": [
                123.492,
                123.245016,
                122.99852596800001,
                123.552019334856,
                123.3049152961863,
                123.05830546559392,
                123.61206784018908,
                124.16832214546992,
                124.72707959512454,
                124.47762543593429,
            ],
            "l": [
                122.631,
                122.385738,
                122.140966524,
                122.690600873358,
                122.44521967161128,
                122.20032923226806,
                122.75023071381325,
                123.30260675202541,
                123.85746848240952,
                123.6097535454447,
            ],
            "o": [
                123,
                122.754,
                122.508492,
                123.059780214,
                122.813660653572,
                122.56803333226486,
                123.11958948226004,
                123.6736276349302,
                124.23015895928738,
                123.98169864136881,
            ],
            "s": "ok",
            "t": [
                1626912000,
                1626998400,
                1627084800,
                1627171200,
                1627257600,
                1627344000,
                1627430400,
                1627516800,
                1627603200,
                1627689600,
            ],
            "v": [75, 63, 33, 54, 59, 33, 28, 80, 95, 48],
        }
        return res


def test_get_quote():
    ms = provider.finnhub.Finnhub(requester=FinnhubMockRequest())
    keys = ["symbol", "date", "open", "high", "low", "close", "provider"]
    values = [
        "AAPL",
        datetime.fromtimestamp(1627689600).date(),
        123.98169864136881,
        124.47762543593429,
        123.6097535454447,
        123.79572609340676,
        provider.finnhub.Finnhub.provider_name,
    ]
    expected = provider.finnhub.FinnhubData(**dict(zip(keys, values)))
    res = ms.get_quote("AAPL")
    assert expected == res
