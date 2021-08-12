from abc import ABC, abstractmethod
from typing import Any, Dict

import requests


class FinnhubRequest(ABC):
    @abstractmethod
    def query(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        pass


class FinnhubHttpRequest(FinnhubRequest):
    def __init__(self, token: str) -> None:
        self._token = token

    def query(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        headers = {"X-Finnhub-Token": self._token}
        res = requests.get(url, params=params, headers=headers)
        return res.json()
