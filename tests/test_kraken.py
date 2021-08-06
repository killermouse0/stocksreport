import datetime
import os
import sys
from typing import Any, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import provider.kraken  # noqa: E402


class KrakenMockRequest(provider.kraken.KrakenRequest):
    def query(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "error": [],
            "result": {
                "XXBTZUSD": [
                    [
                        1627862400,
                        "39889.9",
                        "40440.8",
                        "38700.0",
                        "39152.3",
                        "39553.8",
                        "3504.70836076",
                        26213,
                    ],
                    [
                        1627948800,
                        "39152.4",
                        "39791.1",
                        "37655.0",
                        "38163.0",
                        "38416.8",
                        "2952.96871944",
                        26951,
                    ],
                    [
                        1628035200,
                        "38163.0",
                        "39950.0",
                        "37527.9",
                        "39749.0",
                        "38930.4",
                        "3280.09621767",
                        25886,
                    ],
                    [
                        1628121600,
                        "39749.0",
                        "41403.5",
                        "37355.0",
                        "40886.4",
                        "39368.8",
                        "4722.98596131",
                        38580,
                    ],
                    [
                        1628208000,
                        "40886.5",
                        "41200.1",
                        "39900.0",
                        "40943.3",
                        "40521.7",
                        "1305.41357833",
                        10733,
                    ],
                ],
                "last": 1628121600,
            },
        }


def test_get_quote():
    k = provider.kraken.Kraken(requester=KrakenMockRequest())
    keys = [
        "symbol",
        "date",
        "open",
        "high",
        "low",
        "close",
        "vwap",
        "volume",
        "num_trades",
        "provider",
    ]
    values = [
        "XXBTZUSD",
        datetime.datetime.fromtimestamp(1628121600).date(),
        "39749.0",
        "41403.5",
        "37355.0",
        "40886.4",
        "39368.8",
        "4722.98596131",
        38580,
        provider.kraken.Kraken.provider_name,
    ]
    expected = provider.kraken.KrakenData(**dict(zip(keys, values)))
    res = k.get_quote("XXBTZUSD")
    assert expected == res
