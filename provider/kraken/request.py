import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

import requests

logger = logging.getLogger("kraken")


class KrakenRequest(ABC):
    @abstractmethod
    def query(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        pass


class KrakenHttpRequest(KrakenRequest):
    def query(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        res = requests.get(url, params=params)
        logger.debug(f"kraken request = {res.url}")
        return res.json()
