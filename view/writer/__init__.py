from abc import ABC, abstractmethod
from typing import Dict


class Writer(ABC):
    """Class responsible for writing an str to somewhere"""

    @abstractmethod
    def write(self, data_by_id: Dict[str, str]):
        """Method doing the actual writing"""
