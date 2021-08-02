import json
from csv import DictReader
from typing import Any, Dict, Sequence

from portfolio import Portfolio


class CsvPortfolio(Portfolio):
    def __init__(self, file: str) -> None:
        self._file = file
        self._portfolio: Sequence[Dict[str, Any]]
        self._load()

    def _load(self) -> None:
        with open(self._file) as csv_file:
            rows = DictReader(csv_file)
            self._portfolio = [{"symbol": r["symbol"], "attributes": r} for r in rows]

    def __str__(self) -> str:
        return json.dumps(self._portfolio)

    def get_symbols_for_provider(self, provider: str) -> Sequence[Dict[str, Any]]:
        res = [s for s in self._portfolio if s["attributes"]["provider"] == provider]
        return res
