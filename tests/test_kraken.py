import os
import sys
from datetime import date
from typing import Any, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from helpers.datetime import DateTime
from provider.kraken import KrakenData  # noqa: E402
from provider.kraken import KrakenParametersDayCandle  # noqa: E402
from provider.kraken import KrakenParametersWeekCandle  # noqa: E402
from provider.kraken import Kraken, KrakenRequest  # noqa: E402

today = DateTime(date(2021, 8, 12))


class KrakenMockRequest(KrakenRequest):
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
    k = Kraken(
        id="kraken_test_get_quote",
        parameters=KrakenParametersDayCandle(today=today),
        requester=KrakenMockRequest(),
    )
    keys = [
        "symbol",
        "time",
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
        1628121600,
        "39749.0",
        "41403.5",
        "37355.0",
        "40886.4",
        "39368.8",
        "4722.98596131",
        38580,
        Kraken.provider_name,
    ]
    expected = KrakenData(**Kraken.fix_data(dict(zip(keys, values))))
    res = k.get_quote("XXBTZUSD")
    assert expected == res


def test_week_candle():
    week_candle = KrakenParametersWeekCandle(today=today)
    assert week_candle.get_interval() == 7 * 24 * 60
    assert week_candle.get_since() == 1627516800


def test_get_id():
    k = Kraken(
        id="kraken_test_get_quote",
        parameters=KrakenParametersDayCandle(today=today),
        requester=KrakenMockRequest(),
    )
    assert k.get_id() == "kraken_test_get_quote"
