from typing import Dict, Sequence

from market_data_loader import MarketData
from view import Render
from view.transformer import Transformer
from view.writer import Writer


class WebfrontRender(Render):
    """Renders data to S3 in JSON format"""

    def __init__(self, transformer: Transformer, writer: Writer) -> None:
        self.transformer = transformer
        self.writer = writer

    def render(self, quotes_by_id: Dict[str, Sequence[MarketData]]):
        json_data_by_id = {
            id: self.transformer.transform(f"data_{id}", quotes)
            for (id, quotes) in quotes_by_id.items()
        }
        self.writer.write(json_data_by_id)
