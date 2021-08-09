import json
from typing import Sequence

import boto3  # type: ignore

from market_data_loader import MarketData
from render import Render


class WebfrontRender(Render):
    """Renders data to S3 in JSON format"""

    def __init__(self, bucket: str, key: str) -> None:
        self.bucket = bucket
        self.key = key

    def render_to_json(self, quotes: Sequence[MarketData]):
        res_quotes = []
        for q in quotes:
            keys = ["date", "symbol", "open", "close", "low", "high"]
            values = [q.date, q.symbol, q.open, q.close, q.low, q.high]
            res_q = dict(zip(keys, values))
            res_quotes.append(res_q)
        return "json_data = {}".format(json.dumps(res_quotes, default=str))

    @staticmethod
    def upload_to_s3(bucket: str, key: str, data: str):
        s3 = boto3.client("s3")
        s3.put_object(Bucket=bucket, Key=key, Body=bytearray(data, "utf-8"))

    def render(self, quotes: Sequence[MarketData]):
        json_data = self.render_to_json(quotes)
        self.upload_to_s3(self.bucket, self.key, json_data)
