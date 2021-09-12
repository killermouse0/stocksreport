import logging
from csv import DictReader

from portfolio import Portfolio, PortfolioRow

logger = logging.getLogger("market_data_loader")


class CsvPortfolio(Portfolio):
    def __init__(self, filename: str) -> None:
        super().__init__()
        self._filename = filename
        self._load_csv()

    def _load_csv(self):
        with open(self._filename) as csv_file:
            lines = DictReader(csv_file)
            for line in lines:
                self.add_row(PortfolioRow(**line))
