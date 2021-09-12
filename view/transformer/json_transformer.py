import json
from typing import Sequence

from market_data_loader import MarketData
from view.transformer import Transformer


class JsonTransformer(Transformer):
    def transform(self, var_name: str, quotes: Sequence[MarketData]) -> str:
        res_quotes = []
        for q in quotes:
            keys = ["open_date", "close_date", "symbol", "open", "close", "low", "high"]
            values = [
                q.open_date,
                q.close_date,
                q.symbol,
                q.open,
                q.close,
                q.low,
                q.high,
            ]
            res_q = dict(zip(keys, values))
            res_quotes.append(res_q)
        return "{} = {}".format(var_name, json.dumps(res_quotes, default=str))
