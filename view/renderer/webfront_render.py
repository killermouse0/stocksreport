from typing import Sequence

from market_data_loader import MarketData
from view import Render
from view.transformer import Transformer
from view.writer import Writer


class WebfrontRender(Render):
    """Renders data to S3 in JSON format"""

    def __init__(self, transformer: Transformer, writer: Writer) -> None:
        self.transformer = transformer
        self.writer = writer

    def render(self, quotes: Sequence[MarketData]):
        json_data = self.transformer.transform(quotes)
        self.writer.write(json_data)
