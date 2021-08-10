import json
from typing import Sequence

from market_data_loader import MarketData
from view.transformer import Transformer


class JsonTransformer(Transformer):
    def transform(self, quotes: Sequence[MarketData]) -> str:
        res_quotes = []
        for q in quotes:
            keys = ["date", "symbol", "open", "close", "low", "high"]
            values = [q.date, q.symbol, q.open, q.close, q.low, q.high]
            res_q = dict(zip(keys, values))
            res_quotes.append(res_q)
        return "json_data = {}".format(json.dumps(res_quotes, default=str))
