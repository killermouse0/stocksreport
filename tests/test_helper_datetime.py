import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import helpers.datetime

today = datetime.date(2021, 8, 19)


def test_midnight_ts():
    dt = helpers.datetime.DateTime(today)
    assert dt.get_midnight_ts() == 1629331200


def test_get_days_ago_ts():
    dt = helpers.datetime.DateTime(today)
    assert dt.get_days_ago_ts(10) == 1628467200


def test_get_days_ago():
    dt = helpers.datetime.DateTime(today)
    assert dt.get_days_ago(10) == "2021-08-09"


def test_get_today():
    dt = helpers.datetime.DateTime(today)
    assert dt.get_today() == "2021-08-19"
