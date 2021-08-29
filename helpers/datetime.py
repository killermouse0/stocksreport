import datetime

import pytz


class DateTime:
    def __init__(self, today: datetime.date) -> None:
        self._today = today
        self._midnight = datetime.datetime.combine(
            self._today, datetime.time(0, 0, tzinfo=pytz.utc)
        )

    def get_today(self) -> str:
        return self._midnight.strftime("%Y-%m-%d")

    def get_midnight_ts(self) -> int:
        return int(self._midnight.timestamp())

    def get_days_ago_ts(self, n: int) -> int:
        return int((self._midnight - datetime.timedelta(days=n)).timestamp())

    def get_days_ago(self, n: int) -> str:
        return (self._midnight - datetime.timedelta(days=n)).strftime("%Y-%m-%d")

    @classmethod
    def today(cls):
        return cls(today=datetime.date.today())
