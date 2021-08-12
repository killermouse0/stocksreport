from abc import ABC, abstractmethod
from typing import Any, Dict

import requests


class MarketstackRequest(ABC):
    @abstractmethod
    def query(self, url: str, params: Dict[str, str]) -> Dict[str, Any]:
        pass


class MarketstackHttpRequest(MarketstackRequest):
    def __init__(self, token: str) -> None:
        self._token = token

    def query(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params["access_key"] = self._token
        res = requests.get(url, params=params)
        return res.json()
