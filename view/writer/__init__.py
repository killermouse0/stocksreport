from abc import ABC, abstractmethod


class Writer(ABC):
    """Class responsible for writing an str to somewhere"""

    @abstractmethod
    def write(self, data: str):
        """Method doing the actual writing"""
